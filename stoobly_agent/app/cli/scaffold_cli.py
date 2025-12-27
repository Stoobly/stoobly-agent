import click
import os
import pdb
import sys


from stoobly_agent.app.cli.ca_cert_cli import ca_cert_install
from stoobly_agent.app.cli.helpers.certificate_authority import CertificateAuthority
from stoobly_agent.app.cli.scaffold.app import App
from stoobly_agent.app.cli.scaffold.app_config import AppConfig
from stoobly_agent.app.cli.scaffold.app_create_command import AppCreateCommand
from stoobly_agent.app.cli.scaffold.constants import (
  PLUGIN_CYPRESS, PLUGIN_PLAYWRIGHT, RUNTIME_LOCAL, RUNTIME_OPTIONS, SERVICES_NAMESPACE, WORKFLOW_CONTAINER_PROXY, WORKFLOW_MOCK_TYPE, WORKFLOW_RECORD_TYPE, WORKFLOW_TEST_TYPE
)
from stoobly_agent.app.cli.scaffold.containerized_app import ContainerizedApp
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
from stoobly_agent.app.cli.scaffold.workflow_namesapce import WorkflowNamespace
from stoobly_agent.app.cli.scaffold.docker.workflow.run_command import DockerWorkflowRunCommand
from stoobly_agent.app.cli.scaffold.local.workflow.run_command import LocalWorkflowRunCommand
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
@click.option('--docker-socket-path', default='/var/run/docker.sock', type=click.Path(exists=True, file_okay=True, dir_okay=False), help='Path to Docker socket.')
@click.option('--plugin', multiple=True, type=click.Choice([PLUGIN_CYPRESS, PLUGIN_PLAYWRIGHT]), help='Scaffold integrations.')
@click.option('--proxy-port', default=8080, type=click.IntRange(1, 65535), help='Proxy service port.')
@click.option('--quiet', is_flag=True, help='Disable log output.')
@click.option('--runtime', type=click.Choice(RUNTIME_OPTIONS), default=RUNTIME_LOCAL, help=f"Runtime environments to support (default: {RUNTIME_LOCAL}).")
@click.option('--ui-port', default=4200, type=click.IntRange(1, 65535), help='UI service port.')
@click.argument('app_name', callback=validate_app_name)
def create(**kwargs):
  __validate_app_dir(kwargs['app_dir_path'])

  app = App(kwargs['app_dir_path'], SERVICES_NAMESPACE)

  if not kwargs['quiet']:
    if os.path.exists(app.scaffold_namespace_path):
      print(f"{kwargs['app_dir_path']} already exists, updating scaffold maintained files...")
    else:
      print(f"Creating scaffold in {kwargs['app_dir_path']}")

  res = AppCreateCommand(app, **kwargs).build()

  for warning in res['warnings']:
    print(f"{bcolors.WARNING}WARNING{bcolors.ENDC}: {warning}")

