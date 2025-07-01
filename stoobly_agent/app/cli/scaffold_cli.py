import click
import os
import pdb
import sys

from io import TextIOWrapper
from typing import List
from urllib.parse import urlparse

from stoobly_agent.app.cli.helpers.certificate_authority import CertificateAuthority
from stoobly_agent.app.cli.helpers.shell import exec_stream
from stoobly_agent.app.cli.scaffold.app import App
from stoobly_agent.app.cli.scaffold.app_create_command import AppCreateCommand
from stoobly_agent.app.cli.scaffold.constants import (
  DOCKER_NAMESPACE, WORKFLOW_CONTAINER_PROXY, WORKFLOW_MOCK_TYPE, WORKFLOW_RECORD_TYPE, WORKFLOW_TEST_TYPE
)
from stoobly_agent.app.cli.scaffold.containerized_app import ContainerizedApp
from stoobly_agent.app.cli.scaffold.docker.service.configure_gateway import configure_gateway
from stoobly_agent.app.cli.scaffold.docker.workflow.decorators_factory import get_workflow_decorators
from stoobly_agent.app.cli.scaffold.hosts_file_manager import HostsFileManager
from stoobly_agent.app.cli.scaffold.service import Service
from stoobly_agent.app.cli.scaffold.service_config import ServiceConfig
from stoobly_agent.app.cli.scaffold.service_create_command import ServiceCreateCommand
from stoobly_agent.app.cli.scaffold.service_delete_command import ServiceDeleteCommand
from stoobly_agent.app.cli.scaffold.service_update_command import ServiceUpdateCommand
from stoobly_agent.app.cli.scaffold.service_workflow_validate_command import ServiceWorkflowValidateCommand
from stoobly_agent.app.cli.scaffold.templates.constants import CORE_SERVICES
from stoobly_agent.app.cli.scaffold.validate_exceptions import ScaffoldValidateException
from stoobly_agent.app.cli.scaffold.workflow import Workflow
from stoobly_agent.app.cli.scaffold.workflow_create_command import WorkflowCreateCommand
from stoobly_agent.app.cli.scaffold.workflow_copy_command import WorkflowCopyCommand
from stoobly_agent.app.cli.scaffold.workflow_log_command import WorkflowLogCommand
from stoobly_agent.app.cli.scaffold.workflow_run_command import WorkflowRunCommand
from stoobly_agent.app.cli.scaffold.workflow_validate_command import WorkflowValidateCommand
from stoobly_agent.config.constants import env_vars
from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.lib.logger import bcolors, DEBUG, ERROR, INFO, Logger, WARNING

from .helpers.print_service import FORMATS, print_services, select_print_options
from .validators.scaffold import validate_app_name, validate_hostname, validate_namespace, validate_service_name

LOG_ID = 'Scaffold'

current_working_dir = os.getcwd()
data_dir: DataDir = DataDir.instance()

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

@click.group(
  epilog="Run 'stoobly-agent request response COMMAND --help' for more information on a command.",
  help="Manage workflow scaffold"
)
@click.pass_context
def workflow(ctx):
    pass

@click.group(
  epilog="Run 'stoobly-agent scaffold hostname COMMAND --help' for more information on a command.",
  help="Manage scaffold service hostnames"
)
@click.pass_context
def hostname(ctx):
    pass

@app.command(
  help="Scaffold application"
)
@click.option('--app-dir-path', default=current_working_dir, help='Path to create the app scaffold.')
@click.option('--network', help='App default network name. Defaults to app name.')
@click.option('--quiet', is_flag=True, help='Disable log output.')
@click.option('--ui-port', default=4200, type=click.IntRange(1, 65535), help='UI service port.')
@click.argument('app_name', callback=validate_app_name)
def create(**kwargs):
  __validate_app_dir(kwargs['app_dir_path'])

  app = App(kwargs['app_dir_path'], DOCKER_NAMESPACE)

  if not kwargs['quiet'] and os.path.exists(app.scaffold_namespace_path):
    print(f"{kwargs['app_dir_path']} already exists, updating scaffold maintained files...")

  if not kwargs['network']:
    kwargs['network'] = kwargs['app_name']

  AppCreateCommand(app, **kwargs).build()

