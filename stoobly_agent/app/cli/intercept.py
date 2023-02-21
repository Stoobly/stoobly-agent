import click
import pdb

from stoobly_agent.app.cli.decorators.config import ConfigDecorator
from stoobly_agent.app.settings import Settings
from stoobly_agent.config.constants import mode

settings = Settings.instance()
mode_options = [mode.MOCK, mode.RECORD, mode.REPLAY]

if settings.cli.features.remote:
    mode_options.append(mode.TEST)

@click.group(
    epilog="Run 'stoobly-agent intercept COMMAND --help' for more information on a command.",
    help="Manage request intercept"
)
@click.pass_context
def intercept(ctx):
    pass

@intercept.command(
    help="Enable intercept"
)
@click.option('--mode', type=click.Choice(mode_options))
def enable(**kwargs):
    settings = Settings.instance()

    if kwargs['mode']:
        settings.proxy.intercept.mode = kwargs['mode']

    settings.proxy.intercept.active = True

    settings.commit()

    print("Intercept enabled!")

@intercept.command(
    help="Disable intercept"
)
def disable(**kwargs):
    settings = Settings.instance()

    settings.proxy.intercept.active = False

    settings.commit()

    print("Intercept disabled!")

@intercept.command(
    help="Show intercept"
)
def show(**kwargs):
    settings = Settings.instance()

    mode = settings.proxy.intercept.mode

    if not mode:
        print('No intercept mode set')
    else:
        print(f"{mode.capitalize()} {'enabled' if settings.proxy.intercept.active else 'disabled'}")