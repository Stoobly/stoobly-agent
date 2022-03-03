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
@click.option('--page', default=0)
@click.option('--sort-by', default='created_at', help='created_at|name')
@click.option('--sort-order', default='desc', help='asc | desc')
@click.option('--size', default=10)
@click.argument('project_key')
def list(**kwargs):
    report = Report(Settings.instance())
    reports = report.index(
        kwargs['project_key'], **kwargs
    )
    print(json.dumps(reports, indent=2))