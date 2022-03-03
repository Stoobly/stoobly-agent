import click

from .report import Report
from ..settings import Settings

@click.group()
@click.pass_context
def report(ctx):
    pass

@report.command()
@click.option('--description', help='Report description.')
@click.option('--project-key', required=True, help='Project to create report in.')
@click.argument('name')
def create(**kwargs):
    report = Report(Settings.instance())
    print(report.create(kwargs['project_key'], kwargs['name'], kwargs['description']))