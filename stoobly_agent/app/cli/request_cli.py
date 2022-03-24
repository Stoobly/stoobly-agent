import click
import pdb
import requests

from stoobly_agent.config.constants import test_strategy
from stoobly_agent.app.settings import Settings

from .request_facade import RequestFacade
from .utils.tabulate_print_service import tabulate_print

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
@click.option('--sort-by', default='created_at', help='created_at|path')
@click.option('--sort-order', default='desc', help='asc | desc')
@click.option('--size', default=10)
@click.argument('project_key', required=False)
def list(**kwargs):
  project_key = kwargs.get('project_key')
  del kwargs['project_key']

  request = RequestFacade(Settings.instance())
  requests_response = request.index(project_key, **kwargs)
  tabulate_print(requests_response['list'], filter=['created_at', 'project_id', 'starred', 'updated_at'])

@request.command(
  help="Replay a request"
)
@click.argument('request_key')
def replay(**kwargs):
  request = RequestFacade(Settings.instance())
  res = __replay(request.replay, **kwargs)
  print(res.content)
  
@request.command(
  help="Record a request"
)
@click.option('--scenario-key')
@click.argument('request_key')
def record(**kwargs):
  request = RequestFacade(Settings.instance())
  __replay(request.record, **kwargs)

@request.command(
  help="Test a request"
)
@click.option('--report-key')
@click.option('--strategy', default=test_strategy.DIFF, help=f"{test_strategy.CUSTOM} | {test_strategy.DIFF} | {test_strategy.FUZZY}")
@click.argument('request_key')
def test(**kwargs):
  request = RequestFacade(Settings.instance())
  __replay(request.test, **kwargs)

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
  request = RequestFacade(Settings.instance())
  res = __replay(request.mock, **kwargs)
  print(res.content)

@response.command(
  help="Set new mocked response"
)
def set(**kwargs):
  print("Not yet implemented. Stay tuned!")

request.add_command(response)

def __replay(handler, **kwargs) -> requests.Response:
  request_key = kwargs['request_key']
  del kwargs['request_key']

  return handler(request_key, **kwargs)   