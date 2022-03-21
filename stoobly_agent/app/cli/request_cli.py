import click
import pdb
import requests

from stoobly_agent.config.constants import mode
from stoobly_agent.app.settings import Settings

from .request_facade import RequestFacade
from .utils.tabulate_print_service import tabulate_print

@click.group()
@click.pass_context
def request(ctx):
    pass

@request.command()
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

@request.command()
@click.option('--report-key')
@click.option('--scenario-key')
@click.argument('request_key')
def replay(**kwargs):
  request = RequestFacade(Settings.instance())
  __replay(request.replay, **kwargs)
  
@request.command()
@click.option('--report-key')
@click.option('--scenario-key')
@click.argument('request_key')
def record(**kwargs):
  request = RequestFacade(Settings.instance())
  __replay(request.record, **kwargs)

@request.command()
@click.option('--report-key')
@click.option('--scenario-key')
@click.argument('request_key')
def mock(**kwargs):
  request = RequestFacade(Settings.instance())
  __replay(request.mock, **kwargs)

@request.command()
@click.option('--report-key')
@click.option('--scenario-key')
@click.argument('request_key')
def test(**kwargs):
  request = RequestFacade(Settings.instance())
  __replay(request.test, **kwargs)

def __replay(handler, **kwargs):
  request_key = kwargs['request_key']
  del kwargs['request_key']

  res: requests.Response = handler(request_key, **kwargs)   
  print(res.content)