import click
import docker
import os
import pdb
import sys

from datetime import datetime, timezone
from docker import errors as docker_errors

from stoobly_agent.app.cli.ca_cert_cli import ca_cert_install
from stoobly_agent.app.cli.helpers.certificate_authority import CertificateAuthority
from stoobly_agent.app.cli.scaffold.app import App
from stoobly_agent.app.cli.scaffold.app_config import AppConfig
from stoobly_agent.app.cli.scaffold.app_create_command import AppCreateCommand
from stoobly_agent.app.cli.scaffold.constants import (
  PLUGIN_CYPRESS, PLUGIN_PLAYWRIGHT, PROXY_MODE_FORWARD, PROXY_MODE_REVERSE, RUNTIME_DOCKER, RUNTIME_LOCAL, RUNTIME_OPTIONS, WORKFLOW_MOCK_TYPE, WORKFLOW_NORMALIZE_TYPE, WORKFLOW_RECORD_TYPE, WORKFLOW_TEST_TYPE
)
from stoobly_agent.app.cli.scaffold.docker.workflow.decorators_factory import get_workflow_decorators
from stoobly_agent.app.cli.scaffold.hosts_file_manager import HostsFileManager
from stoobly_agent.app.cli.scaffold.rewrite import apply_upstream_url_rewrite
from stoobly_agent.app.cli.scaffold.service import Service
from stoobly_agent.app.cli.scaffold.service_config import ServiceConfig
from stoobly_agent.app.cli.scaffold.service_create_command import ServiceCreateCommand
from stoobly_agent.app.cli.scaffold.service_delete_command import ServiceDeleteCommand
from stoobly_agent.app.cli.scaffold.service_update_command import ServiceUpdateCommand
from stoobly_agent.app.cli.scaffold.service_workflow_validate_command import ServiceWorkflowValidateCommand
from stoobly_agent.app.cli.scaffold.templates.constants import CORE_SERVICES_DOCKER
from stoobly_agent.app.cli.scaffold.validate_exceptions import ScaffoldValidateException
from stoobly_agent.app.cli.scaffold.workflow import Workflow
from stoobly_agent.app.cli.scaffold.workflow_create_command import WorkflowCreateCommand
from stoobly_agent.app.cli.scaffold.workflow_copy_command import WorkflowCopyCommand
from stoobly_agent.app.cli.scaffold.workflow_config import WorkflowConfig
from stoobly_agent.app.cli.scaffold.workflow_namespace import WorkflowNamespace
from stoobly_agent.app.cli.scaffold.docker.workflow.run_command import DockerWorkflowRunCommand
from stoobly_agent.app.cli.scaffold.local.workflow.run_command import LocalWorkflowRunCommand
from stoobly_agent.app.cli.scaffold.workflow_validate_command import WorkflowValidateCommand
from stoobly_agent.app.models.factories.resource.local_db.helpers.snapshot_scenarios_since_service import snapshot_scenarios_since
from stoobly_agent.app.settings import Settings
from stoobly_agent.app.cli.scaffold.workflow_filter import (
  HTTP_METHODS,
  build_include_filter_rule_for_service_url,
  upsert_filter_rule,
  workflow_template_to_filter_mode,
)
from stoobly_agent.config.constants import env_vars
from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.lib.api.keys.project_key import ProjectKey
from stoobly_agent.lib.logger import bcolors, DEBUG, ERROR, INFO, Logger, WARNING

from .helpers.print_service import FORMATS, print_services, select_print_options
from .scaffold_request_log_cli import request
from .validators.scaffold import validate_app_name, validate_hostname, validate_namespace, validate_service_name

LOG_ID = 'Scaffold'

data_dir: DataDir = DataDir.instance()
context_dir_path = data_dir.context_dir_path

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
@click.option('--app-dir-path', default=os.getcwd(), help='Path to create the app scaffold.')
@click.option('--copy-on-workflow-up', is_flag=True, help='Copy app scaffold from --app-dir-path to isolated tmp path on workflow up.')
@click.option('--docker-socket-path', default='/var/run/docker.sock', type=click.Path(exists=True, file_okay=True, dir_okay=False), help='Path to Docker socket.')
@click.option('--plugin', multiple=True, type=click.Choice([PLUGIN_CYPRESS, PLUGIN_PLAYWRIGHT]), help='Scaffold integrations.')
@click.option('--proxy-mode', default=PROXY_MODE_FORWARD, type=click.Choice([PROXY_MODE_FORWARD, PROXY_MODE_REVERSE]), help='Determines how to proxy requests to the upstream service(s).')
@click.option('--proxy-port', default=8080, type=click.IntRange(1, 65535), help='Proxy service port.')
@click.option('--quiet', is_flag=True, help='Disable log output.')
@click.option('--runtime', type=click.Choice(RUNTIME_OPTIONS), default=RUNTIME_LOCAL, help=f"Runtime environments to support (default: {RUNTIME_LOCAL}).")
@click.option('--ui-port', default=4200, type=click.IntRange(1, 65535), help='UI service port.')
@click.argument('app_name', callback=validate_app_name)
def create(**kwargs):
  # Validate that reverse proxy mode is only used with docker runtime
  if kwargs.get('runtime') == RUNTIME_LOCAL and kwargs.get('proxy_mode') == PROXY_MODE_REVERSE:
    error_message = f"Error: {PROXY_MODE_REVERSE.capitalize()} proxy mode is only supported for {RUNTIME_DOCKER} runtime."
    click.echo(error_message, err=True)
    sys.exit(1)

  # Validate copy-on-workflow-up can only be used with docker runtime
  # This flag is meant to support parallel workflow runs. However ports will conflict for local runtime.
  if kwargs.get('runtime') != RUNTIME_DOCKER and kwargs.get('copy_on_workflow_up'):
    error_message = f"Error: --copy-on-workflow-up is only supported for {RUNTIME_DOCKER} runtime."
    click.echo(error_message, err=True)
    sys.exit(1)

  __validate_app_dir(kwargs['app_dir_path'])

  app = App(kwargs['app_dir_path'])

  if not kwargs['quiet']:
    if os.path.exists(app.scaffold_namespace_path):
      print(f"{kwargs['app_dir_path']} already exists, updating scaffold maintained files...")
    else:
      print(f"Creating scaffold in {kwargs['app_dir_path']}")

  res = AppCreateCommand(app, **kwargs).build()

  for warning in res['warnings']:
    print(f"{bcolors.WARNING}WARNING{bcolors.ENDC}: {warning}")

