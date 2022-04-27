import click
import pdb
import sys

from stoobly_agent.app.settings import Settings
from stoobly_agent.config.constants import test_strategy
from stoobly_agent.lib.api.keys import InvalidProjectKey, InvalidScenarioKey, ProjectKey, ScenarioKey
from stoobly_agent.lib.logger import Logger

from .helpers.scenario_facade import ScenarioFacade
from .helpers.tabulate_print_service import tabulate_print

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
    project_key = __resolve_project_key_and_validate(kwargs, settings) 

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
    __validate_scenario_key(kwargs['key'])

    if kwargs.get('scenario_key') and not kwargs.get('record'):
        print("Error: Missing option '--record'.", file=sys.stderr)
        sys.exit(1)

    if 'scenario_key' in kwargs:
        __validate_scenario_key(kwargs['scenario_key'])

    scenario = ScenarioFacade(Settings.instance())

    scenario.replay(kwargs.get('key'), **kwargs)

@scenario.command(
    help="Replay and test a scenario"
)
@click.option('--report-key', help='Save to report.')
@click.option('--strategy', help=f"{test_strategy.CUSTOM} | {test_strategy.DIFF} | {test_strategy.FUZZY}")
@click.argument('key')
def test(**kwargs):
    __validate_scenario_key(kwargs['key'])

    scenario = ScenarioFacade(Settings.instance())

    scenario.test(kwargs['key'], **kwargs)

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
    project_key = __resolve_project_key_and_validate(kwargs, settings)
    scenario = ScenarioFacade(settings)

    __validate_project_key(project_key)

    scenarios_response = scenario.index(project_key, **kwargs)

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
    scenario_key = __resolve_scenario_key_and_validate(kwargs, settings)
    scenario = ScenarioFacade(settings)

    scenario_response = scenario.show(scenario_key)

    tabulate_print([scenario_response], filter=['created_at', 'project_id', 'starred', 'updated_at'])

### Helpers

def __handle_invalid_scenario_key():
    print('Error: Invalid scenario key', file=sys.stderr) 
    sys.exit(1)

def __handle_invalid_project_key():
    print('Error: Invalid project key', file=sys.stderr) 
    sys.exit(1)

def __validate_scenario_key(scenario_key):
    try:
        ScenarioKey(scenario_key)
    except InvalidScenarioKey:
        __handle_invalid_scenario_key()

def __validate_project_key(project_key):
    try:
        ProjectKey(project_key)
    except InvalidProjectKey:
        __handle_invalid_project_key()

def __resolve_project_key(kwargs: dict, settings: Settings):
    project_key = kwargs.get('project_key')
    del kwargs['project_key']

    if not project_key:
        project_key = settings.proxy.intercept.project_key
        Logger.instance().info(f"No project key specified, using {project_key}")

    return project_key

def __resolve_project_key_and_validate(kwargs: dict, settings: Settings  = Settings.instance()):
    project_key = __resolve_project_key(kwargs, settings)

    __validate_project_key(project_key)

    return project_key

def __resolve_scenario_key(kwargs: dict, settings: Settings):
    scenario_key = kwargs.get('key')

    if not scenario_key:
        project_key = __validate_project_key(settings.proxy.intercept.project_key)
        data_rule = settings.proxy.data.data_rules(project_key.id)
        scenario_key = data_rule.scenario_key
        Logger.instance().info(f"No scenario key specified, using {scenario_key}")

    return scenario_key

def __resolve_scenario_key_and_validate(kwargs: dict, settings: Settings = Settings.instance()):
    scenario_key = __resolve_scenario_key(kwargs, settings)

    __validate_scenario_key(scenario_key)

    return scenario_key