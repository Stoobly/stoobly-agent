import click
import sys

from stoobly_agent.app.settings import Settings
from stoobly_agent.lib.api.keys import ProjectKey, ScenarioKey

from .helpers import ProjectFacade
from .utils.tabulate_print_service import tabulate_print

@click.group(
    epilog="Run 'stoobly-agent project COMMAND --help' for more information on a command.",
    help="Manage request projects"
)
@click.pass_context
def project(ctx):
    pass

@project.command(
    help="Create a project"
)
@click.option('--description', help='Project description.')
@click.option('--organization-key', required=True, help='Project to create project in.')
@click.argument('name')
def create(**kwargs):
    project = ProjectFacade(Settings.instance())
    print(project.create(**kwargs))

@project.command(
    help="Show all projects"
)
@click.option('--page', default=0)
@click.option('--select', multiple=True, help='Select column(s) to display.')
@click.option('--size', default=10)
@click.option('--sort-by', default='created_at', help='created_at|name')
@click.option('--sort-order', default='desc', help='asc | desc')
@click.option('--without-headers', is_flag=True, default=False, help='Disable printing column headers.')
@click.argument('organization_key')
def list(**kwargs):
    project = ProjectFacade(Settings.instance())
    projects_response = project.index(**kwargs)

    if len(projects_response['list']) == 0:
        print('No projects found.', file=sys.stderr)
    else:
        tabulate_print(
            projects_response['list'], 
            filter=['created_at', 'organization_id', 'project_id', 'starred', 'updated_at'],
            headers=not kwargs.get('without_headers'),
            select=kwargs.get('select'),
        )

@project.command(
    help="Describe scenario"
)
@click.option('--select', multiple=True, help='Select column(s) to display.')
@click.option('--without-headers', is_flag=True, default=False, help='Disable printing column headers.')
@click.argument('project_key', required=False)
def show(**kwargs):
    project_key = kwargs.get('project_key')
    settings = Settings.instance()

    if not project_key:
        project_key = settings.proxy.intercept.project_key

    if not project_key or len(project_key) == 0:
        return print('Invalid project key provided.', file=sys.stderr)

    project = ProjectFacade(settings)
    project_response = project.show(project_key)

    tabulate_print(
        [project_response], 
        filter=['created_at', 'organization_id', 'project_id', 'starred', 'updated_at'],
        headers=not kwargs.get('without_headers'),
        select=kwargs.get('select')
    )

@project.command(
    help="Set current active project"
)
@click.argument('project_key')
def use(**kwargs):
    settings = Settings.instance()

    project_key = ProjectKey(kwargs['project_key'])
    if not project_key.id:
        return print("Invalid project key provided.")

    scenario_key = ScenarioKey(kwargs['scenario_key'])

    if project_key.id != scenario_key.project_id:
        data_rule = settings.proxy.data.data_rules(project_key.id)
        data_rule.scenario_key = None
        print("Current scenario does not belong to current project, unsetting current scenario.\n")

    settings.proxy.intercept.project_key = kwargs['project_key']
    settings.commit()
    print("Project updated!")