@service.command(
  help="Scaffold a service",
)
@click.option('--app-dir-path', default=context_dir_path, help='Path to application directory.')
@click.option('--detached', is_flag=True, help='Use isolated and non-persistent context directory.')
@click.option('--env', multiple=True, help='Specify an environment variable.')
@click.option('--hostname', callback=validate_hostname, help='Service hostname.')
@click.option('--local', is_flag=True, help='Specifies upstream service is local. Overrides `--upstream-hostname` option.')
@click.option('--openapi-specification', is_flag=True, help='Enable using OpenAPI specification for this service.')
@click.option('--port', type=click.IntRange(1, 65535), help='Service port.')
@click.option('--priority', default=5, type=click.FloatRange(1.0, 9.0), help='Determines the service run order. Lower values run first.')
@click.option('--quiet', is_flag=True, help='Disable log output.')
@click.option('--scheme', type=click.Choice(['http', 'https']), help='Defaults to https if hostname is set.')
@click.option('--upstream-hostname', callback=validate_hostname, help='Upstream service hostname.')
@click.option('--upstream-port', type=click.IntRange(1, 65535), help='Upstream service port.')
@click.option('--upstream-scheme', type=click.Choice(['http', 'https']), help='Upstream service scheme.')
@click.option('--workflow', multiple=True, type=click.Choice([WORKFLOW_MOCK_TYPE, WORKFLOW_NORMALIZE_TYPE, WORKFLOW_RECORD_TYPE, WORKFLOW_TEST_TYPE]), help='Include pre-defined workflows.')
@click.argument('service_name', callback=validate_service_name)
def create(**kwargs):
  __validate_app_dir(kwargs['app_dir_path'])

  app = App(kwargs['app_dir_path'])
  service = Service(kwargs['service_name'], app)

  if not kwargs['quiet'] and os.path.exists(service.dir_path):
    print(f"{service.dir_path} already exists, updating scaffold maintained files...")

  __scaffold_build(app, **kwargs)

