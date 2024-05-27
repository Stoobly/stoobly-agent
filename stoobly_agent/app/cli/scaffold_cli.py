import click
import sys

from stoobly_agent.app.cli.scaffold.app_create_command import AppCreateCommand
from stoobly_agent.app.cli.scaffold.service_create_command import ServiceCreateCommand
from stoobly_agent.app.cli.scaffold.workflow_create_command import WorkflowCreateCommand
from stoobly_agent.app.cli.scaffold.workflow_run_command import WorkflowRunCommand

from .scaffold.constants import SERVICE_APPLICATION_TYPE, SERVICE_EXTERNAL_TYPE, SERVICE_SIDECAR_TYPE, WORKFLOW_CI_TYPE, WORKFLOW_DEVELOPMENT_TYPE

@click.group(
    epilog="Run 'stoobly-agent project COMMAND --help' for more information on a command.",
    help="Manage scaffold"
)
@click.pass_context
def scaffold(ctx):
    pass

@click.group(
  epilog="Run 'stoobly-agent request response COMMAND --help' for more information on a command.",
  help="Manage app scaffold"
)
@click.pass_context
def app(ctx):
    pass

@click.group(
  epilog="Run 'stoobly-agent request response COMMAND --help' for more information on a command.",
  help="Manage service scaffold"
)
@click.pass_context
def service(ctx):
    pass

@app.command(
  help="Scaffold application"
)
@click.option('--app-dir-path', help='Path to create the app scaffold.')
@click.option('--force', help='If destination folder exists, recreate it.')
@click.argument('app_name')
def create(**kwargs):
  AppCreateCommand(**kwargs).build_with_docker()

@service.command(
  help="Scaffold a service",
)
@click.option('--app-dir-path')
@click.option('--hostname')
@click.option('--port')
@click.option('--scheme', type=click.Choice(['http', 'https']))
@click.option('--type', type=click.Choice([SERVICE_APPLICATION_TYPE, SERVICE_EXTERNAL_TYPE, SERVICE_SIDECAR_TYPE]))
@click.argument('service_name')
def create(**kwargs):
  command = ServiceCreateCommand(**kwargs).as_docker()

  if not command.app_namespace_exists:
    print(f"Error: {command.app_namespace_path} does not exist", file=sys.stderr)
    sys.exit(1)

  command.build_with_docker()

@click.group(
  epilog="Run 'stoobly-agent request response COMMAND --help' for more information on a command.",
  help="Manage service scaffold"
)
@click.pass_context
def workflow(ctx):
    pass

@workflow.command(
  help="Scaffold a workflow",
)
@click.option('--app-dir-path')
@click.option('--service-name')
@click.option('--type', type=click.Choice([WORKFLOW_CI_TYPE, WORKFLOW_DEVELOPMENT_TYPE]))
@click.argument('workflow_name')
def create(**kwargs):
  command = WorkflowCreateCommand(**kwargs).as_docker()

  if not command.app_namespace_exists:
    print(f"Error: {command.app_namespace_path} does not exist", file=sys.stderr)
    sys.exit(1)

  command.build_with_docker()

@workflow.command()
@click.option('--app-dir-path')
@click.option('--certs-dir-path')
@click.option('--data-dir-path')
@click.option('--network')
@click.option('--service-name')
@click.argument('workflow_name')
def run(**kwargs):
  command = WorkflowRunCommand(**kwargs).as_docker()

  if not command.workflow_exists:
    print(f"Error: {command.workflow_path} does not exist", file=sys.stderr)
    sys.exit(1)

  print(command.build_with_docker())

scaffold.add_command(app)
scaffold.add_command(service)
scaffold.add_command(workflow)