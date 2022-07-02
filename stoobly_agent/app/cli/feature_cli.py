import click

from stoobly_agent.app.settings import Settings

from .decorators.config import ConfigDecorator

settings = Settings.instance()

@click.group(
  epilog="Run 'stoobly-agent feature COMMAND --help' for more information on a command.",
  help="Manage features"
)
@click.pass_context
def feature(ctx):
    pass

@click.group(
  epilog="Run 'stoobly-agent dev_tools COMMAND --help' for more information on a command.",
  help="Toggle whether dev-tools command is enabled",
)
@click.pass_context
def dev_tools(ctx):
  pass

ConfigDecorator(dev_tools, settings, 'cli.features.dev_tools').decorate()

feature.add_command(dev_tools)

@click.group(
  epilog="Run 'stoobly-agent exec COMMAND --help' for more information on a command.",
  help="Toggle whether exec command is enabled.",
)
@click.pass_context
def exec(ctx):
  pass

ConfigDecorator(exec, settings, 'cli.features.exec').decorate()

feature.add_command(exec)

@click.group(
  epilog="Run 'stoobly-agent remote COMMAND --help' for more information on a command.",
  help="Toggle whether local or remote storage is used."
)
@click.pass_context
def remote(ctx):
  pass

def __handle_enable_before_action():
  api_key = settings.remote.api_key
  if not api_key or len(api_key) == 0:
    api_key = click.prompt('Please enter your API key', type=str)
    settings.remote.api_key = api_key

ConfigDecorator(remote, settings, 'cli.features.remote', {
  'enable': {
    'before_action': __handle_enable_before_action
  }
}).decorate()

feature.add_command(remote)