import click
import os
import sys

from filelock import FileLock, Timeout

from stoobly_agent.app.models.factories.resource.local_db.helpers.log import Log
from stoobly_agent.app.models.factories.resource.local_db.helpers.log_event import (
  MalformedLogEventError,
  PUT_ACTION,
  REQUEST_RESOURCE,
  SCENARIO_RESOURCE,
)
from stoobly_agent.app.models.factories.resource.local_db.helpers.request_snapshot import (
  MalformedRequestSnapshotError,
  RequestSnapshot,
)
from stoobly_agent.app.models.factories.resource.local_db.helpers.scenario_snapshot import (
  ScenarioSnapshot,
  ScenarioSnapshotV2,
)
from stoobly_agent.app.models.factories.resource.local_db.helpers.snapshot_format import (
  FORMAT_NONE,
  FORMAT_V1,
  FORMAT_V2,
  detect_snapshot_format,
  resolve_write_format,
)
from stoobly_agent.app.models.factories.resource.local_db.helpers.snapshot_migrate import migrate_snapshots
from stoobly_agent.app.models.helpers.apply import Apply
from stoobly_agent.app.models.request_model import RequestModel
from stoobly_agent.app.models.scenario_model import ScenarioModel
from stoobly_agent.app.settings import Settings
from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.lib.api.keys import RequestKey, ScenarioKey
from stoobly_agent.lib.orm.scenario import Scenario

from .helpers.update_request_snapshots_service import update_request_snapshots

SNAPSHOT_FORMAT_CHOICES = ['v1', 'v2']
SNAPSHOT_FORMAT_MAP = {
  'v1': FORMAT_V1,
  'v2': FORMAT_V2,
}

@click.group(
    epilog="Run 'stoobly-agent project COMMAND --help' for more information on a command.",
    help="Manage snapshots"
)
@click.pass_context
def snapshot(ctx):
    pass

@snapshot.command(
  help="Apply snapshots.",
)
@click.option('--force', is_flag=True, default=False, help="Toggles whether resources are hard deleted.")
@click.option('--lock-timeout', default=60, type=int, help='Lock timeout in seconds (default: 60).')
@click.argument('uuid', required=False)
def apply(**kwargs):
  data_dir: DataDir = DataDir.instance()
  lock_file_path = os.path.join(data_dir.tmp_dir_path, '.snapshot-apply.lock')
  lock = FileLock(lock_file_path, timeout=kwargs.get('lock_timeout', 60))

  try:
    with lock:
      apply = Apply(force=kwargs['force']).with_logger(print)
      completed = True

      if kwargs.get('uuid'):
        completed = apply.single(kwargs['uuid'])
      else:
        completed = apply.all()

      if not completed:
        if apply.last_error:
          print(f"Error: {apply.last_error}", file=sys.stderr)
        sys.exit(1)
  except (MalformedLogEventError, MalformedRequestSnapshotError) as e:
    __abort_with_error(e)
  except Timeout:
    print("Error: Another snapshot apply command is already running. Please wait for it to complete.", file=sys.stderr)
    sys.exit(1)