@app.command(
  help="Scaffold app service certs"
)
@click.option('--app-dir-path', default=current_working_dir, help='Path to application directory.')
@click.option('--ca-certs-dir-path', default=data_dir.ca_certs_dir_path, help='Path to ca certs directory used to sign SSL certs.')
@click.option('--certs-dir-path', help='Path to certs directory. Defaults to the certs dir of the context.')
@click.option('--containerized', is_flag=True, help='Set if run from within a container.')
@click.option('--context-dir-path', default=data_dir.context_dir_path, help='Path to Stoobly data directory.')
@click.option('--service', multiple=True, help='Select which services to run. Defaults to all.')
@click.option('--workflow', multiple=True, help='Specify services by workflow(s). Defaults to all.')
def mkcert(**kwargs):
  containerized = kwargs['containerized']
  app_dir_path = current_working_dir if containerized else kwargs['app_dir_path']

  if containerized:
    app = ContainerizedApp(app_dir_path, SERVICES_NAMESPACE, **kwargs)
  else:
    app = App(app_dir_path, SERVICES_NAMESPACE, **kwargs)

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
@click.option('--local', is_flag=True, help='Specifies upstream service is local. Overrides `--upstream-hostname` option.')
@click.option('--port', type=click.IntRange(1, 65535), help='Service port.')
@click.option('--priority', default=5, type=click.FloatRange(1.0, 9.0), help='Determines the service run order. Lower values run first.')
@click.option('--quiet', is_flag=True, help='Disable log output.')
@click.option('--scheme', type=click.Choice(['http', 'https']), help='Defaults to https if hostname is set.')
@click.option('--upstream-hostname', callback=validate_hostname, help='Upstream service hostname.')
@click.option('--upstream-port', type=click.IntRange(1, 65535), help='Upstream service port.')
@click.option('--upstream-scheme', type=click.Choice(['http', 'https']), help='Upstream service scheme.')
@click.option('--workflow', multiple=True, type=click.Choice([WORKFLOW_MOCK_TYPE, WORKFLOW_RECORD_TYPE, WORKFLOW_TEST_TYPE]), help='Include pre-defined workflows.')
@click.argument('service_name', callback=validate_service_name)
def create(**kwargs):
  __validate_app_dir(kwargs['app_dir_path'])

  app = App(kwargs['app_dir_path'], SERVICES_NAMESPACE)
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
@click.option('--all', is_flag=True, default=False, help='Display all services including core and user defined services')
@click.option('--workflow', multiple=True, help='Specify workflow(s) to filter the services by. Defaults to all.')
def _list(**kwargs):
  app = App(kwargs['app_dir_path'], SERVICES_NAMESPACE)
  __validate_app(app)

  without_core = not kwargs['all']
  services = __get_services(app, service=kwargs['service'],  without_core=without_core, workflow=kwargs['workflow'])

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
  help="Show information about a service",
)
@click.option('--app-dir-path', default=current_working_dir, help='Path to application directory.')
@click.option('--format', type=click.Choice(FORMATS), help='Format output.')
@click.option('--without-headers', is_flag=True, default=False, help='Disable printing column headers.')
@click.argument('service_name')
@click.pass_context
def show(ctx, **kwargs):
  service_name = kwargs['service_name']
  del kwargs['service_name']
  kwargs['service'] = [service_name]

  # Invoke list with 1 service
  ctx.invoke(_list, **kwargs)

