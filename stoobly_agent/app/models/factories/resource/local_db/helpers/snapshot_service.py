import pdb

from stoobly_agent.lib.orm.request import Request
from stoobly_agent.lib.orm.scenario import Scenario

from .log import Log
from .log_event import Action, DELETE_ACTION, PUT_ACTION
from .request_snapshot import RequestSnapshot, RequestSnapshotOptions
from .scenario_snapshot import ScenarioSnapshot

def snapshot_request(request: Request, **options: RequestSnapshotOptions):
  action: Action = options.get('action')
  if not __validate_action(action):
    return

  snapshot = RequestSnapshot(request.uuid)

  snapshot.backup()

  if action == PUT_ACTION:
    snapshot.write(request, **options)
  elif action == DELETE_ACTION:
    snapshot.remove()

  log = Log()

  try:
    if action == PUT_ACTION:
      log.put(request)
    elif action == DELETE_ACTION:
      log.delete(request)
  except Exception as e:
    snapshot.rollback() 

  return snapshot.path

def snapshot_scenario(scenario: Scenario, **options):
  action: Action = options.get('action')
  if not __validate_action(action):
    return

  snapshot = ScenarioSnapshot(scenario.uuid)

  snapshot.backup_metadata()

  if action == PUT_ACTION:
    snapshot.write_metadata(scenario)
  elif action == DELETE_ACTION:
    snapshot.remove_metadata()

  snapshot.backup_requests()

  if action == PUT_ACTION:
    snapshot.remove_requests()
    snapshot.write_requests(scenario, **options)
  elif action == DELETE_ACTION:
    snapshot.remove_requests()

  log = Log()

  if action == PUT_ACTION:
    log.put(scenario)
  elif action == DELETE_ACTION:
    log.delete(scenario)

  return snapshot.metadata_path

def __validate_action(action: Action):
  return action == PUT_ACTION or action == DELETE_ACTION 