@app.command(
  help="Scaffold app service certs"
)
@click.option('--app-dir-path', default=current_working_dir, help='Path to application directory.')
@click.option('--ca-certs-dir-path', default=data_dir.ca_certs_dir_path, help='Path to ca certs directory used to sign SSL certs.')
@click.option('--certs-dir-path', help='Path to certs directory. Defaults to the certs dir of the context.')
@click.option('--context-dir-path', default=data_dir.context_dir_path, help='Path to Stoobly data directory.')
@click.option('--service', multiple=True, help='Select which services to run. Defaults to all.')
@click.option('--workflow', multiple=True, help='Specify services by workflow(s). Defaults to all.')
def mkcert(**kwargs):
  app = App(kwargs['app_dir_path'], DOCKER_NAMESPACE, **kwargs)
  __validate_app(app)

  services = __get_services(
    app, service=kwargs['service'], without_core=True, workflow=kwargs['workflow']
  )

  __services_mkcert(app, services)

@service.command(
  help="Scaffold a service",
)
@click.option('--app-dir-path', default=current_working_dir, help='Path to application directory.')
@click.option('--detached', is_flag=True, help='Use isolated and non-persistent context directory.')
@click.option('--env', multiple=True, help='Specify an environment variable.')
@click.option('--hostname', callback=validate_hostname, help='Service hostname.')
@click.option('--port', type=click.IntRange(1, 65535), help='Service port.')
@click.option('--priority', default=5, type=click.FloatRange(1.0, 9.0), help='Determines the service run order. Lower values run first.')
@click.option('--proxy-mode', help='''
  Proxy mode can be "regular", "transparent", "socks5",
  "reverse:SPEC", or "upstream:SPEC". For reverse and
  upstream proxy modes, SPEC is host specification in
  the form of "http[s]://host[:port]".
''')
@click.option('--quiet', is_flag=True, help='Disable log output.')
@click.option('--scheme', type=click.Choice(['http', 'https']), help='Defaults to https if hostname is set.')
@click.option('--workflow', multiple=True, type=click.Choice([WORKFLOW_MOCK_TYPE, WORKFLOW_RECORD_TYPE, WORKFLOW_TEST_TYPE]), help='Include pre-defined workflows.')
@click.argument('service_name', callback=validate_service_name)
def create(**kwargs):
  __validate_app_dir(kwargs['app_dir_path'])

  if kwargs.get("proxy_mode"):
    __validate_proxy_mode(kwargs.get("proxy_mode"))

  app = App(kwargs['app_dir_path'], DOCKER_NAMESPACE)
  service = Service(kwargs['service_name'], app)

  if not kwargs['quiet'] and os.path.exists(service.dir_path):
    print(f"{service.dir_path} already exists, updating scaffold maintained files...")

  __scaffold_build(app, **kwargs)

@service.command(
  help="List services",
  name="list"
)
@click.option('--app-dir-path', default=current_working_dir, help='Path to application directory.')
@click.option('--format', type=click.Choice(FORMATS), help='Format output.')
@click.option('--select', multiple=True, help='Select column(s) to display.')
@click.option('--service', multiple=True, help='Select specific services.')
@click.option('--without-headers', is_flag=True, default=False, help='Disable printing column headers.')
@click.option('--workflow', multiple=True, help='Specify workflow(s) to filter the services by. Defaults to all.')
def _list(**kwargs):
  app = App(kwargs['app_dir_path'], DOCKER_NAMESPACE)
  __validate_app(app)

  services = __get_services(app, service=kwargs['service'], workflow=kwargs['workflow'])

  rows = []
  for service_name in services: 
    service = Service(service_name, app)
    __validate_service_dir(service.dir_path)

    service_config = ServiceConfig(service.dir_path)
    rows.append({
      'name': service_name,
      **service_config.to_dict()
    })

  print_services(rows, **select_print_options(kwargs))