@snapshot.command(
  help="Reset requests and scenarios that have snapshots to their last snapshot state."
)
@click.option('--hard', is_flag=True, default=False, help='Delete all requests and scenarios before resetting.')
@click.option('--lock-timeout', default=60, type=int, help='Lock timeout in seconds (default: 60).')
@click.option('--yes', is_flag=True, default=False, help='Proceed without confirmation.')
def reset(**kwargs):
  data_dir: DataDir = DataDir.instance()
  lock_file_path = os.path.join(data_dir.tmp_dir_path, '.snapshot-reset.lock')
  lock = FileLock(lock_file_path, timeout=kwargs.get('lock_timeout', 60))

  try:
    with lock:
      log = Log()
      apply_service = Apply().with_logger(print)

      # Determine unique resources to be reset for confirmation
      request_ids = set()
      scenario_ids = set()

      for event in log.target_events:
        if event.action != PUT_ACTION:
          continue
        if event.resource == REQUEST_RESOURCE:
          request_ids.add(event.resource_id)
        elif event.resource == SCENARIO_RESOURCE:
          scenario_ids.add(event.resource_id)

      if not kwargs.get('yes'):
        total = len(request_ids) + len(scenario_ids)
        message = f"This will reset {len(request_ids)} request(s) and {len(scenario_ids)} scenario(s) to their last snapshot state ({total} total)."
        if kwargs.get('hard'):
          message += "\nWARNING: --hard is set and will delete ALL requests and scenarios before resetting."
        message += " Continue?"
        if not click.confirm(message, default=False):
          print("Aborted.")
          return

      if kwargs.get('hard'):
        __hard_delete_all(force=True)

      processed_requests = set()
      processed_scenarios = set()
      success_count = 0
      failure_count = 0

      # Iterate latest snapshot events and reset corresponding resources
      for event in log.target_events:
        if event.action != PUT_ACTION:
          continue

        if event.resource == REQUEST_RESOURCE:
          uuid = event.resource_id
          if uuid in processed_requests:
            continue
          processed_requests.add(uuid)

          ok = apply_service.request(uuid)
          if ok:
            success_count += 1
          else:
            failure_count += 1
            if apply_service.last_error:
              print(f"Error: {apply_service.last_error}", file=sys.stderr)
        elif event.resource == SCENARIO_RESOURCE:
          uuid = event.resource_id
          if uuid in processed_scenarios:
            continue
          processed_scenarios.add(uuid)

          ok = apply_service.scenario(uuid)
          if ok:
            success_count += 1
          else:
            failure_count += 1
            if apply_service.last_error:
              print(f"Error: {apply_service.last_error}", file=sys.stderr)

      if failure_count > 0:
        print(f"Completed with {failure_count} failures ({success_count} succeeded).", file=sys.stderr)
        sys.exit(1)
  except (MalformedLogEventError, MalformedRequestSnapshotError) as e:
    __abort_with_error(e)
  except Timeout:
    print("Error: Another snapshot reset command is already running. Please wait for it to complete.", file=sys.stderr)
    sys.exit(1)

@snapshot.command(
  help="Copy snapshots to a different data directory."
)
@click.option('--request-key', multiple=True, help='')
@click.option('--scenario-key', multiple=True, help='')
@click.argument('destination', required=True)
def copy(**kwargs):
  try:
    destination = kwargs['destination']
    __copy_scenarios(kwargs['scenario_key'], destination)
    __copy_requests(kwargs['request_key'], destination)
  except (MalformedLogEventError, MalformedRequestSnapshotError) as e:
    __abort_with_error(e)

@snapshot.command(
  help="Prune deleted snapshots."
)
@click.option('--dry-run', is_flag=True, default=False)
def prune(**kwargs):
  try:
    log = Log()
    log.prune(kwargs['dry_run'])
  except (MalformedLogEventError, MalformedRequestSnapshotError) as e:
    __abort_with_error(e)

@snapshot.command(
  help="Update a snapshot.",
)
@click.option('--no-verify', is_flag=True, default=False)
@click.option('--lifecycle-hooks-path', help='Path to lifecycle hooks script.')
@click.argument('file_path')
def update(**kwargs):
  update_request_snapshots(
    file_path=kwargs['file_path'],
    lifecycle_hooks_path=kwargs.get('lifecycle_hooks_path'),
    no_verify=kwargs.get('no_verify', False)
  )

@snapshot.command(
  help="Migrate snapshots to v1 or v2 format.",
)
@click.option(
  '--format',
  'format',
  required=True,
  type=click.Choice(SNAPSHOT_FORMAT_CHOICES),
  help='Target snapshot format.',
)
def migrate(**kwargs):
  format_name = kwargs['format']
  target_format = SNAPSHOT_FORMAT_MAP[format_name]
  data_dir = DataDir.instance()
  result = migrate_snapshots(data_dir, format=target_format)

  if result.get('noop'):
    if detect_snapshot_format(data_dir) == FORMAT_NONE:
      print("No snapshots to migrate.")
    else:
      print(f"Snapshots are already in {format_name} format.")
    return

  print(
    f"Migrated {result['requests']} request(s) and {result['scenarios']} scenario(s) to {format_name}."
  )

