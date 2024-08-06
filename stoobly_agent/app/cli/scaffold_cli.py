import click
import pdb
import sys

from stoobly_agent.app.cli.helpers.shell import exec_stream
from stoobly_agent.app.cli.scaffold.app import App
from stoobly_agent.app.cli.scaffold.app_create_command import AppCreateCommand
from stoobly_agent.app.cli.scaffold.constants import DOCKER_NAMESPACE, WORKFLOW_MOCK_TYPE, WORKFLOW_RECORD_TYPE
from stoobly_agent.app.cli.scaffold.docker.service.builder import ServiceBuilder
from stoobly_agent.app.cli.scaffold.docker.workflow.decorators_factory import get_workflow_decorators
from stoobly_agent.app.cli.scaffold.service_create_command import ServiceCreateCommand
from stoobly_agent.app.cli.scaffold.workflow import Workflow
from stoobly_agent.app.cli.scaffold.workflow_create_command import WorkflowCreateCommand
from stoobly_agent.app.cli.scaffold.workflow_log_command import WorkflowLogCommand
from stoobly_agent.app.cli.scaffold.workflow_run_command import WorkflowRunCommand
from stoobly_agent.lib.logger import bcolors

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
  kwargs['namespace'] = DOCKER_NAMESPACE
  AppCreateCommand(**kwargs).build()

@service.command(
  help="Scaffold a service",
)
@click.option('--app-dir-path')
@click.option('--detached', is_flag=True)
@click.option('--hostname')
@click.option('--port')
@click.option('--priority', help='Determines the service run order.')
@click.option('--proxy-mode', default="regular", help='''
  Proxy mode can be "regular", "transparent", "socks5",
  "reverse:SPEC", or "upstream:SPEC". For reverse and
  upstream proxy modes, SPEC is host specification in
  the form of "http[s]://host[:port]".
''')
@click.option('--scheme', type=click.Choice(['http', 'https']))
@click.option('--sidecar', is_flag=True)
@click.option('--workflow', multiple=True, type=click.Choice([WORKFLOW_MOCK_TYPE, WORKFLOW_RECORD_TYPE]), help='Include pre-defined workflows.')
@click.argument('service_name')
def create(**kwargs):
  kwargs['namespace'] = DOCKER_NAMESPACE
  command = ServiceCreateCommand(**kwargs)

  if not command.app_dir_path:
    print(f"Error: {command.app_dir_path} does not exist", file=sys.stderr)
    sys.exit(1)

  command.build()

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
@click.option('--template', type=click.Choice([WORKFLOW_MOCK_TYPE, WORKFLOW_RECORD_TYPE]), help='Select which workflow to use as a template.')
@click.argument('workflow_name')
def create(**kwargs):
  kwargs['namespace'] = DOCKER_NAMESPACE
  command = WorkflowCreateCommand(**kwargs)

  if not command.app_namespace_exists:
    print(f"Error: {command.app_namespace_path} does not exist", file=sys.stderr)
    sys.exit(1)

  service_config = command.service_config
  workflow_decorators = get_workflow_decorators(kwargs['template'], service_config)
  command.build(workflow_decorators=workflow_decorators)

@workflow.command()
@click.option('--app-dir-path', help='Path to application directory.')
@click.option('--data-dir-path', help='Path to Stoobly data directory.')
@click.option('--dry-run', default=False, is_flag=True)
@click.option('--extra-compose-path', help='Path to extra compose configuration files.')
@click.argument('workflow_name')
def stop(**kwargs):
  app = App(kwargs['app_dir_path'])

  if not app.exists:
    print(f"Error: {app.path} does not exist", file=sys.stderr)
    sys.exit(1)

  kwargs['namespace'] = DOCKER_NAMESPACE
  workflow = Workflow(kwargs['workflow_name'], app)

  commands = []
  for service in workflow.services(kwargs['namespace']):
    config = { **kwargs }
    config['service_name'] = service
    command = WorkflowRunCommand(**config)
    commands.append(command)

  commands = sorted(commands, key=lambda command: command.service_config.priority)

  for command in commands:
    if kwargs['dry_run']:
      print(command.down())
    else:
      exec_stream(command.down())

@workflow.command()
@click.option('--app-dir-path', help='Path to application directory.')
@click.option('--dry-run', default=False, is_flag=True)
@click.option('--service', multiple=True, help='Select which services to log. Defaults to all.')
@click.argument('workflow_name')
def logs(**kwargs):
  app = App(kwargs['app_dir_path'])

  if not app.exists:
    print(f"Error: {app.path} does not exist", file=sys.stderr)
    sys.exit(1)

  kwargs['namespace'] = DOCKER_NAMESPACE
  workflow = Workflow(kwargs['workflow_name'], app)

  commands = []
  for service in workflow.services(kwargs['namespace']):
    if len(kwargs['service']) > 0 and service not in kwargs['service']:
      continue

    config = { **kwargs }
    config['service_name'] = service 
    command = WorkflowLogCommand(**config)
    commands.append(command)

  commands = sorted(commands, key=lambda command: command.service_config.priority)

  for command in commands:
    __print_header(f"SERVICE {command.service_name}")

    for shell_command in command.all():
      __print_subheader(f"LOGS {shell_command}")
      if not  kwargs['dry_run']:
        exec_stream(shell_command)
 
@workflow.command()
@click.option('--app-dir-path', help='Path to application directory.')
@click.option('--certs-dir-path', help='Path to certs directory.')
@click.option('--data-dir-path', help='Path to Stoobly data directory.')
@click.option('--dry-run', default=False, is_flag=True)
@click.option('--extra-compose-path', help='Path to extra compose configuration files.')
@click.option('--network', help='Name of network namespace.')
@click.argument('workflow_name')
def run(**kwargs):
  app = App(kwargs['app_dir_path'])

  if not app.exists:
    print(f"Error: {app.path} does not exist", file=sys.stderr)
    sys.exit(1)

  kwargs['namespace'] = DOCKER_NAMESPACE
  workflow = Workflow(kwargs['workflow_name'], app)

  commands = []
  for service in workflow.services(kwargs['namespace']):
    config = { **kwargs }
    config['service_name'] = service
    command = WorkflowRunCommand(**config)
    commands.append(command)

  commands = sorted(commands, key=lambda command: command.service_config.priority)

  for command in commands:
    exec_command = command.up()

    __print_header(f"SERVICE {command.service_name}")

    if not kwargs['dry_run']:
      exec_stream(exec_command)
    else:
      print(exec_command)
 
scaffold.add_command(app)
scaffold.add_command(service)
scaffold.add_command(workflow)

def __print_header(text: str):
  print(f"=== {bcolors.OKBLUE}{text}{bcolors.ENDC}")

def __print_subheader(text: str):
  print(f"=== {bcolors.OKCYAN}{text}{bcolors.ENDC}")