@service.command(
  help="Delete a service",
)
@click.option('--app-dir-path', default=current_working_dir, help='Path to application directory.')
@click.argument('service_name')
def delete(**kwargs):
  app = App(kwargs['app_dir_path'], DOCKER_NAMESPACE)
  __validate_app(app)

  service = Service(kwargs['service_name'], app)

  if not os.path.exists(service.dir_path):
    print(f"Service does not exist, so not deleting")
  else:
    print(f"Deleting service: {service.service_name}")
    __scaffold_delete(app, **kwargs)
    print(f"Successfully deleted service: {service.service_name}")

@service.command(
  help="Update a service config"
)
@click.option('--app-dir-path', default=current_working_dir, help='Path to application directory.')
@click.option('--hostname', callback=validate_hostname, help='Service hostname.')
@click.option('--port', type=click.IntRange(1, 65535), help='Service port.')
@click.option('--priority', default=5, type=click.FloatRange(1.0, 9.0), help='Determines the service run order. Lower values run first.')
@click.option('--scheme', type=click.Choice(['http', 'https']), help='Defaults to https if hostname is set.')
@click.option('--name', callback=validate_service_name, type=click.STRING, help='New name of the service to update to.')
@click.option('--proxy-mode', help='''
  Proxy mode can be "regular", "transparent", "socks5",
  "reverse:SPEC", or "upstream:SPEC". For reverse and
  upstream proxy modes, SPEC is host specification in
  the form of "http[s]://host[:port]".
''')
@click.argument('service_name')
def update(**kwargs):
  app = App(kwargs['app_dir_path'], DOCKER_NAMESPACE)
  __validate_app(app)

  service = Service(kwargs['service_name'], app)

  __validate_service_dir(service.dir_path)

  service_config = ServiceConfig(service.dir_path)

  if kwargs['hostname']:
    old_hostname = service_config.hostname

    if old_hostname != kwargs['hostname']:
      service_config.hostname = kwargs['hostname']

      # If this is the default proxy_mode and the origin matches the original hostname, assume it is safe to update with the new hostname
      if service_config.proxy_mode.startswith("reverse:"):
        old_origin = service_config.proxy_mode.split("reverse:")[1]
        parsed_origin_url = urlparse(old_origin)

        if old_hostname == parsed_origin_url.hostname:
          service_config.proxy_mode = service_config.proxy_mode.replace(old_hostname, service_config.hostname)

  if kwargs['priority']:
    service_config.priority = kwargs['priority']

  if kwargs['port']:
    service_config.port = kwargs['port']

  if kwargs['scheme']:
    service_config.scheme = kwargs['scheme']

  if kwargs['name']:
    old_service_name = service.service_name
    new_service_name = kwargs['name']

    print(f"Renaming service from: {old_service_name}, to: {new_service_name}")

    kwargs['service_path'] = service.dir_path
    command = ServiceUpdateCommand(app, **kwargs)
    service = command.rename(new_service_name)
    service_config = command.service_config

    print(f"Successfully renamed service to: {new_service_name}")

  if kwargs['proxy_mode']:
    __validate_proxy_mode(kwargs['proxy_mode'])
    service_config.proxy_mode = kwargs['proxy_mode']

  service_config.write()

@workflow.command(
  help="Create workflow for service(s)"
)
@click.option('--app-dir-path', default=current_working_dir, help='Path to application directory.')
@click.option('--context-dir-path', default=data_dir.context_dir_path, help='Path to Stoobly data directory.')
@click.option('--quiet', is_flag=True, help='Disable log output.')
@click.option('--service', multiple=True, help='Specify the service(s) to create the workflow for.')
@click.option('--template', required=True, type=click.Choice([WORKFLOW_MOCK_TYPE, WORKFLOW_RECORD_TYPE, WORKFLOW_TEST_TYPE]), help='Select which workflow to use as a template.')
@click.argument('workflow_name')
def create(**kwargs):
  __validate_app_dir(kwargs['app_dir_path'])

  app = App(kwargs['app_dir_path'], DOCKER_NAMESPACE, **kwargs)

  for service_name in kwargs['service']:
    config = { **kwargs }
    del config['service']
    config['service_name'] = service_name

    service = Service(service_name, app)
    __validate_service_dir(service.dir_path)

    workflow_dir_path = service.workflow_dir_path(kwargs['workflow_name'])

    if not kwargs['quiet'] and os.path.exists(workflow_dir_path):
      print(f"{workflow_dir_path} already exists, updating scaffold maintained files...")

    __workflow_create(app, **config)