@service.command(
  help="Delete a service",
)
@click.option('--app-dir-path', default=current_working_dir, help='Path to application directory.')
@click.argument('service_name')
def delete(**kwargs):
  app = App(kwargs['app_dir_path'], SERVICES_NAMESPACE)
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
@click.option('--local', is_flag=True, help='Specifies upstream service is local. Overrides `--upstream-hostname` option.')
@click.option('--name', callback=validate_service_name, type=click.STRING, help='New name of the service to update to.')
@click.option('--port', type=click.IntRange(1, 65535), help='Service port.')
@click.option('--priority', type=click.FloatRange(1.0, 9.0), help='Determines the service run order. Lower values run first.')
@click.option('--scheme', type=click.Choice(['http', 'https']), help='Defaults to https if hostname is set.')
@click.option('--upstream-hostname', callback=validate_hostname, help='Upstream service hostname.')
@click.option('--upstream-port', type=click.IntRange(1, 65535), help='Upstream service port.')
@click.option('--upstream-scheme', type=click.Choice(['http', 'https']), help='Upstream service scheme.')
@click.argument('service_name')
def update(**kwargs):
  app = App(kwargs['app_dir_path'], SERVICES_NAMESPACE)
  __validate_app(app)

  service = Service(kwargs['service_name'], app)

  __validate_service_dir(service.dir_path)

  service_config = ServiceConfig(service.dir_path)

  service_config.local = kwargs['local']

  if kwargs['hostname']:
    service_config.hostname = kwargs['hostname']

  if kwargs['port']:
    service_config.port = kwargs['port']

  if kwargs['priority']:
    service_config.priority = kwargs['priority']

  if kwargs['scheme']:
    service_config.scheme = kwargs['scheme']

  if kwargs['upstream_hostname']:
    service_config.upstream_hostname = kwargs['upstream_hostname']

  if kwargs['upstream_port']:
    service_config.upstream_port = kwargs['upstream_port']

  if kwargs['upstream_scheme']:
    service_config.upstream_scheme = kwargs['upstream_scheme']

  if kwargs['name']:
    old_service_name = service.service_name
    new_service_name = kwargs['name']

    print(f"Renaming service from: {old_service_name}, to: {new_service_name}")

    kwargs['service_path'] = service.dir_path
    command = ServiceUpdateCommand(app, **kwargs)
    service = command.rename(new_service_name)
    service_config = command.service_config

    print(f"Successfully renamed service to: {new_service_name}")

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

  app = App(kwargs['app_dir_path'], SERVICES_NAMESPACE, **kwargs)

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
  app = App(kwargs['app_dir_path'], SERVICES_NAMESPACE, **kwargs)

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
@click.option('--hostname-uninstall-confirm', default=None, type=click.Choice(['y', 'Y', 'n', 'N']), help='Confirm answer to hostname uninstall prompt.')
@click.option('--log-level', default=INFO, type=click.Choice([DEBUG, INFO, WARNING, ERROR]), help='''
    Log levels can be "debug", "info", "warning", or "error"
''')
@click.option('--namespace', callback=validate_namespace, help='Workflow namespace.')
@click.option('--script-path', help='Path to intermediate script path.')
@click.option('--service', multiple=True, help='Select which services to log. Defaults to all.')
@click.option('--user-id', default=os.getuid(), help='OS user ID of the owner of context dir path.')
@click.argument('workflow_name')
def down(**kwargs):
  os.environ[env_vars.LOG_LEVEL] = kwargs['log_level']

  containerized = kwargs['containerized']

  app_dir_path = current_working_dir if containerized else kwargs['app_dir_path']
  app = App(app_dir_path, SERVICES_NAMESPACE, **kwargs)
  __validate_app(app)

  __with_namespace_defaults(kwargs)

  services = __get_services(
    app, service=kwargs['service'], workflow=[kwargs['workflow_name']]
  )

  script = __build_script(app, **kwargs)
  
  # Determine which workflow command to use based on app configuration
  app_config = AppConfig(app.scaffold_namespace_path)
  if app_config.runtime_local:
    # Use LocalWorkflowRunCommand for local execution
    workflow_command = LocalWorkflowRunCommand(
      app, 
      services=services, 
      script=script,
      **kwargs
    )
  else:
    # Use DockerWorkflowRunCommand for Docker execution
    workflow_command = DockerWorkflowRunCommand(
      app, 
      services=services, 
      script=script,
      **kwargs
    )

  if not containerized and not kwargs['dry_run']:
    if app_config.runtime_docker:
      # Because test workflow is completely containerized, we don't need to prompt to install hostnames in /etc/hosts
      # Entrypoint container will be within the container network
      if workflow_command.workflow_template != WORKFLOW_TEST_TYPE:
          # Prompt confirm to install hostnames
          if kwargs.get('hostname_uninstall_confirm'):
            confirm = kwargs['hostname_uninstall_confirm']
          else:
            confirm = input(f"Do you want to uninstall hostnames for {kwargs['workflow_name']}? (y/N) ")

          if confirm == "y" or confirm == "Y":
            __hostname_uninstall(app_dir_path=kwargs['app_dir_path'], service=kwargs['service'], workflow=[kwargs['workflow_name']])

  # Execute the workflow down
  command_args = { 'print_service_header': lambda service_name: __print_header(f"Step {service_name}") }
  workflow_command.down(
    **command_args,
    **kwargs
  )

  # Options are no longer valid
  if kwargs['containerized'] and os.path.exists(data_dir.mitmproxy_options_json_path):
    os.remove(data_dir.mitmproxy_options_json_path)

