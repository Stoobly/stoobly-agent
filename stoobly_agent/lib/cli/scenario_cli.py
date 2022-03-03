import click
import json
import pdb

from ..settings import Settings
from .scenario import Scenario

@click.group()
@click.pass_context
def scenario(ctx):
    pass

@scenario.command()
@click.option('--save-to-report', help='Key for the report to store test results.')
@click.option('--strategy', help='Test strategy')
@click.argument('scenario_key')
def test(**kwargs):
    scenario_key = kwargs['scenario_key']
    del kwargs['scenario_key']

    scenario = Scenario(Settings.instance())
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

    scenario = Scenario(Settings.instance())
    scenarios = scenario.index(project_key, **kwargs)

    print(json.dumps(scenarios, indent=2))