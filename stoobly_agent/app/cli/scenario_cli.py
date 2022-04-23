import click
import pdb
import sys

from stoobly_agent.app.settings import Settings
from stoobly_agent.config.constants import test_strategy
from stoobly_agent.lib.api.keys import ProjectKey, ScenarioKey

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
    project_key = kwargs.get('project_key')
    settings = Settings.instance()

    if not project_key:
        project_key = settings.proxy.intercept.project_key

    scenario = ScenarioFacade(Settings.instance())
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
@click.option('--save-to', help='Scenario to store replayed requests.')
@click.argument('scenario_key')
def replay(**kwargs):
    scenario_key = kwargs['scenario_key']
    del kwargs['scenario_key']

    scenario = ScenarioFacade(Settings.instance())
    scenario.replay(scenario_key, **kwargs)   

@scenario.command(
    help="Replay and test a scenario"
)
@click.option('--save-to', help='Report to store test results.')
@click.option('--strategy', help=f"{test_strategy.CUSTOM} | {test_strategy.DIFF} | {test_strategy.FUZZY}")
@click.argument('scenario_key')
def test(**kwargs):
    settings = Settings.instance()

    scenario_key = kwargs['scenario_key']
    del kwargs['scenario_key']

    if not kwargs.get('strategy'):
        project_key = ProjectKey(settings.proxy.intercept.project_key)
        data_rule = settings.proxy.data.data_rules(project_key.id)
        kwargs['strategy'] = data_rule.test_strategy

    scenario = ScenarioFacade(settings)
    scenario.test(scenario_key, **kwargs)

@scenario.command(
    help="Show all scenarios"
)
@click.option('--page', default=0)
@click.option('--project-key', help='Project to create scenario in.')
@click.option('--sort-by', default='created_at', help='created_at|name')
@click.option('--sort-order', default='desc', help='asc | desc')
@click.option('--size', default=10)
@click.option('--select', multiple=True, help='Select column(s) to display.')
@click.option('--without-headers', is_flag=True, default=False, help='Disable printing column headers.')
def list(**kwargs):
    project_key = kwargs.get('project_key')
    del kwargs['project_key']
    settings = Settings.instance()

    if not project_key:
        project_key = settings.proxy.intercept.project_key

    scenario = ScenarioFacade(settings)
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
@click.argument('scenario_key', required=False)
def show(**kwargs):
    scenario_key = kwargs.get('scenario_key')
    settings = Settings.instance()

    if not scenario_key:
        project_key = ProjectKey(settings.proxy.intercept.project_key)
        data_rule = settings.proxy.data.data_rules(project_key.id)
        scenario_key = data_rule.scenario_key

    if not scenario_key or len(scenario_key) == 0:
        return print('Invalid scenario key provided.', file=sys.stderr)

    scenario = ScenarioFacade(settings)
    scenario_response = scenario.show(scenario_key)
    tabulate_print([scenario_response], filter=['created_at', 'project_id', 'starred', 'updated_at'])

