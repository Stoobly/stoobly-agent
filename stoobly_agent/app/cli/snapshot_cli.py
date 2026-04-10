import click
import os
import sys

from filelock import FileLock, Timeout

from stoobly_agent.app.models.factories.resource.local_db.helpers.log import Log
from stoobly_agent.app.models.factories.resource.local_db.helpers.log_event import PUT_ACTION, REQUEST_RESOURCE, SCENARIO_RESOURCE
from stoobly_agent.app.models.factories.resource.local_db.helpers.request_snapshot import RequestSnapshot
from stoobly_agent.app.models.factories.resource.local_db.helpers.scenario_snapshot import ScenarioSnapshot
from stoobly_agent.app.models.helpers.apply import Apply
from stoobly_agent.app.models.request_model import RequestModel
from stoobly_agent.app.models.scenario_model import ScenarioModel
from stoobly_agent.app.settings import Settings
from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.lib.api.keys import RequestKey, ScenarioKey

from .helpers.update_request_snapshots_service import update_request_snapshots

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
        sys.exit(1)
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
          request_ids.add(event.resource_uuid)
        elif event.resource == SCENARIO_RESOURCE:
          scenario_ids.add(event.resource_uuid)

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
          uuid = event.resource_uuid
          if uuid in processed_requests:
            continue
          processed_requests.add(uuid)

          ok = apply_service.request(uuid)
          if ok:
            success_count += 1
          else:
            failure_count += 1
        elif event.resource == SCENARIO_RESOURCE:
          uuid = event.resource_uuid
          if uuid in processed_scenarios:
            continue
          processed_scenarios.add(uuid)

          ok = apply_service.scenario(uuid)
          if ok:
            success_count += 1
          else:
            failure_count += 1

      if failure_count > 0:
        print(f"Completed with {failure_count} failures ({success_count} succeeded).", file=sys.stderr)
        sys.exit(1)
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
  destination = kwargs['destination']
  __copy_scenarios(kwargs['scenario_key'], destination)
  __copy_requests(kwargs['request_key'], destination)

@snapshot.command(
  help="Prune deleted snapshots."
)
@click.option('--dry-run', is_flag=True, default=False)
def prune(**kwargs):
  log = Log()
  log.prune(kwargs['dry_run'])

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

def __copy_requests(request_keys: list, destination: str):
  log = Log()

  data_dir = DataDir.instance(destination)
  destination_log = Log(data_dir)

  for request_key in request_keys:
    found = False

    for event in log.target_events:
      if event.action != PUT_ACTION:
        continue

      if event.resource != REQUEST_RESOURCE:
        continue

      key = RequestKey(request_key)
      if event.resource_uuid != key.id:
        continue

      snapshot: RequestSnapshot = event.snapshot()
      snapshot.copy(destination)
      resource = snapshot.find_resource()

      if not resource:
        print(f"Could not find request {key.id}", file=sys.stderr)
      else:
        destination_log.put(resource)
        found = True

      if not found:
        print(f"No snapshot found for {key}", file=sys.stderr)

def __copy_scenarios(scenario_keys: list, destination: str):
  log = Log()

  data_dir =  DataDir.instance(destination)
  destination_log = Log(data_dir)

  for scenario_key in scenario_keys:
    found = False

    for event in log.target_events:
      if event.action != PUT_ACTION:
        continue

      if event.resource != SCENARIO_RESOURCE:
        continue

      key = ScenarioKey(scenario_key)
      if event.resource_uuid != key.id:
        continue

      snapshot: ScenarioSnapshot = event.snapshot()
      snapshot.copy(destination)
      resource = snapshot.find_resource()

      if not resource:
        print(f"Could not find scenario {key.id}", file=sys.stderr)
      else:
        destination_log.put(resource)
        found = True

      if not found:
        print(f"No snapshot found for {key}", file=sys.stderr)

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