@service.command(
  help="List services",
  name="list"
)
@click.option('--app-dir-path', default=context_dir_path, help='Path to application directory.')
@click.option('--format', type=click.Choice(FORMATS), help='Format output.')
@click.option('--select', multiple=True, help='Select column(s) to display.')
@click.option('--service', multiple=True, help='Select specific services.')
@click.option('--without-headers', is_flag=True, default=False, help='Disable printing column headers.')
@click.option('--all', is_flag=True, default=False, help='Display all services including core and user defined services')
@click.option('--workflow', multiple=True, help='Specify workflow(s) to filter the services by. Defaults to all.')
def _list(**kwargs):
  app = App(kwargs['app_dir_path'])
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
@click.option('--app-dir-path', default=context_dir_path, help='Path to application directory.')
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
@click.option('--app-dir-path', default=context_dir_path, help='Path to application directory.')
@click.argument('service_name')
def delete(**kwargs):
  app = App(kwargs['app_dir_path'])
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
@click.option('--app-dir-path', default=context_dir_path, help='Path to application directory.')
@click.option('--detached', type=bool, default=None, help='Use isolated and non-persistent context directory.')
@click.option('--hostname', callback=validate_hostname, help='Service hostname.')
@click.option('--local', type=bool, default=None, help='Specifies upstream service is local. Overrides `--upstream-hostname` option.')
@click.option('--name', callback=validate_service_name, type=click.STRING, help='New name of the service to update to.')
@click.option('--openapi-specification', type=bool, default=None, help='Enable using OpenAPI specification for this service.')
@click.option('--port', type=click.IntRange(1, 65535), help='Service port.')
@click.option('--priority', type=click.FloatRange(1.0, 9.0), help='Determines the service run order. Lower values run first.')
@click.option('--scheme', type=click.Choice(['http', 'https']), help='Defaults to https if hostname is set.')
@click.option('--upstream-hostname', callback=validate_hostname, help='Upstream service hostname.')
@click.option('--upstream-port', type=click.IntRange(1, 65535), help='Upstream service port.')
@click.option('--upstream-scheme', type=click.Choice(['http', 'https']), help='Upstream service scheme.')
@click.argument('service_name')
def update(**kwargs):
  app = App(kwargs['app_dir_path'])
  __validate_app(app)

  service = Service(kwargs['service_name'], app)

  __validate_service_dir(service.dir_path)

  service_config = ServiceConfig(service.dir_path)

  # If false and service_config.detached is True, then ask for confirmation
  if kwargs['detached'] != None:
      service_config.detached = kwargs['detached']

  if kwargs['hostname']:
    service_config.hostname = kwargs['hostname']

  if kwargs['local'] != None:
    service_config.local = kwargs['local']

  if kwargs['port']:
    service_config.port = kwargs['port']

  if kwargs['priority']:
    service_config.priority = kwargs['priority']

  if kwargs['openapi_specification'] != None:
    service_config.openapi_specification = kwargs['openapi_specification']

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
@click.option('--app-dir-path', default=context_dir_path, help='Path to application directory.')
@click.option('--context-dir-path', default=data_dir.context_dir_path, help='Path to Stoobly data directory.')
@click.option('--quiet', is_flag=True, help='Disable log output.')
@click.option('--service', multiple=True, help='Specify the service(s) to create the workflow for.')
@click.option('--template', required=True, type=click.Choice([WORKFLOW_MOCK_TYPE, WORKFLOW_NORMALIZE_TYPE, WORKFLOW_RECORD_TYPE, WORKFLOW_TEST_TYPE]), help='Select which workflow to use as a template.')
@click.argument('workflow_name')
def create(**kwargs):
  __validate_app_dir(kwargs['app_dir_path'])

  app = App(kwargs['app_dir_path'], **kwargs)

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
@click.option('--app-dir-path', default=context_dir_path, help='Path to application directory.')
@click.option('--context-dir-path', default=data_dir.context_dir_path, help='Path to Stoobly data directory.')
@click.option('--service', multiple=True, help='Specify service(s) to add the workflow to.')
@click.argument('workflow_name')
@click.argument('destination_workflow_name')
def copy(**kwargs):
  app = App(kwargs['app_dir_path'], **kwargs)

  for service_name in kwargs['service']:
    config = { **kwargs }
    del config['service']
    config['service_name'] = service_name

    command = WorkflowCopyCommand(app, **config)

    if not command.app_dir_exists:
      print(f"Error: {command.app_dir_path} does not exist", file=sys.stderr)
      sys.exit(1)

    command.copy(kwargs['destination_workflow_name'])

@workflow.command(
  help="Show information about running workflow(s)"
)
@click.option('--app-dir-path', default=context_dir_path, help='Path to application directory.')
@click.option('--namespace', callback=validate_namespace, help='Workflow namespace. Only valid when workflow_name is provided.')
@click.option('--verbose', '-v', is_flag=True, default=False, help='Show detailed information.')
@click.argument('workflow_name', required=False, default=None)
def show(**kwargs):
  app = App(kwargs['app_dir_path'])
  __validate_app(app)

  workflow_name = kwargs.get('workflow_name')
  namespace = kwargs.get('namespace')

  if namespace and not workflow_name:
    click.echo("Error: --namespace requires a workflow_name argument.")
    sys.exit(1)

  app_config = AppConfig(app.scaffold_namespace_path)
  verbose = kwargs.get('verbose', False)

  found_workflows = __find_running_workflows(app, app_config)

  if workflow_name:
    found_workflows = [w for w in found_workflows if w['workflow_name'] == workflow_name]
    if namespace:
      found_workflows = [w for w in found_workflows if w['namespace'] == namespace]

  if not found_workflows:
    if workflow_name and namespace:
      click.echo(f"No running workflow found for '{workflow_name}' with namespace '{namespace}'.")
    elif workflow_name:
      click.echo(f"No running workflow found for '{workflow_name}'.")
    else:
      click.echo("No workflows are currently running.")
    return

  for workflow_info in found_workflows:
    __print_workflow_status(workflow_info, app, app_config, verbose)
    if len(found_workflows) > 1:
      click.echo()  # Blank line between multiple workflows

