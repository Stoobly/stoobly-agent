import os
import pdb
import sys

from stoobly_agent.app.cli.helpers.handle_replay_service import DEFAULT_FORMAT, handle_before_replay, handle_after_replay, print_session, ReplaySession
from stoobly_agent.app.cli.helpers.handle_test_service import SessionContext, exit_on_failure, handle_test_complete, handle_test_session_complete 
from stoobly_agent.app.cli.helpers.print_service import print_scenarios, select_print_options
from stoobly_agent.app.cli.helpers.test_facade import TestFacade
from stoobly_agent.app.cli.helpers.context import ReplayContext
from stoobly_agent.app.models.factories.resource.local_db.helpers.scenario_snapshot import ScenarioSnapshot
from stoobly_agent.app.models.helpers.apply import Apply
from stoobly_agent.app.models.factories.resource.local_db.helpers.log import Log
from stoobly_agent.app.models.factories.resource.local_db.helpers.log_event import SCENARIO_RESOURCE, PUT_ACTION
from stoobly_agent.app.proxy.test.helpers.diff_service import diff as diff_strings
from stoobly_agent.app.settings import Settings
from stoobly_agent.config.constants import alias_resolve_strategy, env_vars
from stoobly_agent.lib.logger import bcolors, Logger

from ..helpers.scenario_facade import ScenarioFacade
from ..helpers.validations import *
from ..types.scenario import ScenarioTestOptions
from ..helpers.diff_request_print import analyze_request_diff, emit_request_diff, emit_request_diff_header

def create_handler(kwargs):
  print_options = select_print_options(kwargs)

  settings = Settings.instance()
  project_key = resolve_project_key_and_validate(kwargs, settings) 

  scenario = ScenarioFacade(settings)

  res, status = scenario.create(project_key, kwargs['name'], kwargs['description'])

  if filter_response(res, status):
      sys.exit(1)

  print_scenarios([res], **print_options)

def delete_handler(kwargs):
  validate_scenario_key(kwargs['scenario_key'])

  scenario = ScenarioFacade(Settings.instance())
  res, status = scenario.show(kwargs['scenario_key'])

  if filter_response(res, status):
    sys.exit(1)

  is_deleted = res.get('is_deleted')
  if not res:
    print(f"Error: Could not find scenario", file=sys.stderr)
    sys.exit(1)

  res = scenario.delete(kwargs['scenario_key'])
  if not res:
    print('Error: Could not delete scenario', file=sys.stderr)
    sys.exit(1)

  if not is_deleted:
    print('Scenario moved to trash!')
  else:
    print('Scenario deleted!')

def list_handler(kwargs):
  print_options = select_print_options(kwargs)

  settings = Settings.instance()

  project_key = resolve_project_key_and_validate(kwargs, settings)
  if 'project_key' in kwargs:
      del kwargs['project_key']

  if kwargs.get('search'):
      kwargs['q'] = kwargs['search']
      del kwargs['search']

  scenario = ScenarioFacade(settings)

  scenarios_response, status = scenario.index(project_key, kwargs)
  if filter_response(scenarios_response, status):
      sys.exit(1)

  if len(scenarios_response['list']) == 0:
      print('No scenarios found.')
  else:
      print_scenarios(scenarios_response['list'], **print_options) 

def replay_handler(kwargs):
  os.environ[env_vars.LOG_LEVEL] = kwargs['log_level']

  scenario_key = validate_scenario_key(kwargs['key'])

  if kwargs.get('scenario_key'):
      if kwargs['scenario_key'] and not kwargs.get('record'):
          print("Error: Missing option '--record'.", file=sys.stderr)
          sys.exit(1)

      validate_scenario_key(kwargs['scenario_key'])

  scenario = ScenarioFacade(Settings.instance())

  scenario_response, status = scenario.show(kwargs.get('key'))
  if filter_response(scenario_response, status):
      sys.exit(1)

  if 'validate' in kwargs and len(kwargs['validate']):
      validate_aliases(kwargs['validate'], assign=kwargs['assign'], format=kwargs['format'], trace_id=kwargs['trace_id'])

  __assign_default_alias_resolve_strategy(kwargs)
  __assign_default_origin(kwargs)

  session: ReplaySession = {
      'buffer': kwargs['format'] and kwargs['format'] != DEFAULT_FORMAT,
      'contexts': [],
      'format': kwargs['format'],
      'scenario_id': scenario_key.id,
      'total': 0,
  }

  kwargs['before_replay'] = lambda context: handle_before_replay(
    context, session
  )
  kwargs['after_replay'] = lambda context: handle_after_replay(
      context, session
  )

  scenario.replay(kwargs.get('key'), kwargs)

  print_session(session)

