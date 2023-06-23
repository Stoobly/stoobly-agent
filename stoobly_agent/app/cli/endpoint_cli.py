import click

from stoobly_agent.app.models.types import OPENAPI_FORMAT
from stoobly_agent.app.settings import Settings
from stoobly_agent.lib.utils.conditional_decorator import ConditionalDecorator

from .helpers.endpoint_facade import EndpointFacade
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
@click.option('--lifecycle-hooks-script-path', help='Path to lifecycle hooks script.')
@ConditionalDecorator(lambda f: click.option('--project-key', help='Project to create endpoint in.')(f), is_remote)
@click.argument('path')
def _import(**kwargs: EndpointCreateCliOptions):
  facade = EndpointFacade(settings)

  facade.create(**{
    **kwargs,
  })

