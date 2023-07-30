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
@click.option('--force', default=False, help="Toggles whether resources are hard deleted.")
@click.argument('uuid', required=False)
def apply(**kwargs):
  apply = Apply(force=kwargs['force']).with_logger(print)

  if kwargs.get('uuid'):
    apply.single(kwargs['uuid'])
  else:
    apply.all()

