import click
import os
import pdb
import sys

from stoobly_agent.app.cli.helpers.handle_replay_service import DEFAULT_FORMAT, JSON_FORMAT, handle_before_replay, print_request
from stoobly_agent.app.cli.helpers.handle_test_service import SessionContext, exit_on_failure, handle_test_complete, handle_test_session_complete 
from stoobly_agent.app.cli.helpers.print_service import print_scenarios, select_print_options
from stoobly_agent.app.cli.helpers.test_facade import TestFacade
from stoobly_agent.app.cli.helpers.context import ReplayContext
from stoobly_agent.app.settings import Settings
from stoobly_agent.config.constants import alias_resolve_strategy, env_vars, test_filter, test_strategy
from stoobly_agent.lib import logger
from stoobly_agent.lib.utils.conditional_decorator import ConditionalDecorator

from .helpers.scenario_facade import ScenarioFacade
from .helpers.validations import *

settings = Settings.instance()
is_remote = settings.cli.features.remote

@click.group(
    epilog="Run 'stoobly-agent scenario COMMAND --help' for more information on a command.",
    help="Manage request scenarios"
)
@click.pass_context
def scenario(ctx):
    pass

@scenario.command(
    help="Create a scenario"
)
@click.option('--description', default='', help='Scenario description.')
@ConditionalDecorator(lambda f: click.option('--project-key', help='Project to create scenario in.')(f), is_remote)
@click.option('--select', multiple=True, help='Select column(s) to display.')
@click.option('--without-headers', is_flag=True, default=False, help='Disable printing column headers.')
@click.argument('name')
def create(**kwargs):
    print_options = select_print_options(kwargs)

    settings = Settings.instance()
    project_key = resolve_project_key_and_validate(kwargs, settings) 

    scenario = ScenarioFacade(settings)

    try:
        res = scenario.create(project_key, kwargs['name'], kwargs['description'])
    except AssertionError as e:
        return print(e, file=sys.stderr)

    print_scenarios([res], **print_options)

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
@click.option('--format', default=DEFAULT_FORMAT, type=click.Choice([DEFAULT_FORMAT, JSON_FORMAT]), help='Format replay response.')
@ConditionalDecorator(lambda f: click.option('--group-by', help='Repeat for each alias name.')(f), is_remote)
@click.option('--host', help='Rewrite request host.')
@click.option('--lifecycle-hooks-script-path', help='Path to lifecycle hooks script.')
@click.option(
    '--log-level', default=logger.WARNING, type=click.Choice([logger.DEBUG, logger.INFO, logger.WARNING, logger.ERROR]), 
    help='''
        Log levels can be "debug", "info", "warning", or "error"
    '''
)
@click.option('--record', is_flag=True, default=False, help='Replay and record scenario.')
@click.option('--scenario-key', help='Record to scenario.')
@click.option('--scheme', help='Rewrite request scheme.')
@ConditionalDecorator(lambda f: click.option('--trace-id', help='Use existing trace.')(f), is_remote)
@ConditionalDecorator(lambda f: click.option('--validate', multiple=True, help='Validate one or more aliases. Format: <NAME>=?<TYPE>')(f), is_remote)
@click.argument('key')
def replay(**kwargs):
    os.environ[env_vars.LOG_LEVEL] = kwargs['log_level']

    validate_scenario_key(kwargs['key'])

    if kwargs.get('scenario_key'):
        if kwargs['scenario_key'] and not kwargs.get('record'):
            print("Error: Missing option '--record'.", file=sys.stderr)
            sys.exit(1)

        validate_scenario_key(kwargs['scenario_key'])

    if 'validate' in kwargs and len(kwargs['validate']):
        validate_aliases(kwargs['validate'], assign=kwargs['assign'], format=kwargs['format'], trace_id=kwargs['trace_id'])

    __assign_default_alias_resolve_strategy(kwargs)

    kwargs['before_replay'] = lambda context: handle_before_replay(
      context, kwargs['format']
    )
    kwargs['after_replay'] = lambda context: print_request(
        context, kwargs['format']
    )

    scenario = ScenarioFacade(Settings.instance())
    scenario.replay(kwargs.get('key'), kwargs)

@scenario.command(
    help="Show all scenarios"
)
@click.option('--page', default=0)
@ConditionalDecorator(lambda f: click.option('--project-key', help='Project to create scenario in.')(f), is_remote)
@click.option('--select', multiple=True, help='Select column(s) to display.')
@click.option('--size', default=10)
@click.option('--sort-by', default='created_at', help='created_at|name')
@click.option('--sort-order', default='desc', help='asc | desc')
@click.option('--without-headers', is_flag=True, default=False, help='Disable printing column headers.')
def list(**kwargs):
    print_options = select_print_options(kwargs)

    settings = Settings.instance()

    project_key = resolve_project_key_and_validate(kwargs, settings)
    if 'project_key' in kwargs:
        del kwargs['project_key']

    scenario = ScenarioFacade(settings)

    try:
        scenarios_response = scenario.index(project_key, kwargs)
    except AssertionError as e:
        return print(e, file=sys.stderr)

    if len(scenarios_response['list']) == 0:
        print('No scenarios found.')
    else:
        print_scenarios(scenarios_response['list'], **print_options) 

@scenario.command(
    help="Describe scenario"
)
@click.option('--select', multiple=True, help='Select column(s) to display.')
@click.option('--without-headers', is_flag=True, default=False, help='Disable printing column headers.')
@click.argument('key', required=False)
def show(**kwargs):
    print_options = select_print_options(kwargs)

    settings = Settings.instance()
    scenario_key = resolve_scenario_key_and_validate(kwargs, settings)
    scenario = ScenarioFacade(settings)

    try:
        scenario_response = scenario.show(scenario_key)
    except AssertionError as e:
        return print(e, file=sys.stderr)

    print_scenarios([scenario_response], **print_options)

if is_remote:
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
    @click.option('--format', default=DEFAULT_FORMAT, type=click.Choice([DEFAULT_FORMAT, JSON_FORMAT]), help='Format replay response.')
    @click.option('--group-by', help='Repeat for each alias name.')
    @click.option('--host', help='Rewrite request host.')
    @click.option('--lifecycle-hooks-script-path', help='Path to lifecycle hooks script.')
    @click.option(
        '--log-level', default=logger.WARNING, type=click.Choice([logger.DEBUG, logger.INFO, logger.WARNING, logger.ERROR]), 
        help='''
            Log levels can be "debug", "info", "warning", or "error"
        '''
    )
    @click.option('--report-key', help='Save to report.')
    @click.option('--scheme', help='Rewrite request scheme.')
    @click.option(
        '--strategy', 
        default=test_strategy.DIFF, 
        type=click.Choice([test_strategy.CUSTOM, test_strategy.DIFF, test_strategy.FUZZY]), 
        help='How to test responses.'
    )
    @click.option('--trace-id', help='Use existing trace.')
    @click.option('--validate', multiple=True, help='Validate one or more aliases. Format: <NAME>=?<TYPE>')
    @click.argument('key')
    def test(**kwargs):
        os.environ[env_vars.LOG_LEVEL] = kwargs['log_level']
        logger.Logger.reload()

        settings = Settings.instance()
        scenario_key = validate_scenario_key(kwargs['key'])

        if kwargs.get('report_key'):
            validate_report_key(kwargs['report_key'])

        if len(kwargs['validate']):
            validate_aliases(kwargs['validate'], assign=kwargs['assign'], format=kwargs['format'], trace_id=kwargs['trace_id'])

        __assign_default_alias_resolve_strategy(kwargs)

        session_context: SessionContext = { 
            'aggregate_failures': kwargs['aggregate_failures'], 
            'passed': 0, 
            'project_id': scenario_key.project_id, 
            'test_facade': TestFacade(settings), 
            'total': 0 
        }

        kwargs['before_replay'] = lambda context: handle_before_replay(
        context, kwargs['format']
        )
        kwargs['after_replay'] = lambda context: __handle_on_test_response(
            context, session_context, kwargs['format']
        )

        scenario = ScenarioFacade(settings)
        scenario.test(kwargs['key'], kwargs)

        handle_test_session_complete(session_context, kwargs['format'])

        exit_on_failure(session_context, format=kwargs['format'])

def __handle_on_test_response(replay_context: ReplayContext, session_context: SessionContext, format = None):
    handle_test_complete(replay_context, session_context, format)

    if not session_context['aggregate_failures']:
        exit_on_failure(session_context, complete=False, format=format)

def __assign_default_alias_resolve_strategy(kwargs):
    # If we have assigned values to aliases, it's likely we want to also have them resolved
    if 'assign' in kwargs and len(kwargs['assign']) > 0 and kwargs['alias_resolve_strategy'] == alias_resolve_strategy.NONE:
        kwargs['alias_resolve_strategy'] = alias_resolve_strategy.FIFO