def reset_handler(kwargs):
  scenario_key = kwargs['scenario_key']
  _scenario_key = validate_scenario_key(scenario_key)

  apply_service = Apply(force=kwargs['force']).with_logger(print)
  resetted = apply_service.scenario(_scenario_key.id)

  if not resetted:
    print('Successfully reset the scenario!')
  else:
    print('Could not reset the scenario.')

def show_handler(kwargs):
  print_options = select_print_options(kwargs)

  settings = Settings.instance()
  scenario_key = resolve_scenario_key_and_validate(kwargs, settings)
  scenario = ScenarioFacade(settings)

  scenario_response, status = scenario.show(scenario_key)
  if filter_response(scenario_response, status):
      sys.exit(1)

  print_scenarios([scenario_response], **print_options)

def snapshot_handler(kwargs):
  scenario_key = kwargs['scenario_key']
  del kwargs['scenario_key']

  validate_scenario_key(scenario_key)

  scenario = ScenarioFacade(Settings.instance())
  status = scenario.show(scenario_key)[1]

  if status == 404:
    print(f"Error: Could not find scenario", file=sys.stderr)
    sys.exit(1)

  response, status = scenario.snapshot(scenario_key, kwargs)

  if status != 200:
    print(f"Error: Could not snapshot scenario: {response}", file=sys.stderr)
    sys.exit(1)

  return response

def test_handler(kwargs: ScenarioTestOptions):
  os.environ[env_vars.LOG_LEVEL] = kwargs['log_level']
  Logger.reload()

  settings = Settings.instance()
  scenario_key = validate_scenario_key(kwargs['key'])

  if kwargs.get('remote_project_key'):
      validate_project_key(kwargs['remote_project_key'])

  if kwargs.get('report_key'):
      validate_report_key(kwargs['report_key'])
      kwargs['save'] = True # If report_key is set, then intention is to save results to the report

  if len(kwargs['validate']):
      validate_aliases(kwargs['validate'], assign=kwargs['assign'], format=kwargs['format'], trace_id=kwargs['trace_id'])

  __assign_default_alias_resolve_strategy(kwargs)
  __assign_default_origin(kwargs)

  session: ReplaySession = {
      'buffer': kwargs['format'] and kwargs['format'] != DEFAULT_FORMAT,
      'contexts': [],
      'format': kwargs['format'],
      'scenario_id': scenario_key.id,
      'total': 0,
  }

  session_context: SessionContext = { 
      'aggregate_failures': kwargs['aggregate_failures'], 
      'passed': 0, 
      'project_id': scenario_key.project_id,
      'skipped': 0, 
      'test_facade': TestFacade(settings), 
      'total': 0 
  }

  kwargs['before_replay'] = lambda context: handle_before_replay(
      context, session,
  )
  kwargs['after_replay'] = lambda context: __handle_on_test_response(
      context, session_context, kwargs
  )

  scenario = ScenarioFacade(settings)
  scenario.test(kwargs['key'], kwargs)

  handle_test_session_complete(session_context, format=kwargs['format'])

  exit_on_failure(session_context, format=kwargs['format'])

def __handle_on_test_response(replay_context: ReplayContext, session_context: SessionContext, kwargs):
    handle_test_complete(replay_context, session_context, format=kwargs['format'], output_level=kwargs['output_level'])

    if not session_context['aggregate_failures']:
        exit_on_failure(session_context, complete=False, format=kwargs['format'])

def __assign_default_alias_resolve_strategy(kwargs):
    # If we have assigned values to aliases, it's likely we want to also have them resolved
    if 'assign' in kwargs and len(kwargs['assign']) > 0 and kwargs['alias_resolve_strategy'] == alias_resolve_strategy.NONE:
        kwargs['alias_resolve_strategy'] = alias_resolve_strategy.FIFO

