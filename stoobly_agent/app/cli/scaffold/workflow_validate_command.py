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

  # Gateway core service runs in all workflows
  def validate_gateway_service(self):
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

  def validate_core_services(self):
    self.validate_gateway_service()
    self.validate_mock_ui_service()
    self.validate_init_containers(self.managed_services_docker_compose.init_container_name, self.managed_services_docker_compose.configure_container_name)
    self.validate_entrypoint_service()

  def validate(self) -> bool:
    print(f"Validating workflow: {self.workflow_name}\n")
    print(f"Validating core services: {CORE_SERVICES}")

    self.validate_core_services()

    return True


