import os
import pdb

from stoobly_agent.app.cli.scaffold.templates.constants import CORE_ENTRYPOINT_SERVICE_NAME
from stoobly_agent.lib.logger import Logger

from typing import List, TypedDict, Callable, Optional

from ...workflow_run_command import WorkflowRunCommand
from ....types.workflow_run_command import BuildOptions, DownOptions, UpOptions
from ..constants import APP_EGRESS_NETWORK_TEMPLATE, APP_INGRESS_NETWORK_TEMPLATE, DOCKERFILE_CONTEXT
from ..service.configure_gateway import configure_gateway
from ...workflow import Workflow

LOG_ID = 'DockerWorkflowRunCommand'

class WorkflowDownOptions(TypedDict, total=False):
  workflow_namespace: str
  print_service_header: Optional[Callable[[str], None]]
  extra_entrypoint_compose_path: Optional[str]
  namespace: Optional[str]
  rmi: bool
  user_id: Optional[int]
  # CLI-specific options that get passed through
  containerized: bool
  dry_run: bool
  log_level: str
  script_path: Optional[str]
  service: List[str]

class WorkflowUpOptions(TypedDict, total=False):
  workflow_namespace: str
  print_service_header: Optional[Callable[[str], None]]
  extra_entrypoint_compose_path: Optional[str]
  namespace: Optional[str]
  no_build: bool
  pull: bool
  user_id: Optional[int]
  detached: bool
  # CLI-specific options that get passed through
  containerized: bool
  dry_run: bool
  log_level: str
  script_path: Optional[str]
  service: List[str]
  no_publish: bool
  without_base: bool
  verbose: bool
  mkcert: bool

class WorkflowLogsOptions(TypedDict, total=False):
  print_service_header: Optional[Callable[[str], None]]
  container: List[str]
  follow: bool
  namespace: Optional[str]
  # CLI-specific options that get passed through
  containerized: bool
  dry_run: bool
  log_level: str
  script_path: Optional[str]
  service: List[str]

