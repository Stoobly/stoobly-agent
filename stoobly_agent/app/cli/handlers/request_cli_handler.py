import os
import pdb
import requests
import sys

from stoobly_agent.app.cli.helpers.handle_replay_service import DEFAULT_FORMAT, handle_before_replay, handle_after_replay, print_session, ReplaySession
from stoobly_agent.app.cli.helpers.handle_test_service import SessionContext, exit_on_failure, handle_test_complete, handle_test_session_complete
from stoobly_agent.app.cli.helpers.test_facade import TestFacade
from stoobly_agent.app.models.helpers.apply import Apply
from stoobly_agent.app.proxy.replay.body_parser_service import decode_response
from stoobly_agent.app.settings import Settings
from stoobly_agent.config.constants import alias_resolve_strategy, env_vars
from stoobly_agent.lib.api.keys.request_key import InvalidRequestKey
from stoobly_agent.lib.utils import jmespath

from ..helpers.print_service import print_requests, select_print_options
from ..helpers.request_facade import RequestFacade
from ..helpers.validations import *
from ..types.request import RequestTestOptions

def delete_handler(kwargs):
  validate_request_key(kwargs['request_key'])

  request = RequestFacade(Settings.instance())
  res, status = request.show(kwargs['request_key'], {})

  if filter_response(res, status):
    sys.exit(1)

  is_deleted = res.get('is_deleted')
  if not res:
    print(f"Error: Could not find request", file=sys.stderr)
    sys.exit(1)

  res = request.delete(kwargs['request_key'])
  if not res:
    print('Error: Could not delete request', file=sys.stderr)
    sys.exit(1)

  if not is_deleted:
    print('Request moved to trash!')
  else:
    print('Request deleted!')

def get_handler(kwargs):
  validate_request_key(kwargs['request_key'])

  request = RequestFacade(Settings.instance())
  res = __replay(request.mock, kwargs)

  print(res.text)

def list_handler(kwargs):
  print_options = select_print_options(kwargs)

  settings = Settings.instance()
  project_key = None

  if kwargs.get('is_remote'):
    project_key = resolve_project_key_and_validate(kwargs, settings)
    del kwargs['project_key']

  if kwargs.get('scenario_key'):
    validate_scenario_key(kwargs['scenario_key'])

  if kwargs.get('search'):
    kwargs['q'] = kwargs['search']
    del kwargs['search']

  request = RequestFacade(settings)
  requests_response, status = request.index(project_key, kwargs)

  if filter_response(requests_response, status):
    sys.exit(1)

  if not requests_response or len(requests_response['list']) == 0:
    print('No requests found.')
  else:
    print_requests(requests_response['list'], **print_options)

def query_handler(kwargs):
  validate_request_key(kwargs['request_key'])

  request = RequestFacade(Settings.instance())
  res = __replay(request.mock, kwargs)

  content = res.content
  content_type = res.headers.get('content-type')
  decoded_response = decode_response(content, content_type)

  print(jmespath.search(kwargs['query'], decoded_response))

def replay_handler(kwargs):
  os.environ[env_vars.LOG_LEVEL] = kwargs['log_level']

  validate_request_key(kwargs['request_key'])

  if kwargs.get('scenario_key'):
    if not kwargs.get('record'):
      print("Error: Missing option '--record'.", file=sys.stderr)
      sys.exit(1)

    validate_scenario_key(kwargs['scenario_key'])

  if 'validate' in kwargs and len(kwargs['validate']):
      validate_aliases(kwargs['validate'], assign=kwargs['assign'], format=kwargs['format'], trace_id=kwargs['trace_id'])

  __assign_default_alias_resolve_strategy(kwargs)
  __assign_default_origin(kwargs)

  session: ReplaySession = {
    'buffer': kwargs['format'] and kwargs['format'] != DEFAULT_FORMAT,
    'contexts': [],
    'format': kwargs['format'],
    'total': 0,
  }
  
  kwargs['before_replay'] = lambda context: handle_before_replay(context, session)
  kwargs['after_replay'] = lambda context: handle_after_replay(context, session)
  
  request = RequestFacade(Settings.instance())
  __replay(request.replay, kwargs)

  print_session(session)

def reset_handler(kwargs):
  request_key = kwargs['request_key']
  _request_key = validate_request_key(request_key)

  apply_service = Apply(force=kwargs['force']).with_logger(print)
  resetted = apply_service.request(_request_key.id)

  if not resetted:
    print('Successfully reset the request!')
  else:
    print('Could not reset the request.')

def snapshot_handler(kwargs):
  request_key = kwargs['request_key']
  del kwargs['request_key']

  validate_request_key(request_key)

  request = RequestFacade(Settings.instance())
  request.snapshot(request_key, kwargs)

def test_handler(kwargs: RequestTestOptions):
  os.environ[env_vars.LOG_LEVEL] = kwargs['log_level']

  settings = Settings.instance()
  request_key = validate_request_key(kwargs['request_key'])

  if kwargs.get('remote_project_key'):
    validate_project_key(kwargs['remote_project_key'])

  if kwargs.get('report_key'):
    if not kwargs.get('save'):
      print("Error: Missing --save option", file=sys.stderr)
      sys.exit(1)

    validate_report_key(kwargs['report_key'])

  if len(kwargs['validate']):
    validate_aliases(kwargs['validate'], assign=kwargs['assign'], format=kwargs['format'], trace_id=kwargs['trace_id'])

  __assign_default_alias_resolve_strategy(kwargs)
  __assign_default_origin(kwargs)

  session: ReplaySession = {
    'buffer': kwargs['format'] and kwargs['format'] != DEFAULT_FORMAT,
    'contexts': [],
    'format': kwargs['format'],
    'total': 0,
  }

  session_context: SessionContext = { 
      'aggregate_failures': kwargs['aggregate_failures'], 
      'passed': 0, 
      'project_id': request_key.project_id, 
      'skipped': 0,
      'test_facade': TestFacade(settings), 
      'total': 0 
  }

  kwargs['before_replay'] = lambda context: handle_before_replay(
    context, session
  )

  kwargs['after_replay'] = lambda context: handle_test_complete(
    context, session_context, format=kwargs['format'], output_level=kwargs['output_level']
  )

  request = RequestFacade(settings)
  __replay(request.test, kwargs)

  handle_test_session_complete(session_context, format=kwargs['format'])

  exit_on_failure(session_context, format=kwargs['format'])

def __replay(handler, kwargs) -> requests.Response:
  request_key = kwargs['request_key']
  del kwargs['request_key']

  try:
    return handler(request_key, kwargs) 
  except InvalidRequestKey:
    print('Error: Invalid request key.', file=sys.stderr)
    sys.exit(1)

def __assign_default_alias_resolve_strategy(kwargs):
    # If we have assigned values to aliases, it's likely we want to also have them resolved
    if 'assign' in kwargs and len(kwargs['assign']) > 0 and kwargs['alias_resolve_strategy'] == alias_resolve_strategy.NONE:
        kwargs['alias_resolve_strategy'] = alias_resolve_strategy.FIFO

def __assign_default_origin(kwargs):
    if not kwargs.get('host'):
        kwargs['host'] = os.environ.get(env_vars.AGENT_REPLAY_HOST)

    if not kwargs.get('scheme'):
        kwargs['scheme'] = os.environ.get(env_vars.AGENT_REPLAY_SCHEME)