def __assign_default_origin(kwargs):
    if not kwargs.get('host'):
        kwargs['host'] = os.environ.get(env_vars.AGENT_REPLAY_HOST)

    if not kwargs.get('scheme'):
        kwargs['scheme'] = os.environ.get(env_vars.AGENT_REPLAY_SCHEME)

def diff_handler(kwargs):
  scenario_key = kwargs.get('scenario_key')
  full = kwargs.get('full', False)

  if scenario_key:
    resolved_scenario_key = validate_scenario_key(scenario_key)
    snapshot = ScenarioSnapshot(resolved_scenario_key.id)
    if not snapshot.exists:
      print('Error: Snapshot not found for this scenario.', file=sys.stderr)
      sys.exit(1)

    _print_scenario_diff(snapshot=snapshot, full=full, strict=True)
    return

  log = Log()
  visited_scenario_ids = set()
  for event in log.target_events:
    if event.action != PUT_ACTION:
      continue
    if event.resource != SCENARIO_RESOURCE:
      continue
    if event.resource_uuid in visited_scenario_ids:
      continue

    visited_scenario_ids.add(event.resource_uuid)
    snapshot = ScenarioSnapshot(event.resource_uuid)
    if not snapshot.exists:
      continue

    _print_scenario_diff(snapshot=snapshot, full=full, strict=False)

def _print_scenario_diff(snapshot: ScenarioSnapshot, full: bool, strict: bool):
  # Diff scenario metadata (name/description) if possible
  current_scenario = snapshot.find_resource()
  if not current_scenario:
    if strict:
      print('Error: Current scenario not found.', file=sys.stderr)
      sys.exit(1)
    return

  snapshot_meta = snapshot.metadata

  snapshot_name = snapshot_meta.get('name')
  snapshot_description = snapshot_meta.get('description')
  current_name = getattr(current_scenario, 'name', None)
  current_description = getattr(current_scenario, 'description', None)

  name_differs = (snapshot_name or '') != (current_name or '')
  description_differs = (snapshot_description or '') != (current_description or '')
  metadata_has_diff = name_differs or description_differs

  request_snapshots = []
  snapshot.iter_request_snapshots(lambda request_snapshot: request_snapshots.append(request_snapshot))

  request_analyses = []
  for request_snapshot in request_snapshots:
    current_request = request_snapshot.find_resource()
    if not current_request or not current_request.response:
      request_analyses.append((request_snapshot, None))
      continue
    request_analyses.append((request_snapshot, analyze_request_diff(request_snapshot, current_request)))

  snapshot_request_uuids = set([request_snapshot.uuid for request_snapshot in request_snapshots])
  current_requests = current_scenario.requests or []
  requests_missing_snapshot = list(filter(
    lambda request: request.uuid not in snapshot_request_uuids, current_requests
  ))

  has_any_diff = (
    metadata_has_diff
    or any(analysis and analysis.has_diff for _, analysis in request_analyses)
    or len(requests_missing_snapshot) > 0
  )
  if not has_any_diff:
    return

  try:
    scenario_key_str = current_scenario.key()
  except Exception:
    scenario_key_str = snapshot.uuid

  # Title line: inline colored diff for the scenario name when it changed; avoid repeating name in JSON below.
  print('=== Scenario ', end='')
  if name_differs:
    name_diff_text = diff_strings(str(snapshot_name or ''), str(current_name or '')).rstrip('\n')
    if '\n' in name_diff_text:
      name_diff_text = name_diff_text.replace('\n', ' ')
    print(name_diff_text, end='')
  else:
    print(current_name or snapshot_name or '', end='')
  print(f' {scenario_key_str}')
  print()

  if full:
    print('~ Description')
    print(diff_strings(str(snapshot_description or ''), str(current_description or '')))
    print()

  for _, analysis in request_analyses:
    if not analysis or not analysis.has_diff:
      continue
    emit_request_diff(analysis, full=full)

  for request in requests_missing_snapshot:
    emit_request_diff_header(
      request.url or "",
      request.key(),
      f"{bcolors.FAIL}No snapshot found{bcolors.ENDC}",
    )
