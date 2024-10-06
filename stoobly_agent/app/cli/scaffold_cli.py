import click
import os
import pdb
import sys

from typing import List

from stoobly_agent.app.cli.helpers.shell import exec_stream
from stoobly_agent.app.cli.scaffold.app import App
from stoobly_agent.app.cli.scaffold.app_create_command import AppCreateCommand
from stoobly_agent.app.cli.scaffold.constants import DOCKER_NAMESPACE, WORKFLOW_MOCK_TYPE, WORKFLOW_RECORD_TYPE, WORKFLOW_TEST_TYPE
from stoobly_agent.app.cli.scaffold.docker.workflow.decorators_factory import get_workflow_decorators
from stoobly_agent.app.cli.scaffold.service_create_command import ServiceCreateCommand
from stoobly_agent.app.cli.scaffold.workflow import Workflow
from stoobly_agent.app.cli.scaffold.workflow_create_command import WorkflowCreateCommand
from stoobly_agent.app.cli.scaffold.workflow_copy_command import WorkflowCopyCommand
from stoobly_agent.app.cli.scaffold.workflow_log_command import WorkflowLogCommand
from stoobly_agent.app.cli.scaffold.workflow_run_command import WorkflowRunCommand
from stoobly_agent.config.constants import env_vars
from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.lib.logger import bcolors, DEBUG, ERROR, INFO, Logger, WARNING

LOG_ID = 'Scaffold'

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
@click.option('--app-dir-path', default=os.getcwd(), help='Path to create the app scaffold.')
@click.argument('app_name')
def create(**kwargs):
  app = App(kwargs['app_dir_path'], DOCKER_NAMESPACE)
  __app_build(app, **kwargs)

@service.command(
  help="Scaffold a service",
)
@click.option('--app-dir-path', default=os.getcwd(), help='Path to application directory.')
@click.option('--detached', is_flag=True)
@click.option('--env', multiple=True, help='Specify an environment variable.')
@click.option('--hostname')
@click.option('--port')
@click.option('--priority', help='Determines the service run order.')
@click.option('--proxy-mode', help='''
  Proxy mode can be "regular", "transparent", "socks5",
  "reverse:SPEC", or "upstream:SPEC". For reverse and
  upstream proxy modes, SPEC is host specification in
  the form of "http[s]://host[:port]".
''')
@click.option('--scheme', type=click.Choice(['http', 'https']))
@click.option('--workflow', multiple=True, type=click.Choice([WORKFLOW_MOCK_TYPE, WORKFLOW_RECORD_TYPE, WORKFLOW_TEST_TYPE]), help='Include pre-defined workflows.')
@click.argument('service_name')
def create(**kwargs):
  app = App(kwargs['app_dir_path'], DOCKER_NAMESPACE)
  __scaffold_build(app, **kwargs)

@click.group(
  epilog="Run 'stoobly-agent request response COMMAND --help' for more information on a command.",
  help="Manage service scaffold"
)
@click.pass_context
def workflow(ctx):
    pass

@workflow.command(
  help="Create workflow for service(s)"
)
@click.option('--app-dir-path', default=os.getcwd(), help='Path to application directory.')
@click.option('--env', multiple=True, help='Specify an environment variable.')
@click.option('--service', multiple=True, help='Specify the service(s) to create the workflow for.')
@click.option('--template', type=click.Choice([WORKFLOW_MOCK_TYPE, WORKFLOW_RECORD_TYPE, WORKFLOW_TEST_TYPE]), help='Select which workflow to use as a template.')
@click.argument('workflow_name')
def create(**kwargs):
  app = App(kwargs['app_dir_path'], DOCKER_NAMESPACE)

  for service_name in kwargs['service']:
    config = { **kwargs }
    del config['service']
    config['service_name'] = service_name

    __workflow_build(app, **config)

@workflow.command(
  help="Copy a workflow for service(s)",
)
@click.option('--app-dir-path', default=os.getcwd(), help='Path to application directory.')
@click.option('--service', multiple=True, help='Specify service(s) to add the workflow to.')
@click.argument('workflow_name')
@click.argument('destination_workflow_name')
def copy(**kwargs):
  app = App(kwargs['app_dir_path'], DOCKER_NAMESPACE)

  for service_name in kwargs['service']:
    config = { **kwargs }
    del config['service']
    config['service_name'] = service_name
      
    command = WorkflowCopyCommand(app, **config)

    if not command.app_dir_exists:
      print(f"Error: {command.app_dir_path} does not exist", file=sys.stderr)
      sys.exit(1)

    command.copy(kwargs['destination_workflow_name'])

@workflow.command()
@click.option('--app-dir-path', default=os.getcwd(), help='Path to application directory.')
@click.option('--context-dir-path', default=DataDir.instance().context_dir_path, help='Path to Stoobly data directory.')
@click.option('--dry-run', default=False, is_flag=True)
@click.option('--extra-compose-path', help='Path to extra compose configuration files.')
@click.option('--log-level', default=INFO, type=click.Choice([DEBUG, INFO, WARNING, ERROR]), help='''
    Log levels can be "debug", "info", "warning", or "error"
''')
@click.argument('workflow_name')
def stop(**kwargs):  
  cwd = os.getcwd()

  if not os.getenv(env_vars.LOG_LEVEL):
    os.environ[env_vars.LOG_LEVEL] = kwargs['log_level']

  app = App(kwargs['app_dir_path'], DOCKER_NAMESPACE, skip_validate_path=True)

  if kwargs['context_dir_path']:
    app.context_dir_path = kwargs['context_dir_path']

  if not app.exists:
    print(f"Error: {app.dir_path} does not exist", file=sys.stderr)
    sys.exit(1)
  else:
    os.chdir(kwargs['app_dir_path'])

  workflow = Workflow(kwargs['workflow_name'], app)

  commands: List[WorkflowRunCommand] = []
  for service in workflow.services:
    config = { **kwargs }
    config['service_name'] = service
    command = WorkflowRunCommand(app, **config)
    command.current_working_dir = cwd
    commands.append(command)

  commands = sorted(commands, key=lambda command: command.service_config.priority)

  for command in commands:
    __print_header(f"SERVICE {command.service_name}")

    exec_command = command.down()
    if not exec_command:
      continue

    if not kwargs['dry_run']:
      exec_stream(exec_command)
    else:
      print(exec_command)

