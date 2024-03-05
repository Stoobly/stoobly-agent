import os
import pdb
import sys

from stoobly_agent.app.cli.helpers.handle_replay_service import DEFAULT_FORMAT, handle_before_replay, handle_after_replay, print_session, ReplaySession
from stoobly_agent.app.cli.helpers.handle_test_service import SessionContext, exit_on_failure, handle_test_complete, handle_test_session_complete 
from stoobly_agent.app.cli.helpers.print_service import print_scenarios, select_print_options
from stoobly_agent.app.cli.helpers.test_facade import TestFacade
from stoobly_agent.app.cli.helpers.context import ReplayContext
from stoobly_agent.app.models.helpers.apply import Apply
from stoobly_agent.app.settings import Settings
from stoobly_agent.config.constants import alias_resolve_strategy, env_vars
from stoobly_agent.lib import logger

from ..helpers.scenario_facade import ScenarioFacade
from ..helpers.validations import *
from ..types.scenario import ScenarioTestOptions

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
  scenario.snapshot(scenario_key, kwargs)

def test_handler(kwargs: ScenarioTestOptions):
  os.environ[env_vars.LOG_LEVEL] = kwargs['log_level']
  logger.Logger.reload()

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