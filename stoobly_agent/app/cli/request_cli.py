import click
import os
import pdb
import requests
import sys

from stoobly_agent.app.cli.helpers.handle_replay_service import BODY_FORMAT, DEFAULT_FORMAT, JSON_FORMAT, handle_before_replay, handle_after_replay, print_session, ReplaySession
from stoobly_agent.app.cli.helpers.handle_test_service import SessionContext, exit_on_failure, handle_test_complete, handle_test_session_complete
from stoobly_agent.app.cli.helpers.test_facade import TestFacade
from stoobly_agent.app.models.helpers.apply import Apply
from stoobly_agent.app.models.factories.resource.local_db.helpers.log_event import DELETE_ACTION, PUT_ACTION
from stoobly_agent.app.proxy.replay.body_parser_service import decode_response
from stoobly_agent.app.settings import Settings
from stoobly_agent.config.constants import alias_resolve_strategy, env_vars, test_filter, test_strategy
from stoobly_agent.lib import logger
from stoobly_agent.lib.api.keys.request_key import InvalidRequestKey
from stoobly_agent.lib.utils import jmespath
from stoobly_agent.lib.utils.conditional_decorator import ConditionalDecorator

from .helpers.feature_flags import local, remote
from .helpers.print_service import FORMATS, print_requests, select_print_options
from .helpers.request_facade import RequestFacade
from .helpers.validations import *

settings = Settings.instance()
is_remote = remote(settings)
is_local = local(settings) 

log_levels = [logger.DEBUG, logger.INFO, logger.WARNING, logger.ERROR]

@click.group(
  epilog="Run 'stoobly-agent request COMMAND --help' for more information on a command.",
  help="Manage requests"
)
@click.pass_context
def request(ctx):
    pass

@request.command(
  help="Delete recorded request"
)
@click.argument('request_key')
def delete(**kwargs):
  validate_request_key(kwargs['request_key'])

  request = RequestFacade(settings.instance())
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

@request.command(
  help="Show recorded requests"
)
@click.option('--format', type=click.Choice(FORMATS), help='Format output.')
@click.option('--page', default=0)
@ConditionalDecorator(lambda f: click.option('--project-key')(f), is_remote)
@click.option('--scenario-key')
@click.option('--search', help='Query to filter requests by.')
@click.option('--select', multiple=True, help='Select column(s) to display.')
@click.option('--sort-by', default='created_at', help='created_at|path')
@click.option('--sort-order', default='desc', help='asc | desc')
@click.option('--size', default=10)
@click.option('--without-headers', is_flag=True, default=False, help='Disable printing column headers.')
def list(**kwargs):
  print_options = select_print_options(kwargs)

  settings = Settings.instance()
  project_key = None

  if is_remote:
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

@request.command(
  help="Replay a request"
)
@ConditionalDecorator(lambda f: click.option(
    '--alias-resolve-strategy', 
    default=alias_resolve_strategy.NONE, 
    type=click.Choice([alias_resolve_strategy.NONE, alias_resolve_strategy.FIFO, alias_resolve_strategy.LIFO]), 
    help='Strategy for resolving dynamic values for aliases.'
)(f), is_remote)
@ConditionalDecorator(lambda f: click.option('--assign', multiple=True, help='Assign alias values. Format: <NAME>=<VALUE>')(f), is_remote)
@click.option('--format', type=click.Choice([BODY_FORMAT, JSON_FORMAT]), help='Format replay response.')
@click.option('--host', help='Rewrite request host.')
@ConditionalDecorator(lambda f: click.option('--group-by', help='Repeat for each alias name.')(f), is_remote)
@click.option('--lifecycle-hooks-path', help='Path to lifecycle hooks script.')
@click.option(
  '--log-level', default=logger.WARNING, type=click.Choice(log_levels), 
  help='''
    Log levels can be "debug", "info", "warning", or "error"
  '''
)
@ConditionalDecorator(
  lambda f: click.option(
    '--overwrite', is_flag=True, default=False, help='Replay request and overwrite existing response.'
  )(f), not is_remote
)
@click.option('--record', is_flag=True, default=False, help='Replay request and record.')
@ConditionalDecorator(lambda f: click.option('--save', is_flag=True, default=False, help='Replay request and save to history.')(f), is_remote)
@click.option('--scenario-key', help='Record to scenario.')
@click.option('--scheme', type=click.Choice(['http', 'https']), help='Rewrite request scheme.')
@ConditionalDecorator(lambda f: click.option('--trace-id', help='Use existing trace.')(f), is_remote)
@ConditionalDecorator(lambda f: click.option('--validate', multiple=True, help='Validate one or more aliases. Format: <NAME>=?<TYPE>')(f), is_remote)
@click.argument('request_key')
def replay(**kwargs):
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

