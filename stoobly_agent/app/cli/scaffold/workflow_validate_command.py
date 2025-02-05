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

from .app import App


class WorkflowValidateCommand(WorkflowCommand, ValidateCommand):
  def __init__(self, app: App, **kwargs):
    WorkflowCommand.__init__(self, app, **kwargs)
    ValidateCommand.__init__(self)
    self.managed_services_docker_compose = ManagedServicesDockerCompose(target_workflow_name=self.workflow_name)

  def validate_core_components(self):
    print(f"Validating core component: {CORE_GATEWAY_SERVICE_NAME}")
    gateway_container_name = self.managed_services_docker_compose.gateway_container_name
    gateway_container = self.docker_client.containers.get(gateway_container_name)
    if not gateway_container or (gateway_container.status != 'running'):
      raise ScaffoldValidateException(f"Container '{gateway_container_name}' not found for service '{CORE_GATEWAY_SERVICE_NAME}'")

    print(f"Validating core component: {CORE_MOCK_UI_SERVICE_NAME}")
    mock_ui_container_name = self.managed_services_docker_compose.mock_ui_container_name
    mock_ui_container = self.docker_client.containers.get(mock_ui_container_name)
    if not mock_ui_container or (mock_ui_container.status != 'running'):
      raise ScaffoldValidateException(f"Container '{mock_ui_container_name}' not found for service '{CORE_MOCK_UI_SERVICE_NAME}'")

  def validate_no_core_components(self):
    try:
      core_gateway_container = self.docker_client.containers.get(self.managed_services_docker_compose.gateway_container_name)
      if core_gateway_container:
        raise ScaffoldValidateException(f"Gateway container is running when it shouldn't: {core_gateway_container.name}")
    except docker_errors.NotFound:
      pass
    
    try:
      core_mock_ui_container_name = self.docker_client.containers.get(self.managed_services_docker_compose.mock_ui_container_name)
      if core_mock_ui_container_name:
        raise ScaffoldValidateException(f"Stoobly UI container is running when it shouldn't: {core_mock_ui_container_name.name}")
    except docker_errors.NotFound:
      pass
    
    print(f"Skipping validating core component: {CORE_GATEWAY_SERVICE_NAME}")
    print(f"Skipping validating core component: {CORE_MOCK_UI_SERVICE_NAME}")

  
  def validate(self) -> bool:
    print(f"Validating workflow: {self.workflow_name}")
    print(f"Validating core components: {CORE_SERVICES}")

    if self.workflow_name == WORKFLOW_TEST_TYPE:
      # Don't validate the gateway and mock_ui core components in the "test" workflow 
      self.validate_no_core_components()
    else:
      self.validate_core_components()

    self.validate_init_containers(self.managed_services_docker_compose.init_container_name, self.managed_services_docker_compose.configure_container_name)

    print(f"Validating core component: {CORE_ENTRYPOINT_SERVICE_NAME}")

    try:
      core_entrypoint_init_container_name = self.managed_services_docker_compose.entrypoint_init_container_name
      entrypoint_init_container = self.docker_client.containers.get(core_entrypoint_init_container_name)
    except docker_errors.NotFound:
      raise ScaffoldValidateException(f"Container not found: {core_entrypoint_init_container_name}")

    try:
      core_entrypoint_configure_container_name = self.managed_services_docker_compose.entrypoint_configure_container_name
      entrypoint_configure_container = self.docker_client.containers.get(core_entrypoint_configure_container_name)
    except docker_errors.NotFound:
      raise ScaffoldValidateException(f"Container not found: {core_entrypoint_configure_container_name}")

    # NOTE: we should check the correct workflow mode is enabled one day
    # That's not currently queryable

    print(f"Done validating workflow: {self.workflow_name}, success!")
    print()

    return True


