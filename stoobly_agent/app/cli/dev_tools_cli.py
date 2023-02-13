import click
import pdb

from stoobly_agent import VERSION
from stoobly_agent.app.proxy.replay.body_parser_service import decode_response
from stoobly_agent.app.models.adapters.raw_http_response_adapter import RawHttpResponseAdapter
from stoobly_agent.lib.orm.migrate_service import migrate as database_migrate, rollback as database_rollback
from stoobly_agent.lib.orm.replayed_response import ReplayedResponse
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.lib.orm.response import Response
from stoobly_agent.lib.orm.scenario import Scenario
from stoobly_agent.lib.orm.trace import Trace
from stoobly_agent.lib.orm.trace_alias import TraceAlias
from stoobly_agent.lib.orm.trace_request import TraceRequest
from stoobly_agent.lib.utils import jmespath

@click.group(
  epilog="Run 'stoobly-agent dev-tools COMMAND --help' for more information on a command.",
  help="Access developer tools"
)
@click.pass_context
def dev_tools(ctx):
    pass

@dev_tools.command()
def debug(**kwargs):
  pdb.set_trace()

@dev_tools.command()
def migrate():
  database_migrate(VERSION)

@dev_tools.command()
def rollback():
  database_rollback()

@dev_tools.command()
@click.option('--content')
@click.option('--content-type', default='application/json')
@click.argument('query')
def query(**kwargs):
  decoded_response = decode_response(kwargs['content'], kwargs['content_type'])
  print(jmespath.search(kwargs['query'], decoded_response))