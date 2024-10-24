import pdb

from docker.models.containers import Container
from docker import errors as docker_errors

from stoobly_agent.app.cli.scaffold.constants import CORE_SERVICES, WORKFLOW_TEST_TYPE
from stoobly_agent.app.cli.scaffold.core_components_composite import (
  CoreComponentsComposite,
)
from stoobly_agent.app.cli.scaffold.validate_command import ValidateCommand
from stoobly_agent.app.cli.scaffold.workflow_command import WorkflowCommand
from stoobly_agent.config.data_dir import DATA_DIR_NAME

from .app import App


class WorkflowValidateCommand(WorkflowCommand, ValidateCommand):
  def __init__(self, app: App, **kwargs):
    WorkflowCommand.__init__(self, app, **kwargs)
    ValidateCommand.__init__(self)
    self.core_components_composite = CoreComponentsComposite(target_workflow_name=self.workflow_name)

  def validate_detached(self, container: Container) -> None:
    if not container.attrs:
      assert False

    volume_mounts = container.attrs['Mounts']

    for volume_mount in volume_mounts:
      if DATA_DIR_NAME in volume_mount['Source']:
        return

    assert False

  def validate_core_components(self):
    print(f"Validating core components: {CORE_SERVICES}")

    gateway_up = False
    mock_ui_up = False
    gateway_container = Container()

    # docker ps
    containers = self.docker_client.containers.list()
    for container in containers:
      container_name = container.attrs['Name']
      if container_name == self.core_components_composite.core_gateway_container_name:
        gateway_up = True
        gateway_container = container
      elif container_name == self.core_components_composite.core_mock_ui_container_name:
        mock_ui_up = True

    assert gateway_up
    assert mock_ui_up

    self.validate_detached(gateway_container)

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

    all_containers = self.docker_client.containers.list(all=True)

    self.validate_init_containers(all_containers, self.core_components_composite.core_init_container_name, self.core_components_composite.core_configure_container_name)


  def validate(self, **kwargs) -> bool:
    print(f"Validating workflow: {self.workflow_name}")

    # Don't validate the gateway and mock_ui core components in the "test" workflow 
    if self.workflow_name == WORKFLOW_TEST_TYPE:
      self.validate_no_core_components()
    else:
      self.validate_core_components()

    # docker ps -a
    all_containers = self.docker_client.containers.list(all=True)
    self.validate_init_containers(all_containers, self.core_components_composite.core_init_container_name, self.core_components_composite.core_configure_container_name)

    # NOTE: we should check the correct workflow mode is enabled one day
    # That's not currently queryable

    print()

    return True


