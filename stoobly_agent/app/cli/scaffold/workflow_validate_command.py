import pdb

from docker import errors as docker_errors

from stoobly_agent.app.cli.scaffold.constants import WORKFLOW_TEST_TYPE
from stoobly_agent.app.cli.scaffold.managed_services_docker_compose import (
  ManagedServicesDockerCompose,
)
from stoobly_agent.app.cli.scaffold.templates.constants import (
  CORE_ENTRYPOINT_SERVICE_NAME,
  CORE_GATEWAY_SERVICE_NAME,
  CORE_MOCK_UI_SERVICE_NAME,
  CORE_SERVICES,
)
from stoobly_agent.app.cli.scaffold.validate_command import ValidateCommand
from stoobly_agent.app.cli.scaffold.validate_exceptions import ScaffoldValidateException
from stoobly_agent.app.cli.scaffold.workflow_command import WorkflowCommand
from stoobly_agent.lib.logger import bcolors

from .app import App


class WorkflowValidateCommand(WorkflowCommand, ValidateCommand):
  def __init__(self, app: App, **kwargs):
    WorkflowCommand.__init__(self, app, **kwargs)
    ValidateCommand.__init__(self)
    self.managed_services_docker_compose = ManagedServicesDockerCompose(target_workflow_name=self.workflow_name)

  def validate_core_components(self):
    print(f"Validating core component: {CORE_GATEWAY_SERVICE_NAME}")
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


    print(f"Validating core component: {CORE_MOCK_UI_SERVICE_NAME}")
    mock_ui_container_name = self.managed_services_docker_compose.mock_ui_container_name

    container_missing_message = f"{bcolors.FAIL}Container '{mock_ui_container_name}' not found for service '{CORE_MOCK_UI_SERVICE_NAME}'{bcolors.ENDC}"
    suggestion_message = f"{bcolors.BOLD}Stoobly UI is not running. Check if the container is up with 'docker ps -a | grep stoobly_ui'. If not found, then report a bug at https://github.com/Stoobly/stoobly-agent/issues{bcolors.ENDC}"

    mock_ui_missing_error_message = f"{container_missing_message}\n\n{suggestion_message}"

    try:
      mock_ui_container = self.docker_client.containers.get(mock_ui_container_name)
      if not mock_ui_container or (mock_ui_container.status != 'running'):
        raise ScaffoldValidateException(mock_ui_missing_error_message)
    except docker_errors.NotFound:
      raise ScaffoldValidateException(mock_ui_missing_error_message)

  def validate_no_core_components(self):
    try:
      core_gateway_container = self.docker_client.containers.get(self.managed_services_docker_compose.gateway_container_name)
      if core_gateway_container:
        gateway_found_message = f"{bcolors.FAIL}Gateway container is running when it shouldn't: {core_gateway_container.name}{bcolors.ENDC}"
        suggestion_message = f"{bcolors.BOLD}Run 'docker ps | grep gateway'. If the gateway is running during your test workflow, then report a bug at https://github.com/Stoobly/stoobly-agent/issues'{bcolors.ENDC}"
        error_message = f"{gateway_found_message}\n\n{suggestion_message}"
        raise ScaffoldValidateException(error_message)
    except docker_errors.NotFound:
      pass
    
    try:
      core_mock_ui_container_name = self.docker_client.containers.get(self.managed_services_docker_compose.mock_ui_container_name)
      if core_mock_ui_container_name:
        ui_found_message = f"{bcolors.FAIL}Stoobly UI container is running when it shouldn't: {core_mock_ui_container_name.name}{bcolors.ENDC}"
        suggestion_message = f"{bcolors.BOLD}Run 'docker ps | grep stoobly_ui'. If the UI is running during your test workflow, then report a bug at https://github.com/Stoobly/stoobly-agent/issues'{bcolors.ENDC}"
        error_message = f"{ui_found_message}\n\n{suggestion_message}"
        raise ScaffoldValidateException(error_message)
    except docker_errors.NotFound:
      pass
    
    print(f"Skipping validating core component: {CORE_GATEWAY_SERVICE_NAME}")
    print(f"Skipping validating core component: {CORE_MOCK_UI_SERVICE_NAME}")

  
  def validate(self) -> bool:
    print(f"Validating workflow: {self.workflow_name}\n")
    print(f"Validating core components: {CORE_SERVICES}")

    if self.workflow_name == WORKFLOW_TEST_TYPE:
      # Don't validate the gateway and mock_ui core components in the "test" workflow 
      self.validate_no_core_components()
    else:
      self.validate_core_components()

    self.validate_init_containers(self.managed_services_docker_compose.init_container_name, self.managed_services_docker_compose.configure_container_name)

    print(f"Validating core component: {CORE_ENTRYPOINT_SERVICE_NAME}")

    core_entrypoint_init_container_name = None
    try:
      core_entrypoint_init_container_name = self.managed_services_docker_compose.entrypoint_init_container_name
      entrypoint_init_container = self.docker_client.containers.get(core_entrypoint_init_container_name)
    except docker_errors.NotFound:
      container_missing_message = f"{bcolors.FAIL}Container not found: {core_entrypoint_init_container_name}{bcolors.ENDC}"
      suggestion_message = f"{bcolors.BOLD}Run 'docker ps -a' and report a bug at https://github.com/Stoobly/stoobly-agent/issues{bcolors.ENDC}"
      error_message = f"{container_missing_message}\n\n{suggestion_message}"
      raise ScaffoldValidateException()
    
    core_entrypoint_configure_container_name = None
    try:
      core_entrypoint_configure_container_name = self.managed_services_docker_compose.entrypoint_configure_container_name
      entrypoint_configure_container = self.docker_client.containers.get(core_entrypoint_configure_container_name)
    except docker_errors.NotFound:
      container_missing_message = f"{bcolors.FAIL}Container not found: {core_entrypoint_configure_container_name}{bcolors.ENDC}"
      suggestion_message = f"{bcolors.BOLD}Run 'docker ps -a' and report a bug at https://github.com/Stoobly/stoobly-agent/issues{bcolors.ENDC}"
      error_message = f"{container_missing_message}\n\n{suggestion_message}"
      raise ScaffoldValidateException(error_message)

    # NOTE: we should check the correct workflow mode is enabled one day
    # That's not currently queryable

    print(f"{bcolors.OKGREEN}Done validating core components for workflow: {self.workflow_name}, success!\n{bcolors.ENDC}")

    return True


