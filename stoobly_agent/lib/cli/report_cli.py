import click
import json

from .report_facade import ReportFacade
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
    report = ReportFacade(Settings.instance())
    print(report.create(kwargs['project_key'], kwargs['name'], kwargs['description']))

@report.command()
@click.option('--page', default=0)
@click.option('--sort-by', default='created_at', help='created_at|name')
@click.option('--sort-order', default='desc', help='asc | desc')
@click.option('--size', default=10)
@click.argument('project_key')
def list(**kwargs):
    report_key = kwargs['project_key']
    del kwargs['project_key']

    report = ReportFacade(Settings.instance())
    reports = report.index(report_key, **kwargs)
    
    print(json.dumps(reports, indent=2))