@workflow.command()
@click.option('--app-dir-path', default=current_working_dir, help='Path to application directory.')
@click.option(
  '--container', multiple=True, help=f"Select which containers to log. Defaults to '{WORKFLOW_CONTAINER_PROXY}'"
)
@click.option('--containerized', is_flag=True, help='Set if run from within a container.')
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

  app_dir_path = current_working_dir if kwargs['containerized'] else kwargs['app_dir_path']
  app = App(app_dir_path, SERVICES_NAMESPACE, **kwargs)
  __validate_app(app)

  __with_namespace_defaults(kwargs)

  if len(kwargs['container']) == 0:
    kwargs['container'] = [WORKFLOW_CONTAINER_PROXY]

  services = __get_services(
    app, service=kwargs['service'], without_core=True, workflow=[kwargs['workflow_name']]
  )

  script = __build_script(app, **kwargs)
  
  # Determine which workflow command to use based on app configuration
  app_config = AppConfig(app.scaffold_namespace_path)
  if app_config.runtime_local:
    # Use LocalWorkflowRunCommand for local execution
    workflow_command = LocalWorkflowRunCommand(
      app, 
      services=services,
      script=script,
      **kwargs
    )
  else:
    # Use DockerWorkflowRunCommand for Docker execution
    workflow_command = DockerWorkflowRunCommand(
      app, 
      services=services,
      script=script,
      **kwargs
    )

  # Execute the workflow logs
  command_args = { 'print_service_header': lambda service_name: __print_header(f"SERVICE {service_name}") }
  workflow_command.logs(
    **command_args,
    **kwargs
  )