@workflow.command(
  help="Stop and tear down a scaffold workflow",
)
@click.option('--app-dir-path', default=context_dir_path, help='Path to application directory.')
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
  __with_namespace_defaults(kwargs)

  app = App(context_dir_path, **kwargs) if containerized else App(kwargs['app_dir_path'], **kwargs)
  __validate_app(app)

  services = __get_services(
    app, service=kwargs['service'], workflow=[kwargs['workflow_name']]
  )

  script = __build_script(app, **kwargs)
  
  # Determine which workflow command to use based on app configuration
  workflow_namespace = WorkflowNamespace(app, kwargs['namespace'])
  app_config = AppConfig(app.scaffold_namespace_path)

  if app_config.copy_on_workflow_up:
    app.denormalize_configure(workflow_namespace)

  # UTC ISO-8601 instant used as updated_since when snapshotting scenarios on down (non-test workflows).
  # Local: PID file ctime (approximates when the marker was written for the detached run).
  # Docker: Unix epoch seconds from the workflow .timestamp file (see DockerWorkflowRunCommand.__create_timestamp_file);
  #   if read/parse fails, falls back to that file's ctime. Left unset when the marker file is absent.
  workflow_up_timestamp = None

  if app_config.runtime_local:
    # Use LocalWorkflowRunCommand for local execution
    workflow_command = LocalWorkflowRunCommand(
      app, 
      services=services, 
      script=script,
      **kwargs
    )

    pid_file_path = workflow_command.pid_file_path
    if os.path.exists(pid_file_path):
      workflow_up_timestamp = datetime.fromtimestamp(
        os.path.getctime(pid_file_path),
        tz=timezone.utc
      ).isoformat()
  else:
    # Use DockerWorkflowRunCommand for Docker execution
    workflow_command = DockerWorkflowRunCommand(
      app, 
      services=services, 
      script=script,
      **kwargs
    )

    timestamp_file_path = workflow_command.timestamp_file_path
    if os.path.exists(timestamp_file_path):
      try:
        with open(timestamp_file_path, 'r') as f:
          unix_ts = float(f.read().strip())
      except (OSError, ValueError) as e:
        Logger.instance(LOG_ID).warning(
          f"Could not read workflow timestamp from {timestamp_file_path}: {e}; using file ctime"
        )
        unix_ts = os.path.getctime(timestamp_file_path)
      workflow_up_timestamp = datetime.fromtimestamp(unix_ts, tz=timezone.utc).isoformat()

  # Snapshot / hostname steps must not skip workflow teardown: down() runs in finally.
  try:
    # Persist snapshots for scenarios updated at or after workflow_up_timestamp (snapshot_scenarios_since).
    if workflow_command.workflow_template != WORKFLOW_TEST_TYPE and not kwargs['dry_run']:
      if workflow_up_timestamp:
        try:
          snapshot_results = snapshot_scenarios_since(workflow_up_timestamp)

          for snapshot_result in snapshot_results:
            scenario = snapshot_result[0]
            scenario_key = scenario.get('key')
            scenario_name = scenario.get('name')

            Logger.instance(LOG_ID).info(
              f"{bcolors.OKBLUE}Created{bcolors.ENDC} snapshot for scenario {scenario_key} {scenario_name}"
            )
        except Exception as e:
          Logger.instance(LOG_ID).warning(
            f"Snapshotting scenarios before workflow down failed: {e}"
          )

    if not containerized and not kwargs['dry_run']:
      if app_config.runtime_docker:
        # Because test workflow is completely containerized, we don't need to prompt to install hostnames in /etc/hosts
        # Entrypoint container will be within the container network
        if workflow_command.workflow_template != WORKFLOW_TEST_TYPE:
          try:
            # Prompt confirm to install hostnames
            __hostname_uninstall_with_prompt(
                app_dir_path=kwargs['app_dir_path'],
                hostname_uninstall_confirm=kwargs.get('hostname_uninstall_confirm'),
                service=kwargs['service'],
                validate=True,
                workflow=[kwargs['workflow_name']],
              )
          except Exception as e:
            Logger.instance(LOG_ID).warning(
              f"Hostname uninstall before workflow down failed: {e}"
            )

  finally:
    # Execute the workflow down
    command_args = { 'print_service_header': lambda service_name: __print_header(f"SERVICE {service_name}") }
    workflow_command.down(
      **command_args,
      **kwargs
    )

  # Options are no longer valid (after successful down; still run if pre-down work failed)
  if containerized and os.path.exists(data_dir.mitmproxy_options_json_path):
    os.remove(data_dir.mitmproxy_options_json_path)

