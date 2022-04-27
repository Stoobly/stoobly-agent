import click
import pdb
import sys

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
    settings = Settings.instance()
    project_key = resolve_project_key_and_validate(kwargs, settings) 

    scenario = ScenarioFacade(settings)
    res = scenario.create(project_key, kwargs['name'], kwargs['description'])

    tabulate_print(
        [res],
        filter=['created_at', 'project_id', 'starred', 'updated_at'],
        headers=not kwargs.get('without_headers'),
        select=kwargs.get('select')
    )

@scenario.command(
    help="Replay a scenario"
)
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

    scenario = ScenarioFacade(Settings.instance())

    scenario.replay(kwargs.get('key'), kwargs)

@scenario.command(
    help="Replay and test a scenario"
)
@click.option('--report-key', help='Save to report.')
@click.option('--strategy', help=f"{test_strategy.CUSTOM} | {test_strategy.DIFF} | {test_strategy.FUZZY}")
@click.argument('key')
def test(**kwargs):
    validate_scenario_key(kwargs['key'])

    if kwargs.get('report_key'):
        validate_report_key(kwargs['report_key'])

    scenario = ScenarioFacade(Settings.instance())

    scenario.test(kwargs['key'], kwargs)

@scenario.command(
    help="Show all scenarios"
)
@click.option('--page', default=0)
@click.option('--project-key', help='Project to list scenarios from.')
@click.option('--sort-by', default='created_at', help='created_at|name')
@click.option('--sort-order', default='desc', help='asc | desc')
@click.option('--size', default=10)
@click.option('--select', multiple=True, help='Select column(s) to display.')
@click.option('--without-headers', is_flag=True, default=False, help='Disable printing column headers.')
def list(**kwargs):
    settings = Settings.instance()
    project_key = resolve_project_key_and_validate(kwargs, settings)
    scenario = ScenarioFacade(settings)

    validate_project_key(project_key)

    scenarios_response = scenario.index(project_key, kwargs)

    if len(scenarios_response['list']) == 0:
        print('No scenarios found.')
    else:
        tabulate_print(
            scenarios_response['list'], 
            filter=['created_at', 'project_id', 'starred', 'updated_at'],
            headers=not kwargs.get('without_headers'),
            select=kwargs.get('select')
        )

@scenario.command(
    help="Describe scenario"
)
@click.argument('key', required=False)
def show(**kwargs):
    settings = Settings.instance()
    scenario_key = resolve_scenario_key_and_validate(kwargs, settings)
    scenario = ScenarioFacade(settings)

    scenario_response = scenario.show(scenario_key)

    tabulate_print([scenario_response], filter=['created_at', 'project_id', 'starred', 'updated_at'])