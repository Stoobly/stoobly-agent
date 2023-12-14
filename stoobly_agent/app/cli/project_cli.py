import click
import pdb
import sys

from stoobly_agent.app.settings import Settings

from .helpers import ProjectFacade
from .helpers.print_service import FORMATS, print_projects, select_print_options
from .helpers.validations import *

@click.group(
    epilog="Run 'stoobly-agent project COMMAND --help' for more information on a command.",
    help="Manage projects"
)
@click.pass_context
def project(ctx):
    pass

@project.command(
    help="Create a project"
)
@click.option('--description', help='Project description.')
@click.option('--format', type=click.Choice(FORMATS), help='Format output.')
@click.option('--organization-key', required=True, help='Project to create project in.')
@click.option('--select', multiple=True, help='Select column(s) to display.')
@click.option('--without-headers', is_flag=True, default=False, help='Disable printing column headers.')
@click.argument('name')
def create(**kwargs):
    print_options = select_print_options(kwargs)

    project = ProjectFacade(Settings.instance())

    try:
        project_response = project.create(**kwargs)
    except AssertionError as e:
        return print(e, file=sys.stderr)

    print_projects([project_response], **print_options)

@project.command(
    help="Show all projects"
)
@click.option('--format', type=click.Choice(FORMATS), help='Format output.')
@click.option('--page', default=0)
@click.option('--select', multiple=True, help='Select column(s) to display.')
@click.option('--size', default=10)
@click.option('--sort-by', default='created_at', help='created_at|name')
@click.option('--sort-order', default='desc', help='asc | desc')
@click.option('--without-headers', is_flag=True, default=False, help='Disable printing column headers.')
@click.argument('organization_key', required=False)
def list(**kwargs):
    print_options = select_print_options(kwargs)
    settings = Settings.instance()
    project = ProjectFacade(settings)

    organization_key = kwargs['organization_key']

    # If organization_key is not set, try to use current project's organization
    if not organization_key:
        try:
            project_key = ProjectKey(settings.proxy.intercept.project_key)

            if not project_key.is_local:
                organization_key = OrganizationKey.encode(project_key.organization_id)
        except InvalidProjectKey as e:
            pass

    # If organization_key is not set, try to use current user's private organization
    if not organization_key:
        try:
            user_profile = project.user_profile()
        except AssertionError as e:
            return print(e, file=sys.stderr)

        organization_key = user_profile['organization_key']

    validate_organization_key(organization_key)

    try:
        kwargs['organization_key'] = organization_key
        projects_response = project.index(kwargs)
    except AssertionError as e:
        return print(e, file=sys.stderr)

    if len(projects_response['list']) == 0:
        print('No projects found.', file=sys.stderr)
    else:
        print_projects(projects_response['list'], **print_options)

@project.command(
    help="Describe project"
)
@click.option('--format', type=click.Choice(FORMATS), help='Format output.')
@click.option('--select', multiple=True, help='Select column(s) to display.')
@click.option('--without-headers', is_flag=True, default=False, help='Disable printing column headers.')
@click.argument('project_key', required=False)
def show(**kwargs):
    print_options = select_print_options(kwargs)

    settings = Settings.instance()
    project_key = resolve_project_key_and_validate(kwargs, settings)
    project = ProjectFacade(settings)

    try:
        project_response = project.show(project_key)
    except AssertionError as e:
        return print(e, file=sys.stderr)

    print_projects([project_response], **print_options)