@workflow.command(
  help="Show or follow logs from workflow service(s)",
)
@click.option('--app-dir-path', default=context_dir_path, help='Path to application directory.')
@click.option(
  '--container', multiple=True, help=f"Select which containers to log."
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

  containerized = kwargs['containerized']
  __with_namespace_defaults(kwargs)

  app = App(context_dir_path, **kwargs) if containerized else App(kwargs['app_dir_path'], **kwargs)
  __validate_app(app)

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

  # Execute the workflow logs
  command_args = { 'print_service_header': lambda service_name: __print_header(f"SERVICE {service_name}") }
  workflow_command.logs(
    **command_args,
    **kwargs
  )

@workflow.command(
  help="Start a scaffold workflow and bring up service(s)",
)
@click.option('--app-dir-path', default=context_dir_path, help='Path to application directory.')
@click.option('--ca-certs-dir-path', default=None, help='Path to ca certs directory used to sign SSL certs. Defaults to the ca_certs dir of the context.')
@click.option('--ca-certs-install-confirm', default=None, type=click.Choice(['y', 'Y', 'n', 'N']), help='Confirm answer to CA certificate installation prompt.')
@click.option('--certs-dir-path', help='Path to certs directory. Defaults to the certs dir of the context.')
@click.option('--containerized', is_flag=True, help='Set if run from within a container.')
@click.option('--context-dir-path', default=data_dir.context_dir_path, help='Path to Stoobly data directory.')
@click.option('--detached', is_flag=True, help='If set, will run the highest priority service in the background.')
@click.option('--dry-run', default=False, is_flag=True, help='If set, prints commands instead of running them.')
@click.option('--hostname-install-confirm', default=None, type=click.Choice(['y', 'Y', 'n', 'N']), help='Confirm answer to hostname installation prompt.')
@click.option('--log-level', default=INFO, type=click.Choice([DEBUG, INFO, WARNING, ERROR]), help='''
    Log levels can be "debug", "info", "warning", or "error"
''')
@click.option('--mkcert', is_flag=True, help='Set to generate SSL certs for HTTPS services.')
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
  __with_namespace_defaults(kwargs)

  # Because we are running a docker-compose command which depends on APP_DIR env var
  # when we are running this command within a container, the host's app_dir_path will likely differ
  # It needs to differ because if containerized, we are generating .env with contents from the host
  app = App(context_dir_path, **kwargs) if containerized else App(kwargs['app_dir_path'], **kwargs)
  __validate_app(app)

  # Generate SSL certs for HTTPS services
  if kwargs['mkcert']:
    services = __get_services(
      app, service=kwargs['service'], without_core=True, workflow=[kwargs['workflow_name']]
    )
    __services_mkcert(app, services)

  # Determine which workflow command to use based on app configuration
  services = __get_services(
    app, service=kwargs['service'], workflow=[kwargs['workflow_name']]
  )
  script = __build_script(app, **kwargs)

  workflow_namespace = WorkflowNamespace(app, kwargs['namespace'])
  app_config = AppConfig(app.scaffold_namespace_path)

  if app_config.copy_on_workflow_up:
    app.denormalize_up(workflow_namespace, migrate=True)

  if app_config.runtime_local:
    # Use LocalWorkflowRunCommand for local execution
    workflow_command = LocalWorkflowRunCommand(
      app, 
      services=services, 
      script=script,
      workflow_namespace=workflow_namespace,
      **kwargs
    )
  else:
    # Use DockerWorkflowRunCommand for Docker execution
    workflow_command = DockerWorkflowRunCommand(
      app, 
      services=services, 
      script=script,
      workflow_namespace=workflow_namespace,
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
        __hostname_install_with_prompt(
          app_dir_path=kwargs['app_dir_path'],
          hostname_install_confirm=kwargs.get('hostname_install_confirm'),
          service=kwargs['service'],
          validate=True,
          workflow=[kwargs['workflow_name']],
        )

    options = {}

    if os.getcwd() != app.dir_path:
      options['app_dir_path'] = app.dir_path

    if kwargs['namespace'] != kwargs['workflow_name']:
      options['namespace'] = kwargs['namespace']

    options_str = ' '.join([f"--{key} {value}" for key, value in options.items()])
    if options_str:
      options_str = f" {options_str}"

    Logger.instance(LOG_ID).info(f"To view logs, run `stoobly-agent scaffold workflow logs{options_str} {kwargs['workflow_name']}`")
  
  # Execute the workflow
  command_args = { 'print_service_header': lambda service_name: __print_header(f"SERVICE {service_name}") }
  workflow_command.up(
    **command_args,
    **kwargs
  )

@workflow.command(
  help="Generate SSL certs for workflow service(s)"
)
@click.option('--app-dir-path', default=context_dir_path, help='Path to application directory.')
@click.option('--ca-certs-dir-path', default=None, help='Path to ca certs directory used to sign SSL certs. Defaults to the ca_certs dir of the context.')
@click.option('--certs-dir-path', help='Path to certs directory. Defaults to the certs dir of the context.')
@click.option('--containerized', is_flag=True, help='Set if run from within a container.')
@click.option('--context-dir-path', default=data_dir.context_dir_path, help='Path to Stoobly data directory.')
@click.option('--service', multiple=True, help='Select specific services. Defaults to all.')
@click.argument('workflow_name')
def mkcert(**kwargs):
  containerized = kwargs['containerized']
  app = App(context_dir_path, **kwargs) if containerized else App(kwargs['app_dir_path'], **kwargs)

  __validate_app(app)

  services = __get_services(
    app, service=kwargs['service'], without_core=True, workflow=[kwargs['workflow_name']]
  )
  __services_mkcert(app, services)

@workflow.command(
  help="Sync normalize rewrite rules from service upstream hostname, port, and scheme"
)
@click.option('--app-dir-path', default=context_dir_path, help='Path to application directory.')
@click.option('--containerized', is_flag=True, help='Set if run from within a container.')
@click.option('--context-dir-path', default=data_dir.context_dir_path, help='Path to Stoobly data directory.')
@click.option('--service', multiple=True, help='Select specific services. Defaults to all.')
@click.argument('workflow_name')
def rewrite(**kwargs):
  containerized = kwargs['containerized']
  app = App(context_dir_path, **kwargs) if containerized else App(kwargs['app_dir_path'], **kwargs)

  __validate_app(app)

  services = __get_services(
    app, service=kwargs['service'], without_core=True, workflow=[kwargs['workflow_name']]
  )
  __services_rewrite(app, services, kwargs['workflow_name'])

@workflow.command(
  'filter',
  help="Configure include filter rules for workflow service(s)"
)
@click.option('--app-dir-path', default=context_dir_path, help='Path to application directory.')
@click.option('--containerized', is_flag=True, help='Set if run from within a container.')
@click.option('--context-dir-path', default=data_dir.context_dir_path, help='Path to Stoobly data directory.')
@click.option('--service', multiple=True, help='Select specific services. Defaults to all.')
@click.argument('workflow_name')
def _filter(**kwargs):
  containerized = kwargs['containerized']
  app = App(context_dir_path, **kwargs) if containerized else App(kwargs['app_dir_path'], **kwargs)

  __validate_app(app)

  services = __get_services(
    app, service=kwargs['service'], without_core=True, workflow=[kwargs['workflow_name']]
  )
  __services_filter(app, services, kwargs['workflow_name'])

@workflow.command(
  help="Validate a scaffold workflow"
)
@click.option('--app-dir-path', default=context_dir_path, help='Path to validate the app scaffold.')
@click.option('--context-dir-path', default=data_dir.context_dir_path, help='Path to Stoobly data directory.')
@click.option('--namespace', callback=validate_namespace, help='Workflow namespace.')
@click.argument('workflow_name')
def validate(**kwargs):
  __with_namespace_defaults(kwargs)

  app = App(kwargs['app_dir_path'], **kwargs)
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
      if service not in CORE_SERVICES_DOCKER:
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
@click.option('--app-dir-path', default=context_dir_path, help='Path to application directory.')
@click.option('--hostname-install-confirm', default=None, type=click.Choice(['y', 'Y', 'n', 'N']), help='Confirm answer to hostname installation prompt.')
@click.option('--service', multiple=True, help='Select specific services. Defaults to all.')
@click.option('--validate', is_flag=True, help='Validate installation of hostnames.')
@click.option('--workflow', multiple=True, help='Specify services by workflow(s). Defaults to all.')
def install(**kwargs):
  __hostname_install_with_prompt(
    app_dir_path=kwargs['app_dir_path'],
    hostname_install_confirm=kwargs.get('hostname_install_confirm'),
    service=kwargs['service'],
    validate=kwargs.get('validate'),
    workflow=kwargs['workflow'],
  )

@hostname.command(
  help="Delete from the system hosts file all scaffold service hostnames"
)
@click.option('--app-dir-path', default=context_dir_path, help='Path to application directory.')
@click.option('--hostname-uninstall-confirm', default=None, type=click.Choice(['y', 'Y', 'n', 'N']), help='Confirm answer to hostname uninstall prompt.')
@click.option('--service', multiple=True, help='Select specific services. Defaults to all.')
@click.option('--validate', is_flag=True, help='Validate uninstallation of hostnames.')
@click.option('--workflow', multiple=True, help='Specify services by workflow(s). Defaults to all.')
def uninstall(**kwargs):
  __hostname_uninstall_with_prompt(
    app_dir_path=kwargs['app_dir_path'],
    hostname_uninstall_confirm=kwargs.get('hostname_uninstall_confirm'),
    service=kwargs['service'],
    validate=kwargs.get('validate'),
    workflow=kwargs['workflow'],
  )

scaffold.add_command(app)
scaffold.add_command(service)
scaffold.add_command(workflow)
scaffold.add_command(hostname)
scaffold.add_command(request)

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
    selected_services += CORE_SERVICES_DOCKER
    missing_services = [service for service in selected_services if service not in app.services]

    if missing_services:
      # Warn if an invalid service is provided
      Logger.instance(LOG_ID).warn(f"Service(s) {','.join(missing_services)} are not found")

    # Remove services that don't exist
      selected_services = list(set(selected_services) - set(missing_services))

  # If without_score is set, filter out CORE_SERVICES
  if kwargs.get('without_core'):
    selected_services = list(set(selected_services) - set(CORE_SERVICES_DOCKER))

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
  app = App(kwargs['app_dir_path'])
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

def __hostname_install_with_prompt(
  workflow: tuple,
  app_dir_path: str,
  service: tuple,
  hostname_install_confirm: str = None,
  validate: bool = False,
  hosts_file_path: str = '/etc/hosts',
):
  """Prompt user to install hostnames and install them if confirmed."""

  hostnames = __get_hostnames(
    app_dir_path=app_dir_path, service=service, workflow=workflow
  )

  if validate:
    # Check app_config.proxy_mode is reverse
    app = App(app_dir_path)
    app_config = AppConfig(app.scaffold_namespace_path)

    if app_config.proxy_mode != PROXY_MODE_REVERSE:
      return

    hosts_file_manager = HostsFileManager(hosts_file_path=hosts_file_path)
    if hosts_file_manager.hostname_installed(hostnames):
      return

  hostname_install_confirm = hostname_install_confirm or os.environ.get('STOOBLY_HOSTNAME_INSTALL_CONFIRM')

  # Prompt confirm to install hostnames
  if hostname_install_confirm:
    confirm = hostname_install_confirm
  else:
    confirm = input(f"Do you want to install hostname(s) in {hosts_file_path}? (y/N) ")

  if confirm == "y" or confirm == "Y":
    __hostname_install(
      app_dir_path=app_dir_path,
      hosts_file_path=hosts_file_path,
      hostnames=hostnames,
      service=service,
      workflow=workflow,
    )

def __hostname_uninstall_with_prompt(
  workflow: tuple,
  app_dir_path: str,
  service: tuple,
  hostname_uninstall_confirm: str = None,
  validate: bool = False,
  hosts_file_path: str = '/etc/hosts',
):
  """Prompt user to uninstall hostnames and uninstall them if confirmed."""

  hostnames = __get_hostnames(app_dir_path=app_dir_path, service=service, workflow=workflow)

  if validate:
    # Check app_config.proxy_mode is reverse
    app = App(app_dir_path)
    app_config = AppConfig(app.scaffold_namespace_path)

    if app_config.proxy_mode != PROXY_MODE_REVERSE:
      return

    hosts_file_manager = HostsFileManager(hosts_file_path=hosts_file_path)
    if not hosts_file_manager.hostname_installed(hostnames):
      return

  hostname_uninstall_confirm = hostname_uninstall_confirm or os.environ.get('STOOBLY_HOSTNAME_UNINSTALL_CONFIRM')

  # Prompt confirm to uninstall hostnames
  if hostname_uninstall_confirm:
    confirm = hostname_uninstall_confirm
  else:
    confirm = input(f"Do you want to uninstall hostname(s) in {hosts_file_path}? (y/N) ")

  if confirm == "y" or confirm == "Y":
    __hostname_uninstall(
      app_dir_path=app_dir_path,
      hosts_file_path=hosts_file_path,
      hostnames=hostnames,
      service=service,
      workflow=workflow,
    )

def __prepare_temp_hosts(hosts_file_path: str) -> str:
  """Create a temp hosts file seeded from the destination, readable even if destination requires sudo."""
  import shutil
  import subprocess
  import tempfile

  tmp_dir = tempfile.gettempdir()
  temp_hosts_path = os.path.join(tmp_dir, f"stoobly-hosts-{os.getpid()}")

  # Seed temp hosts file with the current destination contents.
  if os.path.exists(hosts_file_path):
    try:
      shutil.copy2(hosts_file_path, temp_hosts_path)
    except PermissionError:
      # If we can't read the destination, fall back to `sudo cp` for just the read/copy.
      subprocess.run(["sudo", "cp", hosts_file_path, temp_hosts_path], check=True)
  else:
    open(temp_hosts_path, 'a').close()

  return temp_hosts_path

def __sudo_backup_and_replace(hosts_file_path: str, temp_hosts_path: str):
  """Backup destination (if /etc/hosts) and copy temp file into place via sudo."""
  import subprocess
  import tempfile
  import os

  if os.path.exists(hosts_file_path):
    # Backup hosts file
    backup_path = os.path.join(tempfile.gettempdir(), f"hosts.bak")
    is_readable = os.access(hosts_file_path, os.R_OK)
    if not is_readable:
      subprocess.run(["sudo", "cp", hosts_file_path, backup_path], check=True)
    else:
      subprocess.run(["cp", hosts_file_path, backup_path], check=True)

  # Replace destination from temp
  # Use sudo only when necessary: if destination is /etc/hosts or not writable
  dest_exists = os.path.exists(hosts_file_path)
  dest_dir = os.path.dirname(hosts_file_path) or "."
  is_writable = os.access(hosts_file_path, os.W_OK) if dest_exists else os.access(dest_dir, os.W_OK)

  if not is_writable:
    subprocess.run(["sudo", "cp", temp_hosts_path, hosts_file_path], check=True)
  else:
    subprocess.run(["cp", temp_hosts_path, hosts_file_path], check=True)

def __hostname_install(**kwargs):
  hostnames = kwargs.get('hostnames')
  if not hostnames:
    return

  hosts_file_path = os.path.abspath(kwargs.get('hosts_file_path') or '/etc/hosts')
  temp_hosts_path = __prepare_temp_hosts(hosts_file_path)
  try:
    # Apply changes to the temp file (not the destination).
    hosts_file_manager = HostsFileManager(hosts_file_path=temp_hosts_path)
    hosts_file_manager.install_hostnames(hostnames)
    # Backup (if needed) and replace destination from temp
    __sudo_backup_and_replace(hosts_file_path, temp_hosts_path)
  finally:
    try:
      if os.path.exists(temp_hosts_path):
        os.remove(temp_hosts_path)
    except OSError:
      pass

def __hostname_uninstall(**kwargs):
  hostnames = kwargs.get('hostnames')
  if not hostnames:
    return

  hosts_file_path = os.path.abspath(kwargs.get('hosts_file_path') or '/etc/hosts')
  temp_hosts_path = __prepare_temp_hosts(hosts_file_path)
  try:
    # Apply changes to the temp file (not the destination).
    hosts_file_manager = HostsFileManager(hosts_file_path=temp_hosts_path)
    hosts_file_manager.uninstall_hostnames(hostnames)
    # Backup (if needed) and replace destination from temp
    __sudo_backup_and_replace(hosts_file_path, temp_hosts_path)
  finally:
    try:
      if os.path.exists(temp_hosts_path):
        os.remove(temp_hosts_path)
    except OSError:
      pass

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

def __services_rewrite(app: App, services, workflow_name: str):
  for service_name in services:
    service = Service(service_name, app)
    __validate_service_dir(service.dir_path)

    workflow_dir_path = service.workflow_dir_path(workflow_name)
    workflow_config = WorkflowConfig(workflow_dir_path)
    workflow_template = workflow_config.template or workflow_name

    # Skip rewrite for docker runtime local services in test workflows
    # In such a case, UPSTREAM_HOSTNAME will be set to host.docker.internal
    service_config = ServiceConfig(service.dir_path)
    if (
      workflow_template == WORKFLOW_TEST_TYPE and
      service_config.local and
      service_config.app_config.runtime == RUNTIME_DOCKER
    ):
      continue

    apply_upstream_url_rewrite(service_config)

def __services_filter(app: App, services, workflow_name: str):
  settings = Settings.instance()
  project_key = ProjectKey(settings.proxy.intercept.project_key)
  project_id = project_key.id
  filter_rules = settings.proxy.filter.filter_rules(project_id)

  for service_name in services:
    service = Service(service_name, app)
    __validate_service_dir(service.dir_path)

    workflow_dir_path = service.workflow_dir_path(workflow_name)
    workflow_config = WorkflowConfig(workflow_dir_path)
    workflow_template = workflow_config.template or workflow_name
    # For custom workflows, template is set using the --template option
    filter_mode = workflow_template_to_filter_mode(workflow_template)

    service_config = ServiceConfig(service.dir_path)
    if not service_config.url:
      continue

    new_rule = build_include_filter_rule_for_service_url(
      service_url=service_config.url,
      filter_mode=filter_mode,
      methods=HTTP_METHODS,
    )
    upsert_filter_rule(filter_rules=filter_rules, new_rule=new_rule)

  settings.proxy.filter.set_filter_rules(project_id, filter_rules)
  settings.commit()

def __validate_app(app: App):
  try:
    app.valid
  except ValueError as e:
    print(f"Error: {e}", file=sys.stderr)
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

def __is_docker_workflow_running(namespace: str) -> bool:
  """Check if any containers are running for this workflow namespace."""
  docker_client = None
  try:
    docker_client = docker.from_env()
    # Filter containers by compose project name (namespace)
    containers = docker_client.containers.list(
      filters={'label': f'com.docker.compose.project={namespace}'}
    )
    # Check if any are running
    return any(c.status == 'running' for c in containers)
  except docker_errors.DockerException:
    return False  # Docker not available or error
  finally:
    if docker_client:
      docker_client.close()

def __find_running_workflows(app: App, app_config: AppConfig):
  """Scan for running workflows and return their info."""
  found_workflows = []
  tmp_dir_path = app.data_dir.tmp_dir_path

  if not os.path.exists(tmp_dir_path):
    return found_workflows

  # Determine file extension based on runtime
  if app_config.runtime_local:
    file_extension = '.pid'
  else:
    file_extension = '.timestamp'

  # Scan tmp directory for workflow status files
  try:
    folders = os.listdir(tmp_dir_path)
  except PermissionError:
    return found_workflows

  for folder in folders:
    folder_path = os.path.join(tmp_dir_path, folder)

    if not os.path.isdir(folder_path):
      continue

    try:
      files = os.listdir(folder_path)
    except PermissionError:
      continue

    for file in files:
      if not file.endswith(file_extension):
        continue

      file_path = os.path.join(folder_path, file)
      workflow_name = file.removesuffix(file_extension)

      # For local runtime, verify process is running
      if app_config.runtime_local:
        try:
          with open(file_path, 'r') as f:
            pid = int(f.read().strip())
          # Check if process is running (signal 0 doesn't kill)
          os.kill(pid, 0)
          found_workflows.append({
            'workflow_name': workflow_name,
            'namespace': folder,
            'file_path': file_path,
            'pid': pid
          })
        except (OSError, ProcessLookupError, ValueError):
          continue
      else:
        # For Docker runtime, verify containers are running
        if not __is_docker_workflow_running(folder):
          continue
        found_workflows.append({
          'workflow_name': workflow_name,
          'namespace': folder,
          'file_path': file_path
        })

  return found_workflows

def __print_workflow_status(workflow_info: dict, app: App, app_config: AppConfig, verbose: bool):
  """Print status for a single workflow."""
  workflow_name = workflow_info['workflow_name']
  namespace = workflow_info['namespace']

  # Header bar
  header = f"  Workflow: {workflow_name}"
  bar = "═" * 45
  click.echo(bar)
  click.echo(header)
  click.echo(bar)

  # Status with green color for "running"
  status_value = click.style("running", fg="green")

  # Aligned key-value pairs
  click.echo(f"  {'Namespace':<12}{namespace}")
  click.echo(f"  {'Status':<12}{status_value}")

  if app_config.runtime_local:
    click.echo(f"  {'Runtime':<12}local")
    click.echo(f"  {'PID':<12}{workflow_info['pid']}")
  else:
    # Read timestamp for Docker runtime
    try:
      with open(workflow_info['file_path'], 'r') as f:
        timestamp = float(f.read().strip())
      started = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    except (IOError, ValueError):
      started = "unknown"
    click.echo(f"  {'Runtime':<12}docker")
    click.echo(f"  {'Started':<12}{started}")

  if verbose:
    __show_workflow_services(workflow_name, app)

def __show_workflow_services(workflow_name: str, app: App):
  """Show services for a workflow."""
  services = __get_services(app, service=(), without_core=True, workflow=(workflow_name,))

  if services:
    click.echo()
    click.echo("Services")
    click.echo("─" * 45)
    rows = []
    for service_name in services:
      service = Service(service_name, app)
      if not os.path.exists(service.dir_path):
        continue
      config = ServiceConfig(service.dir_path)
      rows.append({
        'name': service_name,
        **config.to_dict()
      })

    print_services(rows)
