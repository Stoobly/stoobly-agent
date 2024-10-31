import pdb

from docker import errors as docker_errors
from docker.models.containers import Container

from stoobly_agent.app.cli.scaffold.constants import WORKFLOW_TEST_TYPE
from stoobly_agent.app.cli.scaffold.core_components_composite import (
  CoreComponentsComposite,
)
from stoobly_agent.app.cli.scaffold.templates.constants import CORE_ENTRYPOINT_SERVICE_NAME, CORE_GATEWAY_SERVICE_NAME, CORE_MOCK_UI_SERVICE_NAME, CORE_SERVICES
from stoobly_agent.app.cli.scaffold.validate_command import ValidateCommand
from stoobly_agent.app.cli.scaffold.validate_exceptions import ScaffoldValidateGatewayMissingException, ScaffoldValidateStooblyUiMissingException
from stoobly_agent.app.cli.scaffold.workflow_command import WorkflowCommand
from stoobly_agent.config.data_dir import DATA_DIR_NAME

from .app import App


class WorkflowValidateCommand(WorkflowCommand, ValidateCommand):
  def __init__(self, app: App, **kwargs):
    WorkflowCommand.__init__(self, app, **kwargs)
    ValidateCommand.__init__(self)
    self.core_components_composite = CoreComponentsComposite(target_workflow_name=self.workflow_name)

  def validate_core_components(self):
    gateway_up = False
    mock_ui_up = False
    gateway_container = Container()

    # docker ps
    containers = self.docker_client.containers.list()
    for container in containers:
      if container.name == self.core_components_composite.core_gateway_container_name:
        gateway_up = True
        gateway_container = container
      elif container.name == self.core_components_composite.core_mock_ui_container_name:
        mock_ui_up = True

    print(f"Validating core component: {CORE_GATEWAY_SERVICE_NAME}")
    if not gateway_up:
      raise ScaffoldValidateGatewayMissingException(f"Gateway container is missing: {self.core_components_composite.core_gateway_container_name}")
    self.validate_detached(gateway_container)

    print(f"Validating core component: {CORE_MOCK_UI_SERVICE_NAME}")
    if not mock_ui_up:
      raise ScaffoldValidateStooblyUiMissingException(f"Container '{self.core_components_composite.core_mock_ui_container_name}' is missing for service '{CORE_MOCK_UI_SERVICE_NAME}'")

    return True

  def validate_no_core_components(self):
    try:
      core_gateway_container = self.docker_client.containers.get(self.core_components_composite.core_gateway_container_name)
      if core_gateway_container:
        assert False
    except docker_errors.NotFound:
      assert True
    
    try:
      core_mock_ui_container_name = self.docker_client.containers.get(self.core_components_composite.core_mock_ui_container_name)
      if core_mock_ui_container_name:
        assert False
    except docker_errors.NotFound:
      assert True
    
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

    # docker ps -a
    all_containers = self.docker_client.containers.list(all=True)
    self.validate_init_containers(all_containers, self.core_components_composite.core_init_container_name, self.core_components_composite.core_configure_container_name)

    print(f"Validating core component: {CORE_ENTRYPOINT_SERVICE_NAME}")
    entrypoint_init_container = self.docker_client.containers.get(self.core_components_composite.core_entrypoint_init_container_name)
    entrypoint_configure_container = self.docker_client.containers.get(self.core_components_composite.core_entrypoint_configure_container_name)
    assert entrypoint_init_container
    assert entrypoint_configure_container


    # NOTE: we should check the correct workflow mode is enabled one day
    # That's not currently queryable

    print()

    return True


