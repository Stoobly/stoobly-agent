import click
import pdb
import sys

from stoobly_agent.app.cli.helpers.print_service import handle_on_request_response, handle_on_test_response
from stoobly_agent.app.settings import Settings
from stoobly_agent.config.constants import test_strategy

from .helpers.scenario_facade import ScenarioFacade
from .helpers.tabulate_print_service import tabulate_print
from .helpers.validations import *

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
@click.option('--description', help='Scenario description.')
@click.option('--project-key', help='Project to create scenario in.')
@click.option('--select', multiple=True, help='Select column(s) to display.')
@click.option('--without-headers', is_flag=True, default=False, help='Disable printing column headers.')
@click.argument('name')
def create(**kwargs):
    print_options = __select_print_options(kwargs)

    settings = Settings.instance()
    project_key = resolve_project_key_and_validate(kwargs, settings) 

    scenario = ScenarioFacade(settings)

    try:
        res = scenario.create(project_key, kwargs['name'], kwargs['description'])
    except AssertionError as e:
        return print(e, file=sys.stderr)

    __print([res], **print_options)

@scenario.command(
    help="Replay a scenario"
)
@click.option('--assign', multiple=True, help='Assign alias values.')
@click.option('--record', is_flag=True, default=False, help='Replay and record scenario.')
@click.option('--scenario-key', help='Record to scenario.')
@click.argument('key')
def replay(**kwargs):
    validate_scenario_key(kwargs['key'])

    if kwargs.get('scenario_key'):
        if kwargs['scenario_key'] and not kwargs.get('record'):
            print("Error: Missing option '--record'.", file=sys.stderr)
            sys.exit(1)

        validate_scenario_key(kwargs['scenario_key'])

    kwargs['on_response'] = handle_on_request_response

    scenario = ScenarioFacade(Settings.instance())
    scenario.replay(kwargs.get('key'), kwargs)

@scenario.command(
    help="Replay and test a scenario"
)
@click.option('--assign', multiple=True, help='Assign alias values.')
@click.option('--report-key', help='Save to report.')
@click.option('--strategy', help=f"{test_strategy.CUSTOM} | {test_strategy.DIFF} | {test_strategy.FUZZY}")
@click.argument('key')
def test(**kwargs):
    scenario_key = validate_scenario_key(kwargs['key'])

    if kwargs.get('report_key'):
        validate_report_key(kwargs['report_key'])

    settings = Settings.instance()
    kwargs['on_response'] = lambda context: handle_on_test_response(
        context, scenario_key.project_id, settings
    )

    scenario = ScenarioFacade(settings)
    scenario.test(kwargs['key'], kwargs)

@scenario.command(
    help="Show all scenarios"
)
@click.option('--page', default=0)
@click.option('--project-key', help='Project to list scenarios from.')
@click.option('--select', multiple=True, help='Select column(s) to display.')
@click.option('--size', default=10)
@click.option('--sort-by', default='created_at', help='created_at|name')
@click.option('--sort-order', default='desc', help='asc | desc')
@click.option('--without-headers', is_flag=True, default=False, help='Disable printing column headers.')
def list(**kwargs):
    print_options = __select_print_options(kwargs)

    settings = Settings.instance()
    project_key = resolve_project_key_and_validate(kwargs, settings)
    del kwargs['project_key']

    scenario = ScenarioFacade(settings)

    try:
        scenarios_response = scenario.index(project_key, kwargs)
    except AssertionError as e:
        return print(e, file=sys.stderr)

    if len(scenarios_response['list']) == 0:
        print('No scenarios found.')
    else:
        __print(scenarios_response['list'], **print_options) 

@scenario.command(
    help="Describe scenario"
)
@click.option('--select', multiple=True, help='Select column(s) to display.')
@click.option('--without-headers', is_flag=True, default=False, help='Disable printing column headers.')
@click.argument('key', required=False)
def show(**kwargs):
    print_options = __select_print_options(kwargs)

    settings = Settings.instance()
    scenario_key = resolve_scenario_key_and_validate(kwargs, settings)
    scenario = ScenarioFacade(settings)

    try:
        scenario_response = scenario.show(scenario_key)
    except AssertionError as e:
        return print(e, file=sys.stderr)

    __print([scenario_response], **print_options)

def __print(scenarios, **kwargs):
    tabulate_print(
        scenarios, 
        filter=['created_at', 'priority', 'project_id', 'starred', 'updated_at'],
        headers=not kwargs.get('without_headers'),
        select=kwargs.get('select') or []
    )

def __select_print_options(kwargs):
    print_options = {
        'select': kwargs['select'],
        'without_headers': kwargs['without_headers']
    }

    del kwargs['without_headers']
    del kwargs['select']

    return print_options