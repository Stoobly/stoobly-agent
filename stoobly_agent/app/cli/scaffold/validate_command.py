import pdb
import re
from time import sleep

import docker
from docker import errors as docker_errors
from docker.models.containers import Container

from stoobly_agent.app.cli.scaffold.validate_exceptions import ScaffoldValidateException
from stoobly_agent.config.data_dir import DATA_DIR_NAME


class ValidateCommand():
  def __init__(self):
    self.docker_client = docker.from_env()

  # Some containers like init and configure can take longer than expected to finish so retry
  def __get_container(self, container_name: str) -> Container:
    tries = 30
    for _ in range(tries):
      try:
        container = self.docker_client.containers.get(container_name)
        return container
      except docker_errors.NotFound:
        sleep(0.5)

    raise ScaffoldValidateException(f"Container not found: {container_name}")

  def validate_init_containers(self, init_container_name, configure_container_name) -> None:
    print(f"Validating setup containers: {init_container_name}, {configure_container_name}")


    init_container = self.__get_container(init_container_name)
    logs = init_container.logs()
    if logs and re.search('error', str(logs), re.IGNORECASE):
      raise ScaffoldValidateException(f"Error logs potentially detected in: {init_container_name}")
    if init_container.status != 'exited' or init_container.attrs['State']['ExitCode'] != 0:
      raise ScaffoldValidateException(f"init container {init_container_name} exited with: {init_container.attrs['State']['ExitCode']}")

    configure_container = self.__get_container(configure_container_name)

    configure_container_ran = False
    if configure_container.status == 'exited' and configure_container.attrs['State']['ExitCode'] == 0:
      configure_container_ran = True
    if not configure_container_ran:
      raise ScaffoldValidateException(f"configure container {configure_container_name} exited with: {configure_container.attrs['State']['ExitCode']}")
  
  def validate_detached(self, container: Container) -> None:
    print(f"Validating detached for: {container.name}")
    
    if not container.attrs:
      raise ScaffoldValidateException(f"Container is missing: {container.name}")

    volume_mounts = container.attrs['Mounts']
    for volume_mount in volume_mounts:
      if DATA_DIR_NAME in volume_mount['Source']:
        return

    raise ScaffoldValidateException(f"Data directory is missing from container: {container.name}")

