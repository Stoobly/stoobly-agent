import click
import pdb
import sys

from stoobly_agent.app.settings import Settings
from stoobly_agent.lib.api.keys import organization_key
from stoobly_agent.lib.api.users_resource import UsersResource

from .helpers import ProjectFacade
from .helpers.tabulate_print_service import tabulate_print
from .helpers.validations import *

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
    __print(project.create(**kwargs))

@project.command(
    help="Show all projects"
)
@click.option('--page', default=0)
@click.option('--select', multiple=True, help='Select column(s) to display.')
@click.option('--size', default=10)
@click.option('--sort-by', default='created_at', help='created_at|name')
@click.option('--sort-order', default='desc', help='asc | desc')
@click.option('--without-headers', is_flag=True, default=False, help='Disable printing column headers.')
@click.argument('organization_key', required=False)
def list(**kwargs):
    organization_key = kwargs['organization_key']

    select = kwargs['select']
    without_headers = kwargs['without_headers']
    del kwargs['select']
    del kwargs['without_headers']

    project = ProjectFacade(Settings.instance())
    if not kwargs['organization_key']:
        try:
            user_profile = project.user_profile()
        except AssertionError as e:
            return print(e, file=sys.stderr)

        organization_key = user_profile['organization_key']
        kwargs['organization_key'] = organization_key

    validate_organization_key(organization_key)

    try:
        projects_response = project.index(kwargs)
    except AssertionError as e:
        return print(e, file=sys.stderr)

    if len(projects_response['list']) == 0:
        print('No projects found.', file=sys.stderr)
    else:
        __print(projects_response['list'], without_headers=without_headers, select=select)

@project.command(
    help="Describe scenario"
)
@click.option('--select', multiple=True, help='Select column(s) to display.')
@click.option('--without-headers', is_flag=True, default=False, help='Disable printing column headers.')
@click.argument('project_key', required=False)
def show(**kwargs):
    settings = Settings.instance()
    project_key = resolve_project_key_and_validate(kwargs, settings)
    project = ProjectFacade(settings)

    try:
        project_response = project.show(project_key)
    except AssertionError as e:
        return print(e, file=sys.stderr)

    __print([project_response] **kwargs)

def __print(projects, **kwargs):
    tabulate_print(
        projects, 
        filter=['created_at', 'organization_id', 'project_id', 'starred', 'updated_at'],
        headers=not kwargs.get('without_headers'),
        select=kwargs.get('select')
    )