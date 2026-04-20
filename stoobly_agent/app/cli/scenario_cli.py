import sys

import click

from stoobly_agent.app.cli.helpers.handle_replay_service import JSON_FORMAT
from stoobly_agent.app.cli.helpers.print_service import FORMATS, print_snapshots, select_print_options
from stoobly_agent.app.cli.helpers.snapshot_list_service import list_snapshots, snapshot_list_options
from stoobly_agent.app.cli.helpers.update_request_snapshots_service import update_request_snapshots
from stoobly_agent.app.models.factories.resource.local_db.helpers.log_event import DELETE_ACTION, PUT_ACTION, SCENARIO_RESOURCE
from stoobly_agent.app.settings import Settings
from stoobly_agent.config.constants import alias_resolve_strategy, test_filter, test_output_level, test_strategy
from stoobly_agent.lib import logger
from stoobly_agent.lib.utils.conditional_decorator import ConditionalDecorator

from .handlers.scenario_cli_handler import (
    create_handler, delete_handler, list_handler, replay_handler, reset_handler, show_handler, snapshot_handler, test_handler, diff_handler
)
from .helpers.feature_flags import local, remote
from .helpers.validations import *
from .types.scenario import ScenarioTestOptions

settings = Settings.instance()
is_remote = remote(settings)
is_local = local(settings)

@click.group(
    epilog="Run 'stoobly-agent scenario COMMAND --help' for more information on a command.",
    help="Manage scenarios"
)
@click.pass_context
def scenario(ctx):
    pass

@scenario.command(
    help="Create a scenario"
)
@click.option('--description', default='', help='Scenario description.')
@click.option('--format', type=click.Choice(FORMATS), help='Format output.')
@ConditionalDecorator(lambda f: click.option('--project-key', help='Project to create scenario in.')(f), is_remote)
@click.option('--select', multiple=True, help='Select column(s) to display.')
@click.option('--without-headers', is_flag=True, default=False, help='Disable printing column headers.')
@click.argument('name')
def create(**kwargs):
    create_handler(kwargs)

@scenario.command(
    help="Replay a scenario"
)
@ConditionalDecorator(lambda f: click.option(
    '--alias-resolve-strategy', 
    default=alias_resolve_strategy.NONE, 
    type=click.Choice([alias_resolve_strategy.NONE, alias_resolve_strategy.FIFO, alias_resolve_strategy.LIFO]), 
    help='Strategy for resolving dynamic values for aliases.'
)(f), is_remote)
@ConditionalDecorator(lambda f: click.option('--assign', multiple=True, help='Assign alias values. Format: <NAME>=<VALUE>')(f), is_remote)
@click.option('--format', type=click.Choice([JSON_FORMAT]), help='Format replay response.')
@ConditionalDecorator(lambda f: click.option('--group-by', help='Repeat for each alias name.')(f), is_remote)
@click.option('--host', help='Rewrite request host.')
@click.option('--lifecycle-hooks-path', help='Path to lifecycle hooks script.')
@click.option(
    '--log-level', default=logger.WARNING, type=click.Choice([logger.DEBUG, logger.INFO, logger.WARNING, logger.ERROR]), 
    help=f'''
        Configure which logs to print. Defaults to {logger.WARNING}.
    '''
)
@ConditionalDecorator(
  lambda f: click.option(
    '--overwrite', is_flag=True, default=False, help='Replay scenario and overwrite existing responses.'
  )(f), not is_remote
)
@click.option('--record', is_flag=True, default=False, help='Replay scenario and record.')
@ConditionalDecorator(lambda f: click.option('--save', is_flag=True, default=False, help='Replay scenario and save to history.')(f), not is_remote)
@click.option('--scenario-key', help='Record to scenario.')
@click.option('--scheme', help='Rewrite request scheme.')
@ConditionalDecorator(lambda f: click.option('--trace-id', help='Use existing trace.')(f), is_remote)
@ConditionalDecorator(lambda f: click.option('--validate', multiple=True, help='Validate one or more aliases. Format: <NAME>=?<TYPE>')(f), is_remote)
@click.argument('key')
def replay(**kwargs):
   replay_handler(kwargs) 

@scenario.command(
    help="Show all scenarios"
)
@click.option('--format', type=click.Choice(FORMATS), help='Format output.')
@click.option('--page', default=0)
@ConditionalDecorator(lambda f: click.option('--project-key', help='Project to create scenario in.')(f), is_remote)
@click.option('--select', multiple=True, help='Select column(s) to display.')
@click.option('--search', help='Query to filter scenarios by')
@click.option('--size', default=10)
@click.option('--sort-by', default='created_at', help='created_at|name')
@click.option('--sort-order', default='desc', help='asc | desc')
@click.option('--without-headers', is_flag=True, default=False, help='Disable printing column headers.')
def list(**kwargs):
    list_handler(kwargs)    

@scenario.command(
    help="Show a scenario"
)
@click.option('--format', type=click.Choice(FORMATS), help='Format output.')
@click.option('--select', multiple=True, help='Select column(s) to display.')
@click.option('--without-headers', is_flag=True, default=False, help='Disable printing column headers.')
@click.argument('key')
def show(**kwargs):
    show_handler(kwargs)

@scenario.command(
  help="Delete a scenario"
)
@click.argument('scenario_key')
def delete(**kwargs):
    delete_handler(kwargs)

