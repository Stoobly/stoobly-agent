import os
import pdb
import socket
from typing import Optional

from docker import errors as docker_errors

from stoobly_agent.app.cli.scaffold.constants import WORKFLOW_TEST_TYPE
from stoobly_agent.app.cli.scaffold.managed_services_docker_compose import (
  ManagedServicesDockerCompose,
)
from stoobly_agent.app.cli.scaffold.templates.constants import (
  CORE_ENTRYPOINT_SERVICE_NAME,
  CORE_GATEWAY_SERVICE_NAME,
  CORE_MOCK_UI_SERVICE_NAME,
  CORE_SERVICES_DOCKER,
  CORE_SERVICES_LOCAL,
)
from stoobly_agent.app.cli.scaffold.validate_command import ValidateCommand
from stoobly_agent.app.cli.scaffold.validate_exceptions import ScaffoldValidateException
from stoobly_agent.app.cli.scaffold.workflow_command import WorkflowCommand
from stoobly_agent.app.cli.scaffold.workflow_namespace import WorkflowNamespace
from stoobly_agent.lib.logger import bcolors

from .app import App


class WorkflowValidateCommand(WorkflowCommand, ValidateCommand):
  def __init__(self, app: App, **kwargs):
    WorkflowCommand.__init__(self, app, **kwargs)

    self.__namespace = kwargs.get('namespace') or self.workflow_name

    # Only require Docker for non-local runtime
    require_docker = not self.app_config.runtime_local
    ValidateCommand.__init__(self, require_docker=require_docker)

    # Only initialize Docker-specific components when needed
    if not self.app_config.runtime_local:
      self.managed_services_docker_compose = ManagedServicesDockerCompose(target_workflow_name=self.__namespace)

  # Gateway core service only runs in Docker scaffolds
  def validate_gateway_service(self):
    if self.app_config.runtime_local:
      # print(f"Skipping core service validation: {CORE_GATEWAY_SERVICE_NAME} (local runtime)")
      return

    print(f"Validating core service: {CORE_GATEWAY_SERVICE_NAME}")
    gateway_container_name = self.managed_services_docker_compose.gateway_container_name

    container_missing_message = f"{bcolors.FAIL}Container '{gateway_container_name}' not found for service '{CORE_GATEWAY_SERVICE_NAME}'{bcolors.ENDC}"
    suggestion_message = f"{bcolors.BOLD}Workflow might not be running yet. Try running 'scaffold workflow up <WORKFLOW_NAME>'{bcolors.ENDC}"
    error_message = f"{container_missing_message}\n\n{suggestion_message}"

    try:
      gateway_container = self.docker_client.containers.get(gateway_container_name)
      if not gateway_container or (gateway_container.status != 'running'):
        raise ScaffoldValidateException(error_message)
    except docker_errors.NotFound:
      raise ScaffoldValidateException(error_message)

  def validate_mock_ui_service(self):
    if self.app_config.runtime_local:
      return
    
    mock_ui_container_name = self.managed_services_docker_compose.mock_ui_container_name

    # The stoobly-ui service does not run in test workflows
    if self.workflow_name == WORKFLOW_TEST_TYPE:
      try:
        mock_ui_container = self.docker_client.containers.get(mock_ui_container_name)

        if mock_ui_container:
          ui_found_message = f"{bcolors.FAIL}Stoobly UI container is running when it shouldn't: {mock_ui_container_name}{bcolors.ENDC}"
          suggestion_message = f"{bcolors.BOLD}Run 'docker ps | grep stoobly_ui' to check if the Stoobly UI is running during the test workflow. Did you stop the record or mock workflow yet?{bcolors.ENDC}"
          error_message = f"{ui_found_message}\n\n{suggestion_message}"
          raise ScaffoldValidateException(error_message)
      except docker_errors.NotFound:
        print(f"Skipping validating core service: {CORE_MOCK_UI_SERVICE_NAME}")
        return

    print(f"Validating core service: {CORE_MOCK_UI_SERVICE_NAME}")
    container_missing_message = f"{bcolors.FAIL}Container '{mock_ui_container_name}' not found for service '{CORE_MOCK_UI_SERVICE_NAME}'{bcolors.ENDC}"
    suggestion_message = f"{bcolors.BOLD}Stoobly UI is not running. Check if the container is up with 'docker ps -a | grep {mock_ui_container_name}'{bcolors.ENDC}"
    mock_ui_missing_error_message = f"{container_missing_message}\n\n{suggestion_message}"

    try:
      mock_ui_container = self.docker_client.containers.get(mock_ui_container_name)
      if not mock_ui_container or (mock_ui_container.status != 'running'):
        raise ScaffoldValidateException(mock_ui_missing_error_message)
    except docker_errors.NotFound:
      raise ScaffoldValidateException(mock_ui_missing_error_message)

  def validate_entrypoint_service(self):
    print(f"Validating core service: {CORE_ENTRYPOINT_SERVICE_NAME}")

    core_entrypoint_init_container_name = None
    try:
      core_entrypoint_init_container_name = self.managed_services_docker_compose.entrypoint_init_container_name
      entrypoint_init_container = self.docker_client.containers.get(core_entrypoint_init_container_name)
    except docker_errors.NotFound:
      error_message = self._ValidateCommand__generate_container_not_found_error(core_entrypoint_init_container_name)
      raise ScaffoldValidateException(error_message)
    
    core_entrypoint_configure_container_name = None
    try:
      core_entrypoint_configure_container_name = self.managed_services_docker_compose.entrypoint_configure_container_name
      entrypoint_configure_container = self.docker_client.containers.get(core_entrypoint_configure_container_name)
    except docker_errors.NotFound:
      error_message = self._ValidateCommand__generate_container_not_found_error(core_entrypoint_configure_container_name)
      raise ScaffoldValidateException(error_message)

    # NOTE: we should check the correct workflow mode is enabled one day
    # That's not currently queryable

    print(f"{bcolors.OKGREEN}✔ Done validating core services for workflow: {self.workflow_name}, success!\n{bcolors.ENDC}")

  # Local validation helper methods
  def _get_workflow_namespace(self) -> WorkflowNamespace:
    """Get the workflow namespace for this workflow."""
    return WorkflowNamespace(self.app, self.workflow_name)

  def _read_pid(self, file_path: str) -> Optional[int]:
    """Read the process PID from the PID file."""
    if not os.path.exists(file_path):
      return None

    try:
      with open(file_path, 'r') as f:
        return int(f.read().strip())
    except (ValueError, IOError):
      return None

  def _is_process_running(self, pid: int) -> bool:
    """Check if a process is still running."""
    try:
      os.kill(pid, 0)  # Signal 0 doesn't kill, just checks existence
      return True
    except (OSError, ProcessLookupError):
      return False

  def _is_port_listening(self, port: int, host: str = 'localhost') -> bool:
    """Check if a port is being listened on."""
    try:
      with socket.create_connection((host, port), timeout=1):
        return True
    except (socket.timeout, socket.error):
      return False

  def validate_core_services(self):
    if self.app_config.runtime_local:
      self.validate_local_core_services()
    else:
      self.validate_gateway_service()
      self.validate_mock_ui_service()
      self.validate_init_containers(self.managed_services_docker_compose.init_container_name, self.managed_services_docker_compose.configure_container_name)
      self.validate_entrypoint_service()

  # Local workflow validation methods
  def validate_local_core_services(self):
    """Validate core services for local runtime mode."""
    print(f"Validating core service: proxy")

    # Validate process is running
    self.validate_local_process()

    # Validate proxy port is listening
    self.validate_proxy_port()

    print(f"{bcolors.OKGREEN}✔ Done validating local core services for workflow: {self.workflow_name}, success!\n{bcolors.ENDC}")

  def validate_local_process(self):
    """Validate the local workflow process is running."""
    print(f"Validating local process for workflow: {self.workflow_name}")

    workflow_namespace = self._get_workflow_namespace()
    pid_file_path = os.path.join(workflow_namespace.path, f"{self.workflow_name}.pid")

    # Check PID file exists
    if not os.path.exists(pid_file_path):
      error_message = f"{bcolors.FAIL}PID file not found: {pid_file_path}{bcolors.ENDC}"
      suggestion_message = f"{bcolors.BOLD}Workflow might not be running. Try running 'scaffold workflow up {self.workflow_name}'{bcolors.ENDC}"
      raise ScaffoldValidateException(f"{error_message}\n\n{suggestion_message}")

    # Read and validate PID
    pid = self._read_pid(pid_file_path)
    if pid is None:
      error_message = f"{bcolors.FAIL}Could not read PID from file: {pid_file_path}{bcolors.ENDC}"
      suggestion_message = f"{bcolors.BOLD}PID file may be corrupted. Try running 'scaffold workflow down {self.workflow_name}' then 'scaffold workflow up {self.workflow_name}'{bcolors.ENDC}"
      raise ScaffoldValidateException(f"{error_message}\n\n{suggestion_message}")

    # Check process is running
    if not self._is_process_running(pid):
      log_file_path = os.path.join(workflow_namespace.path, f"{self.workflow_name}.log")
      error_message = f"{bcolors.FAIL}Process {pid} for workflow '{self.workflow_name}' is not running{bcolors.ENDC}"
      suggestion_message = f"{bcolors.BOLD}Process may have crashed. Check logs at {log_file_path} and restart with 'scaffold workflow up {self.workflow_name}'{bcolors.ENDC}"
      raise ScaffoldValidateException(f"{error_message}\n\n{suggestion_message}")

    print(f"Process {pid} is running for workflow: {self.workflow_name}")

  def validate_proxy_port(self):
    """Validate the proxy port is being listened on."""
    proxy_port = self.app_config.proxy_port
    print(f"Validating proxy port: {proxy_port}")

    if not self._is_port_listening(proxy_port):
      error_message = f"{bcolors.FAIL}Proxy port {proxy_port} is not listening{bcolors.ENDC}"
      suggestion_message = f"{bcolors.BOLD}The stoobly-agent proxy may have failed to start. Check logs for errors.{bcolors.ENDC}"
      raise ScaffoldValidateException(f"{error_message}\n\n{suggestion_message}")

    print(f"Proxy port {proxy_port} is listening")

  def validate(self) -> bool:
    print(f"Validating workflow: {self.workflow_name}\n")
    
    if self.app_config.runtime_local:
      print(f"Validating core services: {CORE_SERVICES_LOCAL}")
    else:
      print(f"Validating core services: {CORE_SERVICES_DOCKER}")

    self.validate_core_services()

    return True