@workflow.command(
  help="Copy a workflow for service(s)",
)
@click.option('--app-dir-path', default=current_working_dir, help='Path to application directory.')
@click.option('--context-dir-path', default=data_dir.context_dir_path, help='Path to Stoobly data directory.')
@click.option('--service', multiple=True, help='Specify service(s) to add the workflow to.')
@click.argument('workflow_name')
@click.argument('destination_workflow_name')
def copy(**kwargs):
  app = App(kwargs['app_dir_path'], DOCKER_NAMESPACE, **kwargs)

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
@click.option('--app-dir-path', default=current_working_dir, help='Path to application directory.')
@click.option('--context-dir-path', default=data_dir.context_dir_path, help='Path to Stoobly data directory.')
@click.option('--containerized', is_flag=True, help='Set if run from within a container.')
@click.option('--dry-run', default=False, is_flag=True)
@click.option('--extra-entrypoint-compose-path', help='Path to extra entrypoint compose file.')
@click.option('--log-level', default=INFO, type=click.Choice([DEBUG, INFO, WARNING, ERROR]), help='''
    Log levels can be "debug", "info", "warning", or "error"
''')
@click.option('--namespace', callback=validate_namespace, help='Workflow namespace.')
@click.option('--network', help='Workflow network name.')
@click.option('--rmi', is_flag=True, help='Remove images used by containers.')
@click.option('--script-path', help='Path to intermediate script path.')
@click.option('--service', multiple=True, help='Select which services to log. Defaults to all.')
@click.option('--user-id', default=os.getuid(), help='OS user ID of the owner of context dir path.')
@click.argument('workflow_name')
def down(**kwargs):  
  os.environ[env_vars.LOG_LEVEL] = kwargs['log_level']

  app = App(kwargs['app_dir_path'], DOCKER_NAMESPACE, **kwargs)
  __validate_app(app)

  __with_namespace_defaults(kwargs)

  services = __get_services(
    app, service=kwargs['service'], workflow=[kwargs['workflow_name']]
  )

  commands: List[WorkflowRunCommand] = []
  for service in services:
    config = { **kwargs }
    config['service_name'] = service
    command = WorkflowRunCommand(app, **config)
    command.current_working_dir = current_working_dir
    commands.append(command)

  script = __build_script(**kwargs)

  commands = sorted(commands, key=lambda command: command.service_config.priority)
  for index, command in enumerate(commands):
    __print_header(f"SERVICE {command.service_name}")

    extra_compose_path = None

    # By default, the entrypoint service should be last
    # However, this can change if the user has configured a service's priority to be higher
    if index == len(commands) - 1:
      extra_compose_path = kwargs['extra_entrypoint_compose_path']

    exec_command = command.down(
      extra_compose_path=extra_compose_path,
      namespace=kwargs['namespace'],
      rmi=kwargs['rmi'],
      user_id=kwargs['user_id']
    )
    if not exec_command:
      continue
    
    print(exec_command, file=script)

  # After services are stopped, their network needs to be removed
  if len(commands) > 0:
    command: WorkflowRunCommand = commands[0]

    if kwargs['rmi']:
      remove_image_command = command.remove_image(kwargs['user_id'])
      print(remove_image_command, file=script)

    remove_egress_network_command = command.remove_egress_network()
    print(remove_egress_network_command, file=script)

    remove_ingress_network_command = command.remove_ingress_network()
    print(remove_ingress_network_command, file=script)

  __run_script(script, kwargs['dry_run'])

  # Options are no longer valid
  if kwargs['containerized'] and os.path.exists(data_dir.mitmproxy_options_json_path):
    os.remove(data_dir.mitmproxy_options_json_path)