if not is_remote:
  @request.command(
    help="Snapshot a request"
  )
  @click.option('--action', default=PUT_ACTION, type=click.Choice([DELETE_ACTION, PUT_ACTION]), help='Sets snapshot action.')
  @click.option('--decode', default=False, is_flag=True, help="Toggles whether to decode response body.")
  @click.argument('request_key')
  def snapshot(**kwargs):
    request_key = kwargs['request_key']
    del kwargs['request_key']

    validate_request_key(request_key)

    request = RequestFacade(Settings.instance())
    res = request.snapshot(request_key, kwargs)

  @request.command(
      help="Reset a request to its snapshot state"
  )
  @click.option('--force', default=False, is_flag=True, help="Toggles whether request are hard deleted.")
  @click.argument('request_key')
  def reset(**kwargs):
    request_key = kwargs['request_key']
    _request_key = validate_request_key(request_key)

    apply_service = Apply(force=kwargs['force']).with_logger(print)
    resetted = apply_service.request(_request_key.id)

    if not resetted:
      print('Successfully reset the request!')
    else:
      print('Could not reset the request.')

@request.command(
  help="Test a request"
)
@click.option(
    '--alias-resolve-strategy', 
    default=alias_resolve_strategy.NONE, 
    type=click.Choice([alias_resolve_strategy.NONE, alias_resolve_strategy.FIFO, alias_resolve_strategy.LIFO]), 
    help='Strategy for resolving dynamic values for aliases.'
)
@click.option('--aggregate-failures', default=False, is_flag=True, help='Toggles whether to continue execution on failure.')
@click.option('--assign', multiple=True, help='Assign alias values. Format: <NAME>=<VALUE>')
@click.option('--filter', default=test_filter.ALL, type=click.Choice([test_filter.ALL, test_filter.ALIAS, test_filter.LINK]), help='For iterable responses, selectively test properties.')
@click.option('--format', type=click.Choice([BODY_FORMAT, JSON_FORMAT]), help='Format replay response.')
@click.option('--group-by', help='Repeat for each alias name.')
@click.option('--host', help='Rewrite request host.')
@click.option('--lifecycle-hooks-path', help='Path to lifecycle hooks script.')
@click.option(
    '--log-level', default=logger.WARNING, type=click.Choice(log_levels), 
    help='''
        Log levels can be "debug", "info", "warning", or "error"
    '''
)
@ConditionalDecorator(lambda f: click.option('--remote-project-key', help='Use remote project for endpoint definitions.')(f), is_remote and is_local)
@ConditionalDecorator(lambda f: click.option('--report-key', help='Save to report.')(f), is_remote)
@ConditionalDecorator(lambda f: click.option('--save', is_flag=True, default=False, help='Saves test results.')(f), is_remote)
@click.option('--scheme', type=click.Choice(['http', 'https']), help='Rewrite request scheme.')
@click.option('--strategy', default=test_strategy.DIFF, type=click.Choice([test_strategy.CONTRACT, test_strategy.CUSTOM, test_strategy.DIFF, test_strategy.FUZZY]), help='How to test responses.')
@click.option('--trace-id', help='Use existing trace.')
@click.option('--validate', multiple=True, help='Validate one or more aliases. Format: <NAME>=?<TYPE>')
@click.argument('request_key')
def test(**kwargs):
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
      'test_facade': TestFacade(settings), 
      'total': 0 
  }

  kwargs['before_replay'] = lambda context: handle_before_replay(
    context, session
  )

  kwargs['after_replay'] = lambda context: handle_test_complete(
    context, session_context, format=kwargs['format']
  )

  request = RequestFacade(settings)
  __replay(request.test, kwargs)

  handle_test_session_complete(session_context, format=kwargs['format'])

  exit_on_failure(session_context, format=kwargs['format'])

@click.group(
  epilog="Run 'stoobly-agent request response COMMAND --help' for more information on a command.",
  help="Manage request responses"
)
@click.pass_context
def response(ctx):
    pass

@response.command(
  help="Retrieve mocked response"
)
@click.argument('request_key')
def get(**kwargs) -> None:
  validate_request_key(kwargs['request_key'])

  request = RequestFacade(Settings.instance())
  res = __replay(request.mock, kwargs)

  print(res.text)

@response.command(
  help="Query properties in response"
)
@click.option('--query', required=True)
@click.argument('request_key')
def query(**kwargs):
  validate_request_key(kwargs['request_key'])

  request = RequestFacade(Settings.instance())
  res = __replay(request.mock, kwargs)

  content = res.content
  content_type = res.headers.get('content-type')
  decoded_response = decode_response(content, content_type)

  print(jmespath.search(kwargs['query'], decoded_response))

request.add_command(response)

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

