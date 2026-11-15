import click
import sys

from stoobly_agent.app.cli.helpers.intercept_options import (
  ORDER_OPTIONS,
  POLICY_OPTIONS,
  STRATEGY_OPTIONS,
  validate_options_for_mode,
)
from stoobly_agent.app.cli.scaffold.app import App
from stoobly_agent.app.cli.scaffold.settings_init_manager import (
  build_init_path,
  build_intercept_command,
  prepend_or_append_intercept_command,
  resolve_workflows,
)
from stoobly_agent.config.constants import mode


def _validate_app(app: App):
  try:
    app.valid
  except ValueError as e:
    click.echo(f"Error: {e}", err=True)
    sys.exit(1)


def _apply_intercept_command(subcommand: str, kwargs: dict):
  app = App(kwargs.get('app_dir_path'))
  _validate_app(app)

  workflows = resolve_workflows(app.app_data_dir.path, kwargs.get('workflow'))
  if not workflows:
    click.echo("Error: No build workflow init scripts found", err=True)
    sys.exit(1)

  command = build_intercept_command(subcommand, kwargs)

  for workflow_name in workflows:
    init_path = build_init_path(app.app_data_dir.path, workflow_name)
    prepend_or_append_intercept_command(init_path, command)
    click.echo(f"Updated {init_path}")


@click.group(
  epilog="Run 'stoobly-agent scaffold intercept COMMAND --help' for more information on a command.",
  help="Manage scaffold intercept written to build workflow init scripts"
)
@click.pass_context
def intercept(ctx):
  pass


@intercept.command(
  help="Enable intercept"
)
@click.option('--app-dir-path', default=None, help='Path to application directory.')
@click.option('--workflow', multiple=True, help='Workflow(s) whose build init script to update. Defaults to all.')
def enable(**kwargs):
  _apply_intercept_command('enable', kwargs)


@intercept.command(
  help="Disable intercept"
)
@click.option('--app-dir-path', default=None, help='Path to application directory.')
@click.option('--workflow', multiple=True, help='Workflow(s) whose build init script to update. Defaults to all.')
def disable(**kwargs):
  _apply_intercept_command('disable', kwargs)


@intercept.command(
  help="Set intercept options"
)
@click.option('--app-dir-path', default=None, help='Path to application directory.')
@click.option('--mode', type=click.Choice(mode.options), help='Intercept mode.')
@click.option(
  '--order',
  type=click.Choice(ORDER_OPTIONS),
  help=f"Order to use for recording. Valid options: {ORDER_OPTIONS}",
)
@click.option(
  '--policy',
  type=click.Choice(POLICY_OPTIONS),
  help=f"Policy to use for intercept. Valid options: {POLICY_OPTIONS}",
)
@click.option(
  '--strategy',
  type=click.Choice(STRATEGY_OPTIONS),
  help=f"Strategy to use for intercept. Valid options: {STRATEGY_OPTIONS}",
)
@click.option('--workflow', multiple=True, help='Workflow(s) whose build init script to update. Defaults to all.')
def set(**kwargs):
  if not kwargs['mode'] and not kwargs['order'] and not kwargs['policy'] and not kwargs['strategy']:
    click.echo("Error: Missing an option", err=True)
    sys.exit(1)

  validate_options_for_mode(kwargs)

  _apply_intercept_command('set', kwargs)