@workflow.command()
@click.option('--app-dir-path', default=current_working_dir, help='Path to application directory.')
@click.option('--ca-certs-dir-path', default=data_dir.ca_certs_dir_path, help='Path to ca certs directory used to sign SSL certs.')
@click.option('--ca-certs-install-confirm', default=None, type=click.Choice(['y', 'Y', 'n', 'N']), help='Confirm answer to CA certificate installation prompt.')
@click.option('--certs-dir-path', help='Path to certs directory. Defaults to the certs dir of the context.')
@click.option('--containerized', is_flag=True, help='Set if run from within a container.')
@click.option('--context-dir-path', default=data_dir.context_dir_path, help='Path to Stoobly data directory.')
@click.option('--detached', is_flag=True, help='If set, will run the highest priority service in the background.')
@click.option('--dry-run', default=False, is_flag=True, help='If set, prints commands.')
@click.option('--hostname-install-confirm', default=None, type=click.Choice(['y', 'Y', 'n', 'N']), help='Confirm answer to hostname installation prompt.')
@click.option('--log-level', default=INFO, type=click.Choice([DEBUG, INFO, WARNING, ERROR]), help='''
    Log levels can be "debug", "info", "warning", or "error"
''')
@click.option('--namespace', callback=validate_namespace, help='Workflow namespace.')
@click.option('--no-publish', is_flag=True, help='Do not publish all ports.')
@click.option('--script-path', help='Path to intermediate script path.')
@click.option('--service', multiple=True, help='Select which services to run. Defaults to all.')
@click.option('--user-id', default=os.getuid(), help='OS user ID of the owner of context dir path.')
@click.option('--verbose', is_flag=True)
@click.argument('workflow_name')
def up(**kwargs):
  os.environ[env_vars.LOG_LEVEL] = kwargs['log_level']

  containerized = kwargs['containerized']
  dry_run = kwargs['dry_run']

  # Because we are running a docker-compose command which depends on APP_DIR env var
  # when we are running this command within a container, the host's app_dir_path will likely differ
  # It needs to differ because if containerized, we are generating .env with contents from the host
  app_dir_path = current_working_dir if containerized else kwargs['app_dir_path']
  app = App(app_dir_path, SERVICES_NAMESPACE, **kwargs)
  __validate_app(app)

  __with_namespace_defaults(kwargs)

  # Determine which workflow command to use based on app configuration
  services = __get_services(
    app, service=kwargs['service'], workflow=[kwargs['workflow_name']]
  )
  script = __build_script(app, **kwargs)

  app_config = AppConfig(app.scaffold_namespace_path)
  if app_config.runtime_local:
    # Use LocalWorkflowRunCommand for local execution
    workflow_command = LocalWorkflowRunCommand(
      app, 
      services=services, 
      script=script,
      **kwargs
    )
  else:
    # Use DockerWorkflowRunCommand for Docker execution
    workflow_command = DockerWorkflowRunCommand(
      app, 
      services=services, 
      script=script,
      **kwargs
    )

  if not containerized and not dry_run:
    # First time running the up command if ca certs folder does not exist or is empty
    first_time = not os.path.exists(app.ca_certs_dir_path) or not os.listdir(app.ca_certs_dir_path)

    if first_time:
      # To improve FTUE, prompt install CA certificate for record workflow
      if workflow_command.workflow_template == WORKFLOW_RECORD_TYPE:
        # Install CA certs for record workflow
        __prompt_ca_cert_install(
          app,
          workflow_name=kwargs['workflow_name'],
          ca_certs_install_confirm=kwargs.get('ca_certs_install_confirm')
        )

    if app_config.runtime_docker:
      # To improve UX, prompt install hostnames for record and mock workflows
      # Because test workflow is complete containerized, we don't need to prompt to install hostnames in /etc/hosts
      # Entrypoint container will be within the container network
      if workflow_command.workflow_template != WORKFLOW_TEST_TYPE:
        # Prompt confirm to install hostnames
        if kwargs.get('hostname_install_confirm'):
          confirm = kwargs['hostname_install_confirm']
        else:
          confirm = input(f"Do you want to install hostnames for {kwargs['workflow_name']}? (y/N) ")

        if confirm == "y" or confirm == "Y":
          __hostname_install(app_dir_path=kwargs['app_dir_path'], service=kwargs['service'], workflow=[kwargs['workflow_name']])

    options = {}

    if os.getcwd() != app_dir_path:
      options['app_dir_path'] = app_dir_path

    if kwargs['namespace'] != kwargs['workflow_name']:
      options['namespace'] = kwargs['namespace']

    options_str = ' '.join([f"--{key} {value}" for key, value in options.items()])
    if options_str:
      options_str = f" {options_str}"

    Logger.instance(LOG_ID).info(f"To view logs, run `stoobly-agent workflow logs{options_str} {kwargs['workflow_name']}`")
  
  # Execute the workflow
  command_args = { 'print_service_header': lambda service_name: __print_header(f"SERVICE {service_name}") }
  workflow_command.up(
    **command_args,
    **kwargs
  )

@workflow.command(
  help="Validate a scaffold workflow"
)
@click.option('--app-dir-path', default=current_working_dir, help='Path to validate the app scaffold.')
@click.argument('workflow_name')
def validate(**kwargs):
  app = App(kwargs['app_dir_path'], SERVICES_NAMESPACE)
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
  __hostname_install(**kwargs)

@hostname.command(
  help="Delete from the system hosts file all scaffold service hostnames"
)
@click.option('--app-dir-path', default=current_working_dir, help='Path to application directory.')
@click.option('--service', multiple=True, help='Select specific services. Defaults to all.')
@click.option('--workflow', multiple=True, help='Specify services by workflow(s). Defaults to all.')
def uninstall(**kwargs):
  __hostname_uninstall(**kwargs)

scaffold.add_command(app)
scaffold.add_command(service)
scaffold.add_command(workflow)
scaffold.add_command(hostname)

