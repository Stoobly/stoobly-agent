import click
import json

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

@report.command()
@click.option('--page', default=0, help='Reports offset.')
@click.option('--size', default=10, help='Number of reports to display')
@click.argument('project_key')
def list(**kwargs):
    report = Report(Settings.instance())
    reports = report.index(kwargs['project_key'], kwargs['page'], kwargs['size'])
    print(json.dumps(reports, indent=2))