@workflow.command()
@click.option('--app-dir-path', default=current_working_dir, help='Path to application directory.')
@click.option(
  '--container', multiple=True, help=f"Select which containers to log. Defaults to '{WORKFLOW_CONTAINER_PROXY}'"
)
@click.option('--dry-run', default=False, is_flag=True, help='If set, prints commands.')
@click.option('--follow', is_flag=True, help='Follow last container log output.')
@click.option('--log-level', default=INFO, type=click.Choice([DEBUG, INFO, WARNING, ERROR]), help='''
    Log levels can be "debug", "info", "warning", or "error"
''')
@click.option('--namespace', callback=validate_namespace, help='Workflow namespace.')
@click.option('--script-path', help='Path to intermediate script path.')
@click.option('--service', multiple=True, help='Select which services to log. Defaults to all.')
@click.argument('workflow_name')
def logs(**kwargs):
  os.environ[env_vars.LOG_LEVEL] = kwargs['log_level']

  app = App(kwargs['app_dir_path'], DOCKER_NAMESPACE)
  __validate_app(app)

  __with_namespace_defaults(kwargs)

  if len(kwargs['container']) == 0:
    kwargs['container'] = [WORKFLOW_CONTAINER_PROXY]

  services = __get_services(
    app, service=kwargs['service'], without_core=True, workflow=[kwargs['workflow_name']]
  )

  commands: List[WorkflowLogCommand] = []
  for service in services:
    if len(kwargs['service']) == 0:
      # If no filter is specified, ignore CORE_SERVICES
      if service in CORE_SERVICES:
        continue
    else:
      # If a filter is specified, ignore all other services
      if service not in kwargs['service']:
        continue

    config = { **kwargs }
    config['service_name'] = service 
    command = WorkflowLogCommand(app, **config)
    commands.append(command)

  script = __build_script(**kwargs)

  commands = sorted(commands, key=lambda command: command.service_config.priority)
  for index, command in enumerate(commands):
    __print_header(f"SERVICE {command.service_name}")

    follow = kwargs['follow'] and index == len(commands) - 1
    shell_commands = command.build(
      containers=kwargs['container'], follow=follow, namespace=kwargs['namespace']
    )

    for shell_command in shell_commands:
      print(shell_command, file=script)

  __run_script(script, kwargs['dry_run'])