def __prompt_ca_cert_install(app: App, workflow_name: str, ca_certs_install_confirm: str = None):
  """Prompt user to install CA certificate for record workflow."""

  if ca_certs_install_confirm:
    confirm = ca_certs_install_confirm
  else:
    confirm = input(f"Installing CA certificate is required for {workflow_name}ing requests, continue? (y/N) ")

  if confirm == "y" or confirm == "Y":
    ca_cert_install(app.ca_certs_dir_path)
  else:
    print("You can install the CA certificate later by running: stoobly-agent ca-cert install")

def __build_script(app: App, **kwargs):
  script_path = kwargs['script_path']
  if not script_path:
    workflow_namespace = WorkflowNamespace(app, kwargs.get('namespace') or kwargs['workflow_name'])
    script_path = workflow_namespace.run_script_path
  
  script_dir = os.path.dirname(script_path)
  if not os.path.exists(script_dir):
    os.makedirs(script_dir, exist_ok=True)

  # Truncate
  with open(script_path, 'w'):
    pass

  return open(script_path, 'a')

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

def __get_hostnames(**kwargs):
  """Get list of hostnames from services in the workflow."""
  app = App(kwargs['app_dir_path'], SERVICES_NAMESPACE)
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

  return hostnames

def __run_hostname_command_with_sudo(action: str, **kwargs):
  """Run hostname install/uninstall command with sudo if not root."""
  import subprocess

  cmd = [
    "sudo", sys.executable, sys.argv[0],
    "scaffold", "hostname", action,
    "--app-dir-path", kwargs['app_dir_path']
  ]
  for workflow_name in kwargs.get('workflow', []):
    cmd.extend(["--workflow", workflow_name])
  for service_name in kwargs.get('service', []):
    cmd.extend(["--service", service_name])

  result = subprocess.run(cmd)
  if result.returncode != 0:
    sys.exit(result.returncode)

def __hostname_install(**kwargs):
  hostnames = __get_hostnames(**kwargs)
  if not hostnames:
    return

  if os.geteuid() != 0:
    __run_hostname_command_with_sudo("install", **kwargs)
  else:
    try:
      hosts_file_manager = HostsFileManager()
      hosts_file_manager.install_hostnames(hostnames)
    except PermissionError:
      print("Permission denied. Please run this command with sudo.", file=sys.stderr)
      sys.exit(1)

def __hostname_uninstall(**kwargs):
  hostnames = __get_hostnames(**kwargs)
  if not hostnames:
    return

  if os.geteuid() != 0:
    __run_hostname_command_with_sudo("uninstall", **kwargs)
  else:
    try:
      hosts_file_manager = HostsFileManager()
      hosts_file_manager.uninstall_hostnames(hostnames)
    except PermissionError:
      print("Permission denied. Please run this command with sudo.", file=sys.stderr)
      sys.exit(1)

def __print_header(text: str):
  Logger.instance(LOG_ID).info(f"{bcolors.OKBLUE}{text}{bcolors.ENDC}")

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
  __validate_dir(app_dir_path)

def __validate_dir(dir_path):
  if not os.path.exists(dir_path):
    print(f"Error: {dir_path} does not exist", file=sys.stderr)
    sys.exit(1)

def __validate_service_dir(service_dir_path):
  if not os.path.exists(service_dir_path):
    print(f"Error: '{service_dir_path}' does not exist, please scaffold this service", file=sys.stderr)
    sys.exit(1)

def __with_namespace_defaults(kwargs):
  if not kwargs.get('namespace'):
    kwargs['namespace'] = kwargs.get('workflow_name')

def __workflow_create(app, **kwargs):
  command = WorkflowCreateCommand(app, **kwargs)

  service_config = command.service_config
  workflow_decorators = get_workflow_decorators(kwargs['template'], service_config)

  command.build(
    template=kwargs['template'],
    workflow_decorators=workflow_decorators
  )

def __with_workflow_namespace(app: App, namespace: str):
  workflow_namespace = WorkflowNamespace(app, namespace)
  workflow_namespace.copy_dotenv()
  return workflow_namespace