class DockerWorkflowRunCommand(WorkflowRunCommand):
  """Docker-specific workflow run command that handles Docker Compose operations."""

  def __init__(self, app, services=None, script=None, **kwargs):
    if not kwargs.get('service_name'):
      kwargs['service_name'] = CORE_ENTRYPOINT_SERVICE_NAME

    super().__init__(app, **kwargs)

    self.services = services or []
    self.script = script

  def setup_docker_environment(self, services, workflow_namespace, no_publish=False, without_base=False, containerized=False, user_id=None, verbose=False):
    """Setup Docker environment including gateway, images, and networks."""
    init_commands = []
    
    # Configure gateway ports dynamically based on workflow run
    workflow = Workflow(self.workflow_name, self.app)
    configure_gateway(workflow_namespace, workflow.service_paths_from_services(services), no_publish)
    
    # Create base image if needed
    if not without_base:
      create_image_command = self.create_image(user_id=user_id, verbose=verbose)
      init_commands.append(create_image_command)
    
    # Create networks
    init_commands.append(self.create_egress_network())
    init_commands.append(self.create_ingress_network())
    
    # Write nameservers if not running in container
    if not containerized:
      self.write_nameservers()
    
    return ' && '.join(init_commands) if init_commands else ''

  def up(self, workflow_namespace, **options: WorkflowUpOptions):
    """Execute the complete Docker workflow up process."""
    print_service_header = options.get('print_service_header')
    
    # Create individual service commands
    commands: List[DockerWorkflowRunCommand] = []
    for service in self.services:
      config = { **options }
      config['service_name'] = service
      command = DockerWorkflowRunCommand(self.app, **config)
      commands.append(command)
    
    # Setup Docker environment
    if commands:
      init_command = self.setup_docker_environment(
        services=self.services,
        workflow_namespace=workflow_namespace,
        no_publish=options.get('no_publish', False),
        without_base=options.get('without_base', False),
        containerized=options.get('containerized', False),
        user_id=options.get('user_id'),
        verbose=options.get('verbose', False)
      )
      
      if init_command and self.script:
        print(init_command, file=self.script)
    
    # Sort commands by priority and execute
    commands = sorted(commands, key=lambda command: command.service_config.priority)
    for index, command in enumerate(commands):
      if print_service_header:
        print_service_header(command.service_name)
      
      attached = False
      extra_compose_path = None
      
      # By default, the entrypoint service should be last
      # However, this can change if the user has configured a service's priority to be higher
      if index == len(commands) - 1:
        attached = not options.get('detached', False)
        extra_compose_path = options.get('extra_entrypoint_compose_path')
      
      exec_command = command.service_up(
        attached=attached,
        extra_compose_path=extra_compose_path,
        namespace=options.get('namespace'),
        no_build=options.get('no_build', False),
        pull=options.get('pull', False),
        user_id=options.get('user_id')
      )
      
      if exec_command and self.script:
        print(exec_command, file=self.script)

  def down(self, **options: WorkflowDownOptions):
    """Execute the complete Docker workflow down process."""
    print_service_header = options.get('print_service_header')
    
    # Create individual service commands
    commands: List[DockerWorkflowRunCommand] = []
    for service in self.services:
      config = { **options }
      config['service_name'] = service
      command = DockerWorkflowRunCommand(self.app, **config)
      commands.append(command)
    
    # Sort commands by priority and execute
    commands = sorted(commands, key=lambda command: command.service_config.priority)
    for index, command in enumerate(commands):
      if print_service_header:
        print_service_header(command.service_name)
      
      extra_compose_path = None
      
      # By default, the entrypoint service should be last
      # However, this can change if the user has configured a service's priority to be higher
      if index == len(commands) - 1:
        extra_compose_path = options.get('extra_entrypoint_compose_path')
      
      exec_command = command.service_down(
        extra_compose_path=extra_compose_path,
        namespace=options.get('namespace'),
        rmi=options.get('rmi', False),
        user_id=options.get('user_id')
      )
      
      if exec_command and self.script:
        print(exec_command, file=self.script)
    
    # After services are stopped, their network needs to be removed
    if commands:
      command = commands[0]
      
      if options.get('rmi'):
        remove_image_command = command.remove_image(options.get('user_id'))
        if remove_image_command and self.script:
          print(remove_image_command, file=self.script)
      
      remove_egress_network_command = command.remove_egress_network()
      if remove_egress_network_command and self.script:
        print(remove_egress_network_command, file=self.script)
      
      remove_ingress_network_command = command.remove_ingress_network()
      if remove_ingress_network_command and self.script:
        print(remove_ingress_network_command, file=self.script)

  def logs(self, **options: WorkflowLogsOptions):
    """Execute the complete Docker workflow logs process."""
    from ...templates.constants import CORE_SERVICES
    
    print_service_header = options.get('print_service_header')
    
    # Filter services based on options
    filtered_services = []
    for service in self.services:
      if len(options.get('service', [])) == 0:
        # If no filter is specified, ignore CORE_SERVICES  
        if service in CORE_SERVICES:
          continue
      else:
        # If a filter is specified, ignore all other services
        if service not in options.get('service', []):
          continue
      filtered_services.append(service)
    
    # Create individual service commands and get their log commands
    commands = []
    for service in filtered_services:
      config = dict(options)
      config['service_name'] = service
      command = DockerWorkflowRunCommand(self.app, **config)
      commands.append((service, command))
    
    # Sort commands by priority and execute
    commands = sorted(commands, key=lambda x: x[1].service_config.priority)
    for index, (service, command) in enumerate(commands):
      if print_service_header:
        print_service_header(service)
      
      follow = options.get('follow', False) and index == len(commands) - 1
      shell_commands = self._build_log_commands(
        command, 
        containers=options.get('container', []), 
        follow=follow, 
        namespace=options.get('namespace')
      )
      
      for shell_command in shell_commands:
        if self.script:
          print(shell_command, file=self.script)

  def _build_log_commands(self, command, containers=None, follow=False, namespace=None):
    """Build Docker log commands for a service."""
    from ...constants import WORKFLOW_CONTAINER_TEMPLATE
    
    log_commands = []
    available_containers = command.containers
    allowed_containers = list(
      map(
        lambda container: WORKFLOW_CONTAINER_TEMPLATE.format(
          container=container, service_name=command.service_name
        ), containers or []
      )
    )

    for index, container in enumerate(available_containers):
      if container not in allowed_containers:
        continue

      container_name = self._container_name(container, namespace or command.workflow_name)
      log_commands.append(f"echo \"=== Logging {container_name}\"")
      
      if follow and index == len(available_containers) - 1:
        docker_command = ['docker', 'logs', '--follow', container_name]
      else:
        docker_command = ['docker', 'logs', container_name]
      
      log_commands.append(' '.join(docker_command))

    return log_commands

  def _container_name(self, container, namespace):
    """Generate container name based on namespace and container."""
    return f"{namespace}-{container}-1"

  def create_image(self, **options: BuildOptions):
    """Build Docker image for the workflow."""
    relative_namespace_path = os.path.relpath(self.scaffold_namespace_path, self.current_working_dir)
    dockerfile_path = os.path.join(relative_namespace_path, DOCKERFILE_CONTEXT)
    user_id = options['user_id'] or os.getuid()
    
    command = ['docker', 'build']
    command.append(f"-f {dockerfile_path}")
    command.append(f"-t stoobly.{user_id}")
    command.append(f"--build-arg USER_ID={user_id}")

    if not os.environ.get('STOOBLY_IMAGE_USE_LOCAL'):
      command.append('--pull')

    if not options.get('verbose'):
      command.append('--quiet')

    # To avoid large context transfer times, should be a folder with relatively low number of files
    command.append(relative_namespace_path) 

    return ' '.join(command)

  def remove_image(self, user_id: str = None):
    """Remove Docker image for the workflow."""
    user_id = user_id or os.getuid()
    command = ['docker', 'rmi', f"stoobly.{user_id}", '&>', '/dev/null']
    command.append('|| true')
    return ' '.join(command)

  def create_egress_network(self):
    """Create Docker egress network."""
    return f"docker network create {APP_EGRESS_NETWORK_TEMPLATE.format(network=self.network)} &> /dev/null"

  def create_ingress_network(self):
    """Create Docker ingress network."""
    return f"docker network create {APP_INGRESS_NETWORK_TEMPLATE.format(network=self.network)} &> /dev/null"

  def remove_egress_network(self):
    """Remove Docker egress network."""
    return f"docker network rm {APP_EGRESS_NETWORK_TEMPLATE.format(network=self.network)} &> /dev/null || true"

  def remove_ingress_network(self):
    """Remove Docker ingress network."""
    return f"docker network rm {APP_INGRESS_NETWORK_TEMPLATE.format(network=self.network)} &> /dev/null || true"

  def service_up(self, **options: UpOptions):
    """Start the workflow using Docker Compose."""
    if not os.path.exists(self.compose_path):
      return ''

    command = ['COMPOSE_IGNORE_ORPHANS=true', 'docker', 'compose']
    command_options = []

    # Add docker compose file
    command_options.append(f"-f {os.path.relpath(self.compose_path, self.current_working_dir)}")

    # Add docker compose networks file
    command_options.append(f"-f {os.path.relpath(self.networks_compose_path, os.getcwd())}")

    # Add custom docker compose file
    custom_services = self.custom_services
    if custom_services:
      uses_profile = False
      for service_name in custom_services:
        service = custom_services[service_name]
        profiles = service.get('profiles')
        if isinstance(profiles, list):
          if self.workflow_name in profiles:
            uses_profile = True
            break
      if not uses_profile:
        # TODO: looking into why warning does not print in docker
        Logger.instance(LOG_ID).error(f"Missing {self.workflow_name} profile in custom compose file")

      compose_file_path = os.path.relpath(self.custom_compose_path, self.current_working_dir)
      command_options.append(f"-f {compose_file_path}")

    if options.get('extra_compose_path'):
      compose_file_path = os.path.relpath(options['extra_compose_path'], self.current_working_dir)
      command_options.append(f"-f {compose_file_path}")

    command_options.append(f"--profile {self.workflow_name}") 

    if not options.get('namespace'):
      options['namespace'] = self.workflow_name
    command_options.append(f"-p {options['namespace']}")

    command += command_options
    command.append('up')

    if not options.get('no_build'):
      command.append('--build')

    if options.get('pull'):
      command.append('--pull missing')

    if not options.get('attached'):
      command.append('-d')

    # Fail fast option - makes docker compose return exit code 1 
    # when one of the services exits with a non-zero exit code
    for option in ['--abort-on-container-exit', '--exit-code-from']:
      if options.get(option):
        command.append(option)

    self.write_env(**options)

    return ' '.join(command)

  def service_down(self, **options: DownOptions):
    """Stop the workflow using Docker Compose."""
    if not os.path.exists(self.compose_path):
      return ''
  
    command = ['docker', 'compose']

    # Add docker compose file
    command.append(f"-f {os.path.relpath(self.compose_path, os.getcwd())}")

    # Add docker compose networks file
    command.append(f"-f {os.path.relpath(self.networks_compose_path, os.getcwd())}")

    # Add custom docker compose file
    if self.custom_services:
      command.append(f"-f {os.path.relpath(self.custom_compose_path, self.current_working_dir)}")

    if options.get('extra_compose_path'):
      command.append(f"-f {os.path.relpath(options['extra_compose_path'], self.current_working_dir)}")

    command.append(f"--profile {self.workflow_name}") 

    if not options.get('namespace'):
      options['namespace'] = self.workflow_name
    command.append(f"-p {options['namespace']}")

    command.append('down')
    command.append('--volumes')

    if options.get('rmi'):
      command.append('--rmi local')

    self.write_env(**options)

    return ' '.join(command)
