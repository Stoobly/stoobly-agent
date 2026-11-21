from typing import TYPE_CHECKING

from stoobly_agent.config.data_dir import DataDir

if TYPE_CHECKING:
  from stoobly_agent.lib.orm.request import Request
  from stoobly_agent.lib.orm.scenario import Scenario

from .log import Log
from .log_event import Action, DELETE_ACTION, PUT_ACTION
from .request_slug import build_request_slug
from .request_snapshot import RequestSnapshotV1, RequestSnapshotV2, RequestSnapshotOptions
from .scenario_snapshot import ScenarioSnapshotV1, ScenarioSnapshotV2
from .snapshot_format import FORMAT_V2, resolve_write_format

def snapshot_request(request: 'Request', **options: RequestSnapshotOptions):
  action: Action = options.get('action')
  if not __validate_action(action):
    return

  data_dir = DataDir.instance(options.get('data_dir_path'))
  write_format = options.get('format')
  if write_format is None:
    write_format = resolve_write_format(data_dir)

  if write_format == FORMAT_V2:
    snapshot = RequestSnapshotV2(
      request.uuid,
      data_dir,
      slug=build_request_slug(request.method, request.path),
    )
  else:
    snapshot = RequestSnapshotV1(request.uuid, data_dir)

  snapshot.backup()

  log = Log(data_dir)

  if action == PUT_ACTION:
    snapshot.write(request, **options)
  elif action == DELETE_ACTION:
    inverted_scenario_index = log.scenario_inverted_index

    # If a scenario currently depends on this request, we can't remove the snapshot until the scenario is also removed
    log.remove_request_snapshot(snapshot, inverted_scenario_index)

  try:
    if action == PUT_ACTION:
      log.put(request, format=write_format)
    elif action == DELETE_ACTION:
      log.delete(request, format=write_format)
  except Exception as e:
    snapshot.rollback()

  return snapshot.path

def snapshot_scenario(scenario: 'Scenario', **options):
  action: Action = options.get('action')
  if not __validate_action(action):
    return

  data_dir = DataDir.instance(options.get('data_dir_path'))
  write_format = options.get('format')
  if write_format is None:
    write_format = resolve_write_format(data_dir)

  if write_format == FORMAT_V2:
    snapshot = ScenarioSnapshotV2(scenario.uuid, data_dir, name=scenario.name)
  else:
    snapshot = ScenarioSnapshotV1(scenario.uuid, data_dir)

  snapshot.backup_metadata()

  if action == PUT_ACTION:
    snapshot.write_metadata(scenario)

  # Backup/remove requests before deleting metadata: v2 stores the request
  # list in the scenario YAML, so metadata must still exist while iterating.
  snapshot.backup_requests()

  log = Log(data_dir)
  inverted_scenario_index = log.scenario_inverted_index
  if action == PUT_ACTION:
    snapshot.remove_requests(
      lambda snap: log.remove_request_snapshot(
        snap,
        inverted_scenario_index,
        ignore_scenario_ids=[scenario.uuid],
      )
    )
    snapshot.write_requests(scenario, **options)
  elif action == DELETE_ACTION:
    # Ignore this scenario so its exclusive requests are removed; requests still
    # referenced by other scenarios are kept.
    snapshot.remove_requests(
      lambda snap: log.remove_request_snapshot(
        snap,
        inverted_scenario_index,
        ignore_scenario_ids=[scenario.uuid],
      )
    )
    snapshot.remove_metadata()

  if action == PUT_ACTION:
    log.put(scenario, format=write_format)
  elif action == DELETE_ACTION:
    log.delete(scenario, format=write_format)

  return snapshot.metadata_path

def __validate_action(action: Action):
  return action == PUT_ACTION or action == DELETE_ACTION
