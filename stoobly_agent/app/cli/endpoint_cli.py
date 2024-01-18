import sys
import traceback

import click

from stoobly_agent.app.models.types import OPENAPI_FORMAT
from stoobly_agent.app.settings import Settings
from stoobly_agent.lib.logger import bcolors
from stoobly_agent.lib.utils.conditional_decorator import ConditionalDecorator

from .helpers.endpoint_facade import EndpointFacade
from .helpers.endpoints_apply_service import apply_endpoints
from .helpers.validations import validate_project_key
from .types.endpoint import EndpointCreateCliOptions

settings = Settings.instance()
is_remote = settings.cli.features.remote

@click.group(
  epilog="Run 'stoobly-agent feature COMMAND --help' for more information on a command.",
  help="Manage endpoints"
)
@click.pass_context
def endpoint(ctx):
  pass

@endpoint.command(
  'import',
  help="Import endpoints"
)
@click.option('--format', required=True, type=click.Choice([OPENAPI_FORMAT]), help='File format')
@click.option('--scenario-key', help='Which scenario to import to. If none then all requests will be imported to.')
@click.option('--lifecycle-hooks-path', help='Path to lifecycle hooks script.')
@ConditionalDecorator(lambda f: click.option('--project-key', help='Project to create endpoint in.')(f), is_remote)
@click.argument('path')
def _import(**kwargs: EndpointCreateCliOptions):
  facade = EndpointFacade(settings)

  try:
    facade.create(**{
      **kwargs,
    })
    print("Success!")
  except Exception as e:
    print("Failed to import API specification, stack trace:\n")
    print(traceback.format_exc())

@endpoint.command(
  help="Apply endpoint to requests"
)
@click.option('--remote-project-key', help='Which remote project to apply endpoints from.')
def apply(**kwargs):
  project_key = kwargs.get('remote_project_key')

  if not project_key:
    project_key = settings.remote.project_key

  if not project_key:
    print('Error: --remote-project-key not set', file=sys.stderr)
    sys.exit(1)

  project_key = validate_project_key(project_key)
  endpoint_handler = lambda endpoint: print(f"{bcolors.OKBLUE}Applying Endpoint: {endpoint['path']}{bcolors.ENDC}")
  request_handler = lambda request: print(request.url)

  apply_endpoints(
    project_key.id,
    endpoint_handler=endpoint_handler,
    request_handler=request_handler
  )
