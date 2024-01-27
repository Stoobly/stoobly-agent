import os
import traceback

import click

from stoobly_agent.app.models.types import OPENAPI_FORMAT
from stoobly_agent.app.settings import Settings
from stoobly_agent.config.constants import env_vars
from stoobly_agent.lib.logger import bcolors
from stoobly_agent.lib.utils.conditional_decorator import ConditionalDecorator

from .helpers.endpoint_facade import EndpointFacade
from .helpers.endpoints_apply_context import EndpointsApplyContext
from .helpers.feature_flags import local, remote
from .helpers.validations import validate_project_key, validate_scenario_key

settings = Settings.instance()
is_remote = remote(settings)
is_local = local(settings)

@click.group(
  epilog="Run 'stoobly-agent feature COMMAND --help' for more information on a command.",
  help="Manage endpoints"
)
@click.pass_context
def endpoint(ctx):
  pass

@endpoint.command(
  help="Apply endpoint to requests"
)
@click.option('--lifecycle-hooks-path', help='Path to lifecycle hooks script.')
@ConditionalDecorator(lambda f: click.option('--project-key', help='Project to create endpoint to.')(f), is_remote)
@ConditionalDecorator(lambda f: click.option('--remote-project-key', help='Which remote project to apply endpoints from.')(f), is_remote and is_local) 
@click.option('--scenario-key', help='Which scenario to import to. If none then all requests will be imported to.')
@click.option('--source-format', required=True, type=click.Choice([OPENAPI_FORMAT]), help='Spec file format.')
@click.option('--source-path', help='Path to spec file.')
def apply(**kwargs):
  context = EndpointsApplyContext()

  project_key = kwargs.get('remote_project_key') or settings.remote.project_key
  if project_key:
    project_key = validate_project_key(project_key)
    context.with_project(project_key.id)

  if kwargs.get('scenario_key'):
    scenario_key = validate_scenario_key(kwargs['scenario_key'])
    context.with_scenario(scenario_key.id)

  context.with_lifecycle_hooks_path(kwargs.get('lifecycle_hooks_path'))
  context.with_source(kwargs.get('source_path'), kwargs.get('source_format'))

  endpoint_handler = lambda endpoint: print(f"{bcolors.OKBLUE}Applying Endpoint: {endpoint['path']}{bcolors.ENDC}")
  context.with_endpoint_handler(endpoint_handler)

  request_handler = lambda request, endpoint: print(request.url)
  context.with_request_handler(request_handler)

  facade = EndpointFacade(settings)
  facade.apply(context)
