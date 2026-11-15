import click
import sys

from stoobly_agent.app.cli.scaffold.app import App
from stoobly_agent.app.cli.scaffold.settings_init_manager import (
  build_init_path,
  build_intercept_command,
  prepend_or_append_intercept_command,
  resolve_workflows,
)
from stoobly_agent.config.constants import (
  mode,
  mock_policy,
  develop_policy,
  record_order,
  record_policy,
  record_strategy,
  test_policy,
  test_strategy,
)


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


_POLICY_OPTIONS = sorted({
  mock_policy.ALL,
  mock_policy.FOUND,
  mock_policy.NONE,
  record_policy.ALL,
  record_policy.API,
  record_policy.FOUND,
  record_policy.NOT_FOUND,
  develop_policy.ALL,
  test_policy.FOUND,
  test_policy.NONE,
})

_STRATEGY_OPTIONS = sorted({
  record_strategy.FULL,
  record_strategy.MINIMAL,
  test_strategy.CONTRACT,
  test_strategy.CUSTOM,
  test_strategy.DIFF,
  test_strategy.FUZZY,
})

_ORDER_OPTIONS = [record_order.APPEND, record_order.OVERWRITE]


@intercept.command(
  help="Set intercept options"
)
@click.option('--app-dir-path', default=None, help='Path to application directory.')
@click.option('--mode', type=click.Choice(mode.options), help='Intercept mode.')
@click.option(
  '--order',
  type=click.Choice(_ORDER_OPTIONS),
  help=f"Order to use for recording. Valid options: {_ORDER_OPTIONS}",
)
@click.option(
  '--policy',
  type=click.Choice(_POLICY_OPTIONS),
  help=f"Policy to use for intercept. Valid options: {_POLICY_OPTIONS}",
)
@click.option(
  '--strategy',
  type=click.Choice(_STRATEGY_OPTIONS),
  help=f"Strategy to use for intercept. Valid options: {_STRATEGY_OPTIONS}",
)
@click.option('--workflow', multiple=True, help='Workflow(s) whose build init script to update. Defaults to all.')
def set(**kwargs):
  if not kwargs['mode'] and not kwargs['order'] and not kwargs['policy'] and not kwargs['strategy']:
    click.echo("Error: Missing an option", err=True)
    sys.exit(1)

  _apply_intercept_command('set', kwargs)
