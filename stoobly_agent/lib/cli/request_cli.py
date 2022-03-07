import click
import requests

from stoobly_agent.lib.intercept_handler.constants import modes, test_strategies

from ..settings import Settings
from .request_facade import RequestFacade

@click.group()
@click.pass_context
def request(ctx):
    pass

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