@workflow.command()
@click.option('--app-dir-path', default=current_working_dir, help='Path to application directory.')
@click.option('--ca-certs-dir-path', default=data_dir.ca_certs_dir_path, help='Path to ca certs directory used to sign SSL certs.')
@click.option('--certs-dir-path', help='Path to certs directory. Defaults to the certs dir of the context.')
@click.option('--containerized', is_flag=True, help='Set if run from within a container.')
@click.option('--context-dir-path', default=data_dir.context_dir_path, help='Path to Stoobly data directory.')
@click.option('--detached', is_flag=True, help='If set, will not run the highest priority service in the foreground.')
@click.option('--dry-run', default=False, is_flag=True, help='If set, prints commands.')
@click.option('--extra-entrypoint-compose-path', help='Path to extra entrypoint compose file.')
@click.option('--log-level', default=INFO, type=click.Choice([DEBUG, INFO, WARNING, ERROR]), help='''
    Log levels can be "debug", "info", "warning", or "error"
''')
@click.option('--mkcert', is_flag=True, help='Set to generate SSL certs for HTTPS services.')
@click.option('--namespace', callback=validate_namespace, help='Workflow namespace.')
@click.option('--network', help='Workflow network name.')
@click.option('--no-build', is_flag=True, help='Do not build images before starting containers.')
@click.option('--no-publish', is_flag=True, help='Do not publish all ports.')
@click.option('--pull', is_flag=True, help='Pull image before running.')
@click.option('--script-path', help='Path to intermediate script path.')
@click.option('--service', multiple=True, help='Select which services to run. Defaults to all.')
@click.option('--user-id', default=os.getuid(), help='OS user ID of the owner of context dir path.')
@click.option('--verbose', is_flag=True)
@click.option('--without-base', is_flag=True, help='Disable building Stoobly base image.')
@click.argument('workflow_name')
def up(**kwargs):
  os.environ[env_vars.LOG_LEVEL] = kwargs['log_level']

  containerized = kwargs['containerized']

  # Because we are running a docker-compose command which depends on APP_DIR env var
  # when we are running this command within a container, the host's app_dir_path will likely differ
  app_dir_path = current_working_dir if containerized else kwargs['app_dir_path']
  app = App(app_dir_path, DOCKER_NAMESPACE, **kwargs)
  __validate_app(app)

  __with_namespace_defaults(kwargs)

  services = __get_services(
    app, service=kwargs['service'], workflow=[kwargs['workflow_name']]
  )

  if kwargs['mkcert']:
    _app = ContainerizedApp(app_dir_path, DOCKER_NAMESPACE) if containerized else app
    __services_mkcert(_app, services)

  # Gateway ports are dynamically set depending on the workflow run
  workflow = Workflow(kwargs['workflow_name'], app)
  configure_gateway(workflow.workflow_name, workflow.service_paths_from_services(services), kwargs['no_publish'])

  commands: List[WorkflowRunCommand] = []
  for service in services:
    config = { **kwargs }
    config['service_name'] = service
    command = WorkflowRunCommand(app, **config)
    command.current_working_dir = current_working_dir
    commands.append(command)

  script = __build_script(**kwargs)

  # Before services can be started, their image and network needs to be created
  if len(commands) > 0:
    command: WorkflowRunCommand = commands[0]

    init_commands = []
    if not kwargs['without_base']:
      create_image_command = command.create_image(user_id=kwargs['user_id'], verbose=kwargs['verbose'])
      init_commands.append(create_image_command)

    init_commands.append(command.create_egress_network())
    init_commands.append(command.create_ingress_network())
    joined_command = ' && '.join(init_commands)

    if not containerized:
      command.write_nameservers()

    print(joined_command, file=script)

  commands = sorted(commands, key=lambda command: command.service_config.priority)
  for index, command in enumerate(commands):
    __print_header(f"SERVICE {command.service_name}")

    attached = False
    extra_compose_path = None

    # By default, the entrypoint service should be last
    # However, this can change if the user has configured a service's priority to be higher
    if index == len(commands) - 1:
      attached = not kwargs['detached']
      extra_compose_path = kwargs['extra_entrypoint_compose_path']

    exec_command = command.up(
      attached=attached,
      extra_compose_path=extra_compose_path,
      namespace=kwargs['namespace'],
      no_build=kwargs['no_build'],
      pull=kwargs['pull'],
      user_id=kwargs['user_id']
    )
    if not exec_command:
      continue

    print(exec_command, file=script)

  __run_script(script, kwargs['dry_run'])


@workflow.command(
  help="Validate a scaffold workflow"
)
@click.option('--app-dir-path', default=current_working_dir, help='Path to validate the app scaffold.')
@click.argument('workflow_name')
def validate(**kwargs):
  app = App(kwargs['app_dir_path'], DOCKER_NAMESPACE)
  __validate_app(app)

  workflow = Workflow(kwargs['workflow_name'], app)
  
  config = { **kwargs }
  config['service_name'] = 'build'

  try:
    command = WorkflowValidateCommand(app, **config)
    command.validate()
  except ScaffoldValidateException as sve:
    print(f"{bcolors.FAIL}\nFatal scaffold validation exception:{bcolors.ENDC}\n{sve}", file=sys.stderr)
    print("\nSee the scaffold workflow troubleshooting guide at: https://docs.stoobly.com/guides/how-to-integrate-e2e-testing/how-to-run-a-workflow/troubleshooting", file=sys.stderr)
    sys.exit(1)

  try:
    for service in workflow.services_ran:
      if service not in CORE_SERVICES:
        config['service_name'] = service
        command = ServiceWorkflowValidateCommand(app, **config)
        command.validate()
  except ScaffoldValidateException as sve:
    print(f"{bcolors.FAIL}\nFatal scaffold validation exception:{bcolors.ENDC}\n{sve}", file=sys.stderr)
    print("\nSee the scaffold workflow troubleshooting guide at: https://docs.stoobly.com/guides/how-to-integrate-e2e-testing/how-to-run-a-workflow/troubleshooting", file=sys.stderr)
    sys.exit(1)

  print(f"{bcolors.OKCYAN}✔ Done validating Stoobly scaffold and services, success!{bcolors.ENDC}")

