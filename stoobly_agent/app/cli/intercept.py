import click
import pdb

from stoobly_agent.app.cli.decorators.config import ConfigDecorator
from stoobly_agent.app.settings import Settings

settings = Settings.instance()

@click.group(
    epilog="Run 'stoobly-agent intercept COMMAND --help' for more information on a command.",
    help="Toggle request intercept"
)
@click.pass_context
def intercept(ctx):
    pass

ConfigDecorator(intercept, settings, 'proxy.intercept.active').decorate()