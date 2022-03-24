import click

from stoobly_agent.app.settings import Settings

from .decorators.config import ConfigDecorator

settings = Settings.instance()

@click.group()
@click.pass_context
def feature(ctx):
    pass

@click.group()
@click.pass_context
def dev_tools(ctx):
  pass

ConfigDecorator(dev_tools, settings, 'features.dev_tools').decorate()

feature.add_command(dev_tools)


@click.group()
@click.pass_context
def exec(ctx):
  pass

ConfigDecorator(exec, settings, 'features.exec').decorate()

feature.add_command(exec)