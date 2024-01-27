import click
import os
import pdb
import sys

from stoobly_agent.app.cli.helpers.handle_replay_service import DEFAULT_FORMAT, JSON_FORMAT, handle_before_replay, handle_after_replay, print_session, ReplaySession
from stoobly_agent.app.cli.helpers.handle_test_service import SessionContext, exit_on_failure, handle_test_complete, handle_test_session_complete 
from stoobly_agent.app.cli.helpers.print_service import FORMATS, print_scenarios, select_print_options
from stoobly_agent.app.cli.helpers.test_facade import TestFacade
from stoobly_agent.app.cli.helpers.context import ReplayContext
from stoobly_agent.app.models.helpers.apply import Apply
from stoobly_agent.app.models.factories.resource.local_db.helpers.log_event import DELETE_ACTION, PUT_ACTION
from stoobly_agent.app.settings import Settings
from stoobly_agent.config.constants import alias_resolve_strategy, env_vars, test_filter, test_strategy
from stoobly_agent.lib import logger
from stoobly_agent.lib.utils.conditional_decorator import ConditionalDecorator

from .helpers.feature_flags import local, remote
from .helpers.scenario_facade import ScenarioFacade
from .helpers.validations import *

settings = Settings.instance()
is_remote = remote(settings)
is_local = local(settings)

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
@click.option('--format', type=click.Choice(FORMATS), help='Format output.')
@ConditionalDecorator(lambda f: click.option('--project-key', help='Project to create scenario in.')(f), is_remote)
@click.option('--select', multiple=True, help='Select column(s) to display.')
@click.option('--without-headers', is_flag=True, default=False, help='Disable printing column headers.')
@click.argument('name')
def create(**kwargs):
    print_options = select_print_options(kwargs)

    settings = Settings.instance()
    project_key = resolve_project_key_and_validate(kwargs, settings) 

    scenario = ScenarioFacade(settings)

    res, status = scenario.create(project_key, kwargs['name'], kwargs['description'])

    if filter_response(res, status):
        sys.exit(1)

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
@click.option('--format', type=click.Choice([JSON_FORMAT]), help='Format replay response.')
@ConditionalDecorator(lambda f: click.option('--group-by', help='Repeat for each alias name.')(f), is_remote)
@click.option('--host', help='Rewrite request host.')
@click.option('--lifecycle-hooks-path', help='Path to lifecycle hooks script.')
@click.option(
    '--log-level', default=logger.WARNING, type=click.Choice([logger.DEBUG, logger.INFO, logger.WARNING, logger.ERROR]), 
    help='''
        Log levels can be "debug", "info", "warning", or "error"
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
    os.environ[env_vars.LOG_LEVEL] = kwargs['log_level']

    scenario_key = validate_scenario_key(kwargs['key'])

    if kwargs.get('scenario_key'):
        if kwargs['scenario_key'] and not kwargs.get('record'):
            print("Error: Missing option '--record'.", file=sys.stderr)
            sys.exit(1)

        validate_scenario_key(kwargs['scenario_key'])

    scenario = ScenarioFacade(Settings.instance())

    scenario_response, status = scenario.show(kwargs.get('key'))
    if filter_response(scenario_response, status):
        sys.exit(1)

    if 'validate' in kwargs and len(kwargs['validate']):
        validate_aliases(kwargs['validate'], assign=kwargs['assign'], format=kwargs['format'], trace_id=kwargs['trace_id'])

    __assign_default_alias_resolve_strategy(kwargs)

    session: ReplaySession = {
        'buffer': kwargs['format'] and kwargs['format'] != DEFAULT_FORMAT,
        'contexts': [],
        'format': kwargs['format'],
        'scenario_id': scenario_key.id,
        'total': 0,
    }

    kwargs['before_replay'] = lambda context: handle_before_replay(
      context, session
    )
    kwargs['after_replay'] = lambda context: handle_after_replay(
        context, session
    )

    scenario.replay(kwargs.get('key'), kwargs)

    print_session(session)

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
    print_options = select_print_options(kwargs)

    settings = Settings.instance()

    project_key = resolve_project_key_and_validate(kwargs, settings)
    if 'project_key' in kwargs:
        del kwargs['project_key']

    if kwargs.get('search'):
        kwargs['q'] = kwargs['search']
        del kwargs['search']

    scenario = ScenarioFacade(settings)

    scenarios_response, status = scenario.index(project_key, kwargs)
    if filter_response(scenarios_response, status):
        sys.exit(1)

    if len(scenarios_response['list']) == 0:
        print('No scenarios found.')
    else:
        print_scenarios(scenarios_response['list'], **print_options) 

@scenario.command(
    help="Describe scenario"
)
@click.option('--format', type=click.Choice(FORMATS), help='Format output.')
@click.option('--select', multiple=True, help='Select column(s) to display.')
@click.option('--without-headers', is_flag=True, default=False, help='Disable printing column headers.')
@click.argument('key', required=False)
def show(**kwargs):
    print_options = select_print_options(kwargs)

    settings = Settings.instance()
    scenario_key = resolve_scenario_key_and_validate(kwargs, settings)
    scenario = ScenarioFacade(settings)

    scenario_response, status = scenario.show(scenario_key)
    if filter_response(scenario_response, status):
        sys.exit(1)

    print_scenarios([scenario_response], **print_options)

@scenario.command(
  help="Delete a scenario"
)
@click.argument('scenario_key')
def delete(**kwargs):
  validate_scenario_key(kwargs['scenario_key'])

  scenario = ScenarioFacade(settings.instance())
  res, status = scenario.show(kwargs['scenario_key'])

  if filter_response(res, status):
    sys.exit(1)

  is_deleted = res.get('is_deleted')
  if not res:
    print(f"Error: Could not find scenario", file=sys.stderr)
    sys.exit(1)

  res = scenario.delete(kwargs['scenario_key'])
  if not res:
    print('Error: Could not delete scenario', file=sys.stderr)
    sys.exit(1)

  if not is_deleted:
    print('Scenario moved to trash!')
  else:
    print('Scenario deleted!')

if not is_remote:
    @scenario.command(
        help="Snapshot a scenario"
    )
    @click.option('--action', default=PUT_ACTION, type=click.Choice([DELETE_ACTION, PUT_ACTION]), help='Sets snapshot action.')
    @click.option('--decode', default=False, is_flag=True, help="Toggles whether to decode response bodies.")
    @click.argument('scenario_key')
    def snapshot(**kwargs):
        scenario_key = kwargs['scenario_key']
        del kwargs['scenario_key']

        validate_scenario_key(scenario_key)

        scenario = ScenarioFacade(Settings.instance())
        res = scenario.snapshot(scenario_key, kwargs)

    @scenario.command(
        help="Reset a scenario to its snapshot state"
    )
    @click.option('--force', default=False, is_flag=True, help="Toggles whether resources are hard deleted.")
    @click.argument('scenario_key')
    def reset(**kwargs):
        scenario_key = kwargs['scenario_key']
        _scenario_key = validate_scenario_key(scenario_key)

        apply_service = Apply(force=kwargs['force']).with_logger(print)
        resetted = apply_service.scenario(_scenario_key.id)

        if not resetted:
            print('Successfully reset the scenario!')
        else:
            print('Could not reset the scenario.')

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
    help='''
        Log levels can be "debug", "info", "warning", or "error"
    '''
)
@ConditionalDecorator(lambda f: click.option('--remote-project-key', help='Use remote project for endpoint definitions.')(f), is_remote)
@ConditionalDecorator(lambda f: click.option('--report-key', help='Save to report.')(f), is_remote)
@ConditionalDecorator(lambda f: click.option('--save', is_flag=True, default=False, help='Replay request and save to history.')(f), is_remote)
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
def test(**kwargs):
    os.environ[env_vars.LOG_LEVEL] = kwargs['log_level']
    logger.Logger.reload()

    settings = Settings.instance()
    scenario_key = validate_scenario_key(kwargs['key'])

    if kwargs.get('remote_project_key'):
        validate_project_key(kwargs['remote_project_key'])

    if kwargs.get('report_key'):
        validate_report_key(kwargs['report_key'])

    if len(kwargs['validate']):
        validate_aliases(kwargs['validate'], assign=kwargs['assign'], format=kwargs['format'], trace_id=kwargs['trace_id'])

    __assign_default_alias_resolve_strategy(kwargs)

    session: ReplaySession = {
        'buffer': kwargs['format'] and kwargs['format'] != DEFAULT_FORMAT,
        'contexts': [],
        'format': kwargs['format'],
        'scenario_id': scenario_key.id,
        'total': 0,
    }

    session_context: SessionContext = { 
        'aggregate_failures': kwargs['aggregate_failures'], 
        'passed': 0, 
        'project_id': scenario_key.project_id, 
        'test_facade': TestFacade(settings), 
        'total': 0 
    }

    kwargs['before_replay'] = lambda context: handle_before_replay(
        context, session,
    )
    kwargs['after_replay'] = lambda context: __handle_on_test_response(
        context, session_context, kwargs
    )

    scenario = ScenarioFacade(settings)
    scenario.test(kwargs['key'], kwargs)

    handle_test_session_complete(session_context, format=kwargs['format'])

    exit_on_failure(session_context, format=kwargs['format'])

def __handle_on_test_response(replay_context: ReplayContext, session_context: SessionContext, kwargs):
    handle_test_complete(replay_context, session_context, format=kwargs['format'])

    if not session_context['aggregate_failures']:
        exit_on_failure(session_context, complete=False, format=kwargs['format'])

def __assign_default_alias_resolve_strategy(kwargs):
    # If we have assigned values to aliases, it's likely we want to also have them resolved
    if 'assign' in kwargs and len(kwargs['assign']) > 0 and kwargs['alias_resolve_strategy'] == alias_resolve_strategy.NONE:
        kwargs['alias_resolve_strategy'] = alias_resolve_strategy.FIFO