import click
import pdb

from stoobly_agent.app.models.helpers.apply import Apply

@click.group(
    epilog="Run 'stoobly-agent project COMMAND --help' for more information on a command.",
    help="Manage snapshots"
)
@click.pass_context
def snapshot(ctx):
    pass

@snapshot.command(
  help="Apply snapshots"
)
@click.argument('uuid', required=False)
def apply(**kwargs):
  apply = Apply().with_logger(print)

  if kwargs.get('uuid'):
    apply.single(kwargs['uuid'])
  else:
    apply.all()