@hostname.command(
  help="Update the system hosts file for all scaffold service hostnames"
)
@click.option('--app-dir-path', default=current_working_dir, help='Path to application directory.')
@click.option('--service', multiple=True, help='Select specific services. Defaults to all.')
@click.option('--workflow', multiple=True, help='Specify services by workflow(s). Defaults to all.')
def install(**kwargs):
  app = App(kwargs['app_dir_path'], DOCKER_NAMESPACE)
  __validate_app(app)

  services = __get_services(
    app, service=kwargs['service'], without_core=True, workflow=kwargs['workflow']
  )

  hostnames = []
  for service_name in services: 
    service = Service(service_name, app)
    __validate_service_dir(service.dir_path)

    service_config = ServiceConfig(service.dir_path)
    if service_config.hostname:
      hostnames.append(service_config.hostname)

  __elevate_sudo()

  try:
    hosts_file_manager = HostsFileManager()
    hosts_file_manager.install_hostnames(hostnames)
  except PermissionError:
    print("Permission denied. Please run this command with sudo.", file=sys.stderr)
    sys.exit(1)

@hostname.command(
  help="Delete from the system hosts file all scaffold service hostnames"
)
@click.option('--app-dir-path', default=current_working_dir, help='Path to application directory.')
@click.option('--service', multiple=True, help='Select specific services. Defaults to all.')
@click.option('--workflow', multiple=True, help='Specify services by workflow(s). Defaults to all.')
def uninstall(**kwargs):
  app = App(kwargs['app_dir_path'], DOCKER_NAMESPACE)
  __validate_app(app)

  services = __get_services(
    app, service=kwargs['service'], without_core=True, workflow=kwargs['workflow']
  )

  hostnames = []
  for service_name in services: 
    service = Service(service_name, app)
    __validate_service_dir(service.dir_path)

    service_config = ServiceConfig(service.dir_path)
    if service_config.hostname:
      hostnames.append(service_config.hostname)

  __elevate_sudo()

  try:
    hosts_file_manager = HostsFileManager()
    hosts_file_manager.uninstall_hostnames(hostnames)
  except PermissionError:
    print("Permission denied. Please run this command with sudo.", file=sys.stderr)
    sys.exit(1)

scaffold.add_command(app)
scaffold.add_command(service)
scaffold.add_command(workflow)
scaffold.add_command(hostname)

def __build_script(**kwargs):
  script_path = kwargs['script_path']
  if not script_path:
    script_file_name = 'run.sh'
    script_path = os.path.join(data_dir.tmp_dir_path, kwargs.get('namespace') or kwargs['workflow_name'] or '', script_file_name)
  
  script_dir = os.path.dirname(script_path)
  if not os.path.exists(script_dir):
    os.makedirs(script_dir, exist_ok=True)

  # Truncate
  with open(script_path, 'w'):
    pass

  return open(script_path, 'a')

def __elevate_sudo():
  import subprocess

  if os.geteuid() != 0:
    subprocess.run(["sudo", sys.executable] + sys.argv)
    sys.exit(0)

