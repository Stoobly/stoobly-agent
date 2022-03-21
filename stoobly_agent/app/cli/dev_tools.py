import click
import pdb

from stoobly_agent.lib.orm.request import Request
from stoobly_agent.lib.orm.response import Response
from stoobly_agent.app.cli.utils.migrate_service import migrate as database_migrate

@click.group()
@click.pass_context
def dev_tools(ctx):
    pass

@dev_tools.command()
def debug(**kwargs):
  pdb.set_trace()

@dev_tools.command()
def migrate():
  database_migrate()