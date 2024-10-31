import pdb
from time import sleep
from typing import List

import docker
from docker.models.containers import Container

from stoobly_agent.app.cli.scaffold.validate_exceptions import ScaffoldValidateNotDetachedException
from stoobly_agent.config.data_dir import DATA_DIR_NAME


class ValidateCommand():
  def __init__(self):
    self.docker_client = docker.from_env()

  def validate_init_containers(self, containers: List[Container], init_container_name, configure_container_name) -> None:
    print(f"Validating setup containers: {init_container_name}, {configure_container_name}")

    init_container = self.docker_client.containers.get(init_container_name)
    logs = init_container.logs()
    if logs or init_container.status != 'exited' or init_container.attrs['State']['ExitCode'] != 0:
      assert False

    # Configure container can take slightly longer than expected to finish so retry
    configure_container_ran = False
    tries = 10
    for i in range(tries):
      configure_container = self.docker_client.containers.get(configure_container_name)
      if configure_container.status == 'exited' and configure_container.attrs['State']['ExitCode'] == 0:
        configure_container_ran = True
        break
      else:
        sleep(0.1)
    
    assert configure_container_ran
  
  def validate_detached(self, container: Container) -> None:
    print(f"Validating detached for: {container.name}")
    
    if not container.attrs:
      raise ScaffoldValidateNotDetachedException(f"Container is missing: {container.name}")

    volume_mounts = container.attrs['Mounts']
    for volume_mount in volume_mounts:
      if DATA_DIR_NAME in volume_mount['Source']:
        return

    raise ScaffoldValidateNotDetachedException(f"Data directory is missing from container: {container.name}")

