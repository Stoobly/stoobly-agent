import click
import json
import pdb

from stoobly_agent.lib.intercept_handler.constants import test_strategies

from ..settings import Settings
from .scenario_facade import ScenarioFacade
from .utils.tabulate_print_service import tabulate_print

@click.group()
@click.pass_context
def scenario(ctx):
    pass

@scenario.command()
@click.option('--description', help='Scenario description.')
@click.option('--project-key', required=True, help='Project to create scenario in.')
@click.argument('name')
def create(**kwargs):
    scenario = ScenarioFacade(Settings.instance())
    print(scenario.create(kwargs['project_key'], kwargs['name'], kwargs['description']))

@scenario.command()
@click.argument('scenario_key')
def replay(**kwargs):
    scenario_key = kwargs['scenario_key']
    del kwargs['scenario_key']

    scenario = ScenarioFacade(Settings.instance())
    scenario.replay(scenario_key, **kwargs)   

@scenario.command()
@click.option('--save-to-report', help='Key for the report to store test results.')
@click.option('--strategy', default=test_strategies.DIFF, help=f"{test_strategies.CUSTOM} | {test_strategies.DIFF} | {test_strategies.FUZZY}")
@click.argument('scenario_key')
def test(**kwargs):
    scenario_key = kwargs['scenario_key']
    del kwargs['scenario_key']

    scenario = ScenarioFacade(Settings.instance())
    scenario.test(scenario_key, **kwargs)

@scenario.command()
@click.option('--page', default=0)
@click.option('--sort-by', default='created_at', help='created_at|name')
@click.option('--sort-order', default='desc', help='asc | desc')
@click.option('--size', default=10)
@click.argument('project_key')
def list(**kwargs):
    project_key = kwargs['project_key']
    del kwargs['project_key']

    scenario = ScenarioFacade(Settings.instance())
    scenarios_response = scenario.index(project_key, **kwargs)

    tabulate_print(scenarios_response['list'], filter=['created_at', 'project_id', 'starred', 'updated_at'])