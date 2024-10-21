import pdb
from typing import List

import docker
from docker.models.containers import Container

from stoobly_agent.config.data_dir import DataDir

from .app import App

class ValidateCommand():
  def __init__(self):
    self.docker_client = docker.from_env()

  # @property
  # def app_name(self):
  #   return self.app.name

  def validate_init_containers(self, containers: List[Container], init_container_name, configure_container_name) -> None:
    init_container_ran = False
    configure_container_ran = False

    print(f"Validating init containers: {init_container_name}, {configure_container_name}")

    for container in containers:
      container_name = container.attrs['Name']
      if container_name == init_container_name:
        logs = container.logs()
        # No errors in log or container status
        if not logs and container.attrs['State']['Status'] == 'exited' and container.attrs['State']['ExitCode'] == 0:
          init_container_ran = True

      if container_name == configure_container_name:
        if container.attrs['State']['Status'] == 'exited' and container.attrs['State']['ExitCode'] == 0:
          configure_container_ran = True

    assert init_container_ran
    assert configure_container_ran
  
  def validate_detached(self, container: Container) -> None:
    if not container.attrs:
      assert False

    volume_mounts = container.attrs['Mounts']

    for volume_mount in volume_mounts:
      if DataDir.DATA_DIR_NAME in volume_mount['Source']:
        return

    assert False

  # def validate(self, **kwargs):
  #   print(f"Validating workflow: {self.workflow_name}")
  #
  #   self.validate_core_components()