def __get_services(app: App, **kwargs):
  selected_services = list(kwargs['service'])

  if not selected_services:
    selected_services = app.services
  else:
    selected_services += CORE_SERVICES
    missing_services = [service for service in selected_services if service not in app.services]

    if missing_services:
      # Warn if an invalid service is provided
      Logger.instance(LOG_ID).warn(f"Service(s) {','.join(missing_services)} are not found")

    # Remove services that don't exist
      selected_services = list(set(selected_services) - set(missing_services))

  # If without_score is set, filter out CORE_SERVICES
  if kwargs.get('without_core'):
    selected_services = list(set(selected_services) - set(CORE_SERVICES))

  # If workflow is set, keep only services in the workflow
  if kwargs.get('workflow'):
    workflow_services = []
    for workflow_name in kwargs['workflow']:
      workflow = Workflow(workflow_name, app)
      workflow_services += workflow.services

    # Intersection
    selected_services = list(filter(lambda x: x in workflow_services, selected_services))

  services = list(set(selected_services))
  services.sort()
  
  return services

def __print_header(text: str):
  Logger.instance(LOG_ID).info(f"{bcolors.OKBLUE}{text}{bcolors.ENDC}")

def __run_script(script: TextIOWrapper, dry_run = False):
  script.close()

  with open(script.name, 'r') as fp:
    for line in fp:
      if not dry_run:
        exec_stream(line.strip())
      else:
        print(line.strip())

def __scaffold_build(app, **kwargs):
  command = ServiceCreateCommand(app, **kwargs)

  command.build()

def __scaffold_delete(app, **kwargs):
  command = ServiceDeleteCommand(app, **kwargs)

  command.delete()

def __services_mkcert(app: App, services):
  for service_name in services:
    service = Service(service_name, app)
    __validate_service_dir(service.dir_path)

    service_config = ServiceConfig(service.dir_path)

    if service_config.scheme != 'https':
      continue

    hostname = service_config.hostname
    
    if not hostname:
      continue

    ca = CertificateAuthority(app.ca_certs_dir_path)
    if not ca.signed(hostname, app.certs_dir_path):
      Logger.instance(LOG_ID).info(f"Creating cert for {hostname}")
      ca.sign(hostname, app.certs_dir_path)

def __validate_app(app: App):
  if not app.valid:
    print(f"Error: {app.dir_path} is not a valid scaffold app", file=sys.stderr)
    sys.exit(1)

def __validate_app_dir(app_dir_path):
  if not os.path.exists(app_dir_path):
    print(f"Error: {app_dir_path} does not exist", file=sys.stderr)
    sys.exit(1)

def __validate_service_dir(service_dir_path):
  if not os.path.exists(service_dir_path):
    print(f"Error: '{service_dir_path}' does not exist, please scaffold this service", file=sys.stderr)
    sys.exit(1)

def __validate_proxy_mode(proxy_mode: str) -> None:
  valid_exact_matches = {
    "regular": None,
    "transparent": None,
    "socks5": None,
  }

  valid_prefixes = {
    "reverse": None,
    "upstream": None
  }

  if proxy_mode in valid_exact_matches:
    return

  split_str = proxy_mode.split(":", 1)
  if len(split_str) != 2:
    print(f"Error: {proxy_mode} is invalid.", file=sys.stderr)
    sys.exit(1)

  prefix = split_str[0]
  spec = split_str[1]

  if prefix not in valid_prefixes:
    print(f"Error: {proxy_mode} is invalid.", file=sys.stderr)
    sys.exit(1)

  # TODO: validate SPEC

def __with_namespace_defaults(kwargs):
  if not kwargs.get('namespace'):
    kwargs['namespace'] = kwargs.get('workflow_name')

  # If network there was a network option, but it is not set, default network to namespace
  if 'network' in kwargs and not kwargs['network']:
    kwargs['network'] = kwargs['namespace']

def __workflow_create(app, **kwargs):
  command = WorkflowCreateCommand(app, **kwargs)

  service_config = command.service_config
  workflow_decorators = get_workflow_decorators(kwargs['template'], service_config)

  command.build(
    template=kwargs['template'],
    workflow_decorators=workflow_decorators
  )