if is_local:
    @click.group(
        epilog="Run 'stoobly-agent scenario snapshot COMMAND --help' for more information on a command.",
        help="Manage scenario snapshots"
    )
    @click.pass_context
    def snapshot(ctx):
        pass

    @snapshot.command(
        name='create',
        help="Create a scenario snapshot"
    )
    @click.option('--action', default=PUT_ACTION, type=click.Choice([DELETE_ACTION, PUT_ACTION]), help='Sets snapshot action.')
    @click.option('--decode', default=False, is_flag=True, help="Toggles whether to decode response bodies.")
    @click.option('--lifecycle-hooks-path', help='Path to lifecycle hooks script.')
    @click.option('--no-verify', is_flag=True, default=False)
    @click.argument('scenario_key')
    def snapshot_create(**kwargs):
        scenario_snapshot_path = snapshot_handler(kwargs)

        if scenario_snapshot_path is None:
            print("Error: Could not snapshot scenario", file=sys.stderr)
            sys.exit(1)

        update_request_snapshots(
          action=kwargs['action'],
          file_path=scenario_snapshot_path,
          lifecycle_hooks_path=kwargs.get('lifecycle_hooks_path'),
          no_verify=kwargs.get('no_verify', False),
          with_snapshot=False
        )

    @snapshot.command(
        name='reset',
        help="Reset a scenario to its snapshot state"
    )
    @click.option('--force', default=False, is_flag=True, help="Toggles whether resources are hard deleted.")
    @click.argument('scenario_key')
    def reset(**kwargs):
        reset_handler(kwargs)

    @snapshot.command(
        name='diff',
        help="Show diff between current scenario and its snapshot"
    )
    @click.option('--full', is_flag=True, default=False, help='Show full raw diffs for each request.')
    @click.option('--scenario-key', help='Show diffs only for this scenario key.')
    def diff(**kwargs):
        diff_handler(kwargs)

    @snapshot.command(
        name='list',
        help='List scenario snapshots'
    )
    @snapshot_list_options
    def snapshot_list(**kwargs):
        print_options = select_print_options(kwargs)
        rows = list_snapshots(
            resource=SCENARIO_RESOURCE,
            pending=kwargs.get('pending', False),
            scenario_key=kwargs.get('scenario_key'),
            search=kwargs.get('search'),
            size=kwargs.get('size'),
        )
        if len(rows):
            print_snapshots(rows, **print_options)

    scenario.add_command(snapshot)

@scenario.command(
    help="Replay and test a scenario"
)
@click.option('--aggregate-failures', default=False, is_flag=True, help='Toggles whether to continue execution on failure.')
@click.option(
    '--alias-resolve-strategy', 
    default=alias_resolve_strategy.NONE, 
    type=click.Choice([alias_resolve_strategy.NONE, alias_resolve_strategy.FIFO, alias_resolve_strategy.LIFO]), 
    help='Strategy for resolving dynamic values for aliases.'
)
@click.option('--assign', multiple=True, help='Assign alias values. Format: <NAME>=<VALUE>')
@click.option(
    '--filter', 
    default=test_filter.ALL, 
    type=click.Choice([test_filter.ALL, test_filter.ALIAS, test_filter.LINK]), 
    help='For iterable responses, selectively test properties.'
)
@click.option('--format', type=click.Choice([JSON_FORMAT]), help='Format replay response.')
@click.option('--group-by', help='Repeat for each alias name.')
@click.option('--host', help='Rewrite request host.')
@click.option('--lifecycle-hooks-path', help='Path to lifecycle hooks script.')
@click.option(
    '--log-level', default=logger.WARNING, type=click.Choice([logger.DEBUG, logger.INFO, logger.WARNING, logger.ERROR]), 
    help=f'''
        Configure which logs to print. Defaults to {logger.WARNING}.
    '''
)
@click.option('--openapi-specification-path', help='Path to OpenAPI specification file.')
@click.option(
  '--output-level', default=test_output_level.PASSED, type=click.Choice([test_output_level.FAILED, test_output_level.SKIPPED, test_output_level.PASSED]),
  help=f'''
    Configure which tests to print. Defaults to {test_output_level.PASSED}.
  '''
)
@click.option('--public-dir-path', help='Path to public files. Used for mocking requests.')
@ConditionalDecorator(lambda f: click.option('--remote-project-key', help='Use remote project for endpoint definitions.')(f), is_local and is_remote)
@ConditionalDecorator(lambda f: click.option('--report-key', help='Save results to report.')(f), is_remote)
@click.option('--response-fixtures-path', help='Path to response fixtures yaml. Used for mocking requests.')
@ConditionalDecorator(lambda f: click.option('--save', is_flag=True, default=False, help='Save results.')(f), is_remote)
@click.option('--scheme', help='Rewrite request scheme.')
@click.option(
    '--strategy', 
    default=test_strategy.DIFF, 
    type=click.Choice([test_strategy.CONTRACT, test_strategy.CUSTOM, test_strategy.DIFF, test_strategy.FUZZY]), 
    help='How to test responses.'
)
@click.option('--trace-id', help='Use existing trace.')
@click.option('--validate', multiple=True, help='Validate one or more aliases. Format: <NAME>=?<TYPE>')
@click.argument('key')
def test(**kwargs: ScenarioTestOptions):
    test_handler(kwargs)