@workflow.command()
@click.option('--app-dir-path', default=os.getcwd(), help='Path to application directory.')
@click.option('--dry-run', default=False, is_flag=True)
@click.option('--service', multiple=True, help='Select which services to log. Defaults to all.')
@click.argument('workflow_name')
def logs(**kwargs):
  app = App(kwargs['app_dir_path'], DOCKER_NAMESPACE)

  if not app.exists:
    print(f"Error: {app.dir_path} does not exist", file=sys.stderr)
    sys.exit(1)
  else:
    os.chdir(kwargs['app_dir_path'])

  workflow = Workflow(kwargs['workflow_name'], app)

  commands: List[WorkflowLogCommand] = []
  for service in workflow.services:
    if len(kwargs['service']) > 0 and service not in kwargs['service']:
      continue

    config = { **kwargs }
    config['service_name'] = service 
    command = WorkflowLogCommand(app, **config)
    commands.append(command)

  commands = sorted(commands, key=lambda command: command.service_config.priority)

  for command in commands:
    __print_header(f"SERVICE {command.service_name}")

    for shell_command in command.all():
      print(shell_command)

      if not kwargs['dry_run']:
        exec_stream(shell_command)
 
@workflow.command()
@click.option('--app-dir-path', default=os.getcwd(), help='Path to application directory.')
@click.option('--certs-dir-path', default=DataDir.instance().certs_dir_path, help='Path to certs directory.')
@click.option('--context-dir-path', default=DataDir.instance().path, help='Path to Stoobly data directory.')
@click.option('--dry-run', default=False, is_flag=True)
@click.option('--extra-compose-path', help='Path to extra compose configuration files.')
@click.option('--log-level', default=INFO, type=click.Choice([DEBUG, INFO, WARNING, ERROR]), help='''
    Log levels can be "debug", "info", "warning", or "error"
''')
@click.option('--network', help='Name of network namespace.')
@click.option('--service', multiple=True, help='Select which services to run. Defaults to all.')
@click.argument('workflow_name')
def run(**kwargs):
  cwd = os.getcwd()

  if not os.getenv(env_vars.LOG_LEVEL):
    os.environ[env_vars.LOG_LEVEL] = kwargs['log_level']

  app = App(kwargs['app_dir_path'], DOCKER_NAMESPACE, skip_validate_path=kwargs['dry_run'])
  if kwargs['certs_dir_path']:
    app.certs_dir_path = kwargs['certs_dir_path']

  if kwargs['context_dir_path']:
    app.context_dir_path = kwargs['context_dir_path']

  if not app.exists:
    print(f"Error: {app.dir_path} does not exist", file=sys.stderr)
    sys.exit(1)
  else:
    os.chdir(kwargs['app_dir_path'])

  app_create_command = AppCreateCommand(app)
  commands = []

  workflow = Workflow(kwargs['workflow_name'], app)
  services = workflow.services

  # Log services that don't exist
  missing_services = [service for service in kwargs['service'] if service not in services]
  if missing_services:
    Logger.instance(WARNING).warn(f"Service(s) {','.join(missing_services)} are not found")

  # If service is specified, run only those services
  if kwargs['service']:
    services = kwargs['service']

  for service in services:
    config = { **kwargs }
    config['service_name'] = service
    command = WorkflowRunCommand(app, **config)
    command.current_working_dir = cwd
    commands.append(command)

  # Create persistent network
  create_network_command = f"docker network create {app_create_command.app_config.network} 2> /dev/null"
  if not kwargs['dry_run']:
    exec_stream(create_network_command)
  else:
    print(create_network_command)

  commands = sorted(commands, key=lambda command: command.service_config.priority)
  for command in commands:
    __print_header(f"SERVICE {command.service_name}")

    exec_command = command.up()
    if not exec_command:
      continue

    if not kwargs['dry_run']:
      exec_stream(exec_command)
    else:
      print(exec_command)
 
scaffold.add_command(app)
scaffold.add_command(service)
scaffold.add_command(workflow)

def __print_header(text: str):
  Logger.instance(LOG_ID).info(f"{bcolors.OKBLUE}{text}{bcolors.ENDC}")

def __print_subheader(text: str):
  Logger.instance(LOG_ID).info(f"{bcolors.OKCYAN}{text}{bcolors.ENDC}")

def __app_build(app, **kwargs):
  AppCreateCommand(app, **kwargs).build()

def __scaffold_build(app, **kwargs):
  command = ServiceCreateCommand(app, **kwargs)

  if not command.app_dir_exists:
    print(f"Error: {command.app_dir_path} does not exist", file=sys.stderr)
    sys.exit(1)

  command.build()

def __workflow_build(app, **kwargs):
  command = WorkflowCreateCommand(app, **kwargs)

  if not command.app_dir_exists:
    print(f"Error: {command.app_dir_path} does not exist", file=sys.stderr)
    sys.exit(1)

  service_config = command.service_config
  workflow_decorators = get_workflow_decorators(kwargs['template'], service_config)
  command.build(
    headless=kwargs['headless'],
    template=kwargs['template'],
    workflow_decorators=workflow_decorators
  )