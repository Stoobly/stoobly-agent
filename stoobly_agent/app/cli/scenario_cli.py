import click
import json
import pdb

from stoobly_agent.app.settings import Settings
from stoobly_agent.config.constants import test_strategy
from stoobly_agent.lib.api.keys import ProjectKey, ScenarioKey

from .scenario_facade import ScenarioFacade
from .utils.tabulate_print_service import tabulate_print

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
@click.option('--project-key', required=True, help='Project to create scenario in.')
@click.argument('name')
def create(**kwargs):
    scenario = ScenarioFacade(Settings.instance())
    print(scenario.create(kwargs['project_key'], kwargs['name'], kwargs['description']))

@scenario.command(
    help="Replay a scenario"
)
@click.argument('scenario_key')
def replay(**kwargs):
    scenario_key = kwargs['scenario_key']
    del kwargs['scenario_key']

    scenario = ScenarioFacade(Settings.instance())
    scenario.replay(scenario_key, **kwargs)   

@scenario.command(
    help="Replay and test a scenario"
)
@click.option('--save-to-report', help='Key for the report to store test results.')
@click.option('--strategy', default=test_strategy.DIFF, help=f"{test_strategy.CUSTOM} | {test_strategy.DIFF} | {test_strategy.FUZZY}")
@click.argument('scenario_key')
def test(**kwargs):
    scenario_key = kwargs['scenario_key']
    del kwargs['scenario_key']

    scenario = ScenarioFacade(Settings.instance())
    scenario.test(scenario_key, **kwargs)

@scenario.command(
    help="Show all scenarios"
)
@click.option('--page', default=0)
@click.option('--sort-by', default='created_at', help='created_at|name')
@click.option('--sort-order', default='desc', help='asc | desc')
@click.option('--size', default=10)
def list(**kwargs):
    project_key = None
    settings = Settings.instance()

    project_key = settings.proxy.intercept.project_key

    scenario = ScenarioFacade(settings)
    scenarios_response = scenario.index(project_key, **kwargs)

    if len(scenarios_response['list']) == 0:
        print('No scenarios found.')
    else:
        tabulate_print(scenarios_response['list'], filter=['created_at', 'project_id', 'starred', 'updated_at'])

@scenario.command(
    help="Set current active scenario"
)
@click.argument('scenario_key')
def set(**kwargs):
    settings = Settings.instance()

    scenario_key = ScenarioKey(kwargs['scenario_key'])
    if not scenario_key.id:
        return print("Invalid scenario key provided.")

    project_key = ProjectKey(kwargs['project_key'])

    if scenario_key.project_id != project_key.id:
        return print("Please provide a scenario that belongs to the current project.\n")

    data_rule = settings.proxy.data.data_rules(project_key.id)
    data_rule.scenario_key = kwargs['scenario_key']
    settings.commit()

    print("Scenario updated!")