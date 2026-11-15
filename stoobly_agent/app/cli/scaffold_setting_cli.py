import click
import sys

from stoobly_agent.app.cli.scaffold.app import App
from stoobly_agent.app.cli.scaffold.settings_init_manager import (
  build_init_path,
  build_setting_command,
  prepend_or_append_setting_command,
)
from stoobly_agent.app.cli.validators.scaffold import validate_hostname
from stoobly_agent.app.settings.constants import filter_action, request_component
from stoobly_agent.config.constants import mode


def _validate_app(app: App):
  try:
    app.valid
  except ValueError as e:
    click.echo(f"Error: {e}", err=True)
    sys.exit(1)


def _apply_setting_command(subgroup: str, kwargs: dict):
  workflows = kwargs.get('workflow') or ()
  if not workflows:
    click.echo("Error: Missing option '--workflow'", err=True)
    sys.exit(1)

  app = App(kwargs.get('app_dir_path'))
  _validate_app(app)

  command = build_setting_command(subgroup, kwargs)

  for workflow_name in workflows:
    init_path = build_init_path(app.app_data_dir.path, workflow_name)
    prepend_or_append_setting_command(init_path, command)
    click.echo(f"Updated {init_path}")


@click.group(
  epilog="Run 'stoobly-agent scaffold setting COMMAND --help' for more information on a command.",
  help="Manage scaffold settings written to build workflow init scripts"
)
@click.pass_context
def setting(ctx):
  pass


@click.group(
  help="Manage rewrite rules"
)
@click.pass_context
def rewrite(ctx):
  pass


@rewrite.command(
  'set',
  help="Set rewrite rule."
)
@click.option('--app-dir-path', default=None, help='Path to application directory.')
@click.option('--hostname', callback=validate_hostname, help='Request URL hostname.')
@click.option(
  '--method',
  multiple=True,
  required=True,
  type=click.Choice(['GET', 'POST', 'DELETE', 'OPTIONS', 'PUT', 'PATCH']),
  help='HTTP methods.'
)
@click.option(
  '--mode',
  multiple=True,
  required=True,
  type=click.Choice([mode.MOCK, mode.RECORD, mode.TEST, mode.DEVELOP])
)
@click.option('--name', help='Name of the request component.')
@click.option('--path', help='Request URL path to rewrite to.')
@click.option('--pattern', required=True, help='URLs to rewrite.')
@click.option('--port', type=click.IntRange(1, 65535), help='Request URL port to rewrite to.')
@click.option(
  '--type',
  type=click.Choice([
    request_component.BODY_PARAM,
    request_component.HEADER,
    request_component.QUERY_PARAM,
    request_component.RESPONSE_HEADER,
    request_component.RESPONSE_PARAM,
  ]),
  help='Request component type.'
)
@click.option(
  '--scheme',
  type=click.Choice(['http', 'https']),
  help='Request URL scheme to rewrite to.'
)
@click.option('--value', help='Rewrite value.')
@click.option('--workflow', multiple=True, required=True, help='Workflow(s) whose build init script to update.')
def rewrite_set(**kwargs):
  if kwargs['name'] or kwargs['value'] or kwargs['type']:
    if kwargs['name'] is None:
      print("Error: Missing option '--name'", file=sys.stderr)
      sys.exit(1)

    if kwargs['value'] is None:
      print("Error: Missing option '--value'", file=sys.stderr)
      sys.exit(1)

    if kwargs['type'] is None:
      print("Error: Missing option '--type'", file=sys.stderr)
      sys.exit(1)

  _apply_setting_command('rewrite', kwargs)


@click.group(
  help="Manage match rules"
)
@click.pass_context
def match(ctx):
  pass


@match.command(
  'set',
  help="Set match rule"
)
@click.option('--app-dir-path', default=None, help='Path to application directory.')
@click.option(
  '--component',
  multiple=True,
  type=click.Choice([request_component.BODY_PARAM, request_component.HEADER, request_component.QUERY_PARAM]),
  help='Request component type.'
)
@click.option(
  '--method',
  multiple=True,
  required=True,
  type=click.Choice(['GET', 'POST', 'DELETE', 'OPTIONS', 'PUT', 'PATCH']),
  help='HTTP methods.'
)
@click.option(
  '--mode',
  multiple=True,
  required=True,
  type=click.Choice([mode.MOCK, mode.TEST])
)
@click.option('--pattern', required=True, help='URLs pattern.')
@click.option('--workflow', multiple=True, required=True, help='Workflow(s) whose build init script to update.')
def match_set(**kwargs):
  _apply_setting_command('match', kwargs)


@click.group(
  'filter',
  help="Manage filter rules"
)
@click.pass_context
def _filter(ctx):
  pass


@_filter.command(
  'set',
  help="Set filter rule."
)
@click.option('--app-dir-path', default=None, help='Path to application directory.')
@click.option(
  '--action',
  required=True,
  type=click.Choice([filter_action.EXCLUDE, filter_action.INCLUDE]),
  help='Action to take on match.'
)
@click.option(
  '--method',
  multiple=True,
  required=True,
  type=click.Choice(['GET', 'POST', 'DELETE', 'OPTIONS', 'PUT', 'PATCH']),
  help='HTTP methods.'
)
@click.option(
  '--mode',
  multiple=True,
  required=True,
  type=click.Choice([mode.MOCK, mode.RECORD, mode.TEST, mode.DEVELOP])
)
@click.option('--pattern', required=True, help='URLs pattern.')
@click.option('--workflow', multiple=True, required=True, help='Workflow(s) whose build init script to update.')
def filter_set(**kwargs):
  _apply_setting_command('filter', kwargs)


setting.add_command(_filter)
setting.add_command(match)
setting.add_command(rewrite)