def __copy_requests(request_keys: list, destination: str):
  log = Log()

  data_dir = DataDir.instance(destination)
  destination_log = Log(data_dir)
  write_format = resolve_write_format(data_dir)

  for request_key in request_keys:
    found = False
    key = RequestKey(request_key)

    for event in log.target_events:
      if event.action != PUT_ACTION:
        continue

      if event.resource != REQUEST_RESOURCE:
        continue

      if event.resource_id != key.id:
        continue

      snapshot: RequestSnapshot = event.snapshot()
      snapshot.copy(destination)
      resource = snapshot.find_resource()

      if not resource:
        print(f"Could not find request {key.id}", file=sys.stderr)
      else:
        destination_log.put(resource, format=write_format)
        found = True

    if not found:
      print(f"No snapshot found for {key}", file=sys.stderr)

def __scenario_event_matches_uuid(event, scenario_uuid: str) -> bool:
  """Match history events to a scenario UUID (v1 bare uuid or v2 name/uuid)."""
  if event.resource_id == scenario_uuid:
    return True

  # Legacy name-only / resolve via on-disk snapshot UUID
  snapshot = event.snapshot()
  if snapshot.uuid == scenario_uuid:
    return True

  # DELETE may have already removed YAML; match locator or legacy name stem
  scenario = Scenario.find_by(uuid=scenario_uuid)
  if scenario:
    locator = ScenarioSnapshotV2.history_locator_for(scenario.uuid, scenario.name)
    if event.resource_uuid == locator:
      return True
    if event.resource_id == scenario.name or event.resource_uuid == scenario.name:
      return True

  return False

def __copy_scenarios(scenario_keys: list, destination: str):
  log = Log()

  data_dir =  DataDir.instance(destination)
  destination_log = Log(data_dir)
  write_format = resolve_write_format(data_dir)

  for scenario_key in scenario_keys:
    found = False
    key = ScenarioKey(scenario_key)

    for event in log.target_events:
      if event.action != PUT_ACTION:
        continue

      if event.resource != SCENARIO_RESOURCE:
        continue

      if not __scenario_event_matches_uuid(event, key.id):
        continue

      snapshot: ScenarioSnapshot = event.snapshot()
      snapshot.copy(destination)
      resource = snapshot.find_resource()

      if not resource:
        print(f"Could not find scenario {key.id}", file=sys.stderr)
      else:
        destination_log.put(resource, format=write_format)
        found = True

    if not found:
      print(f"No snapshot found for {key}", file=sys.stderr)

def __abort_with_error(error: Exception):
  print(f"Error: {error}", file=sys.stderr)
  sys.exit(1)

def __hard_delete_all(force: bool):
  settings = Settings.instance()

  request_model = RequestModel(settings)
  request_model.as_local()
  # Delete all requests first
  while True:
    res, status = request_model.index(page=0, size=100)
    if status != 200:
      print(f"Error: Failed to list requests for hard delete (status: {status}).", file=sys.stderr)
      sys.exit(1)
    requests = res.get('list') or []
    if not requests:
      break
    for r in requests:
      request_model.destroy(r['uuid'], force=force)

  scenario_model = ScenarioModel(settings)
  scenario_model.as_local()
  # Then delete all scenarios
  while True:
    res, status = scenario_model.index(page=0, size=100)
    if status != 200:
      print(f"Error: Failed to list scenarios for hard delete (status: {status}).", file=sys.stderr)
      sys.exit(1)
    scenarios = res.get('list') or []
    if not scenarios:
      break
    for s in scenarios:
      scenario_model.destroy(s['uuid'], force=force)
