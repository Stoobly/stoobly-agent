import click
import pdb
import requests
import sys

from stoobly_agent.app.cli.helpers.handle_test_service import SessionContext, exit_on_failure, handle_on_test_response, print_request
from stoobly_agent.app.cli.helpers.print_service import select_print_options
from stoobly_agent.app.cli.helpers.test_facade import TestFacade
from stoobly_agent.app.settings import Settings
from stoobly_agent.config.constants import test_filter, test_strategy
from stoobly_agent.lib.api.keys.request_key import InvalidRequestKey
from stoobly_agent.lib.utils.conditional_decorator import ConditionalDecorator

from .helpers.print_service import print_requests
from .helpers.request_facade import RequestFacade
from .helpers.validations import *

settings = Settings.instance()
is_remote = settings.cli.features.remote

@click.group(
  epilog="Run 'stoobly-agent request COMMAND --help' for more information on a command.",
  help="Manage requests"
)
@click.pass_context
def request(ctx):
    pass

@request.command(
  help="Show recorded requests"
)
@click.option('--page', default=0)
@ConditionalDecorator(lambda f: click.option('--project-key')(f), is_remote)
@ConditionalDecorator(lambda f: click.option('--scenario-key')(f), is_remote)
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

  request = RequestFacade(settings)
  requests_response = request.index(project_key, kwargs)

  if not requests_response or len(requests_response['list']) == 0:
    print('No requests found.')
  else:
    print_requests(requests_response['list'], **print_options)

@request.command(
  help="Replay a request"
)
@click.option('--assign', multiple=True, help='Assign alias values. Format: <NAME>=<VALUE>')
@click.option('--group-by', help='Repeat for each alias name.')
@click.option('--lifecycle-hooks-script-path', help='Path to lifecycle hooks script.')
@click.option('--record', is_flag=True, default=False, help='Replay and record request.')
@ConditionalDecorator(lambda f: click.option('--scenario-key', help='Record to scenario.')(f), is_remote)
@click.option('--trace-id', help='Use existing trace.')
@click.argument('request_key')
def replay(**kwargs):
  validate_request_key(kwargs['request_key'])

  if kwargs.get('scenario_key'):
    if not kwargs.get('record'):
      print("Error: Missing option '--record'.", file=sys.stderr)
      sys.exit(1)

    validate_scenario_key(kwargs['scenario_key'])

  kwargs['on_response'] = print_request

  request = RequestFacade(Settings.instance())
  __replay(request.replay, kwargs)

if is_remote:
  @request.command(
    help="Test a request"
  )
  @click.option('--aggregate-failures', default=False, is_flag=True, help='Toggles whether to continue execution on failure.')
  @click.option('--assign', multiple=True, help='Assign alias values. Format: <NAME>=<VALUE>')
  @click.option('--filter', default=test_filter.ALL, type=click.Choice([test_filter.ALL, test_filter.ALIAS, test_filter.LINK]), help='For iterable responses, selectively test properties.')
  @click.option('--group-by', help='Repeat for each alias name.')
  @click.option('--lifecycle-hooks-script-path', help='Path to lifecycle hooks script.')
  @click.option('--report-key', help='Save to report.')
  @click.option('--strategy', default=test_strategy.DIFF, type=click.Choice([test_strategy.CUSTOM, test_strategy.DIFF, test_strategy.FUZZY]), help='How to test responses.')
  @click.option('--trace-id', help='Use existing trace.')
  @click.argument('request_key')
  def test(**kwargs):
    settings = Settings.instance()
    request_key = validate_request_key(kwargs['request_key'])

    if kwargs.get('report_key'):
      validate_report_key(kwargs['report_key'])

    session_context: SessionContext = { 
        'aggregate_failures': kwargs['aggregate_failures'], 
        'passed': 0, 
        'project_id': request_key.project_id, 
        'test_facade': TestFacade(settings), 
        'total': 0 
    }
    kwargs['on_response'] = lambda context: handle_on_test_response(
      context, session_context
    )

    request = RequestFacade(settings)
    __replay(request.test, kwargs)

    exit_on_failure(session_context)

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
def get(**kwargs):
  validate_request_key(kwargs['request_key'])

  request = RequestFacade(Settings.instance())
  res = __replay(request.mock, kwargs)

  print(res.content)

@response.command(
  help="Set new mocked response"
)
def set(**kwargs):
  print("Not yet implemented. Stay tuned!")

request.add_command(response)

def __replay(handler, kwargs) -> requests.Response:
  request_key = kwargs['request_key']
  del kwargs['request_key']

  try:
    return handler(request_key, kwargs) 
  except InvalidRequestKey:
    print('Error: Invalid request key.', file=sys.stderr)
    sys.exit(1)