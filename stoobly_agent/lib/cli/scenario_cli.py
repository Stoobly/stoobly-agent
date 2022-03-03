import click

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
    scenario = Scenario(Settings.instance(), kwargs['scenario_key'])
    scenario.test(
        report_key=kwargs['save_to_report'],
        strategy=kwargs['strategy']
    )