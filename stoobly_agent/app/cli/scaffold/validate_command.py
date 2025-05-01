import pdb
import re
from time import sleep
from typing import Union

import docker
from docker import errors as docker_errors
from docker.models.containers import Container

from stoobly_agent.app.cli.scaffold.validate_exceptions import ScaffoldValidateException
from stoobly_agent.config.data_dir import DATA_DIR_NAME
from stoobly_agent.lib.logger import bcolors


class ValidateCommand():
  def __init__(self):
    self.docker_client = docker.from_env()

  def __generate_container_not_found_error(self, container_name: Union[str, None]) -> str:
    not_found_error_message = f"{bcolors.FAIL}Container not found: {container_name}{bcolors.ENDC}"
    suggestion_message = f"{bcolors.BOLD}Run 'docker ps -a | grep {container_name}'. If found, then inspect the logs with 'docker logs {container_name}'{bcolors.ENDC}"
    error_message = f"{not_found_error_message}\n\n{suggestion_message}"

    return error_message

  # Some containers like init and configure can take longer than expected to finish so retry
  def __get_container_with_retries(self, container_name: str) -> Container:
    tries = 30
    for _ in range(tries):
      try:
        container = self.docker_client.containers.get(container_name)
        return container
      except docker_errors.NotFound:
        sleep(0.5)

    error_message = self.__generate_container_not_found_error(container_name)
    raise ScaffoldValidateException(error_message)

  def validate_init_containers(self, init_container_name, configure_container_name) -> None:
    print(f"Validating setup containers: {init_container_name}, {configure_container_name}")

    init_container = self.__get_container_with_retries(init_container_name)
    logs = init_container.logs()

    if logs and re.search('error', str(logs), re.IGNORECASE):
      error_found_message = f"{bcolors.FAIL}Error logs potentially detected in: {init_container_name}{bcolors.ENDC}"
      suggestion_message = f"{bcolors.BOLD}Run 'docker logs {init_container_name}'{bcolors.ENDC}"
      error_message = f"{error_found_message}\n\n{suggestion_message}"
      raise ScaffoldValidateException(error_message)

    if init_container.status != 'exited' or init_container.attrs['State']['ExitCode'] != 0:
      init_exit_message = f"{bcolors.FAIL}init container {init_container_name} exited with: {init_container.attrs['State']['ExitCode']}{bcolors.ENDC}"
      suggestion_message = f"{bcolors.BOLD}Run 'docker logs {init_container_name}'{bcolors.ENDC}"
      error_message = f"{init_exit_message}\n\n{suggestion_message}"
      raise ScaffoldValidateException(error_message)

    configure_container = self.__get_container_with_retries(configure_container_name)

    configure_container_ran = False
    if configure_container.status == 'exited' and configure_container.attrs['State']['ExitCode'] == 0:
      configure_container_ran = True
    if not configure_container_ran:
      raise ScaffoldValidateException(f"configure container {configure_container_name} exited with: {configure_container.attrs['State']['ExitCode']}")
  
  def validate_detached(self, container: Container) -> None:
    print(f"Validating detached for: {container.name}")
    
    if not container.attrs:
      error_message = self.__generate_container_not_found_error(container.name)
      raise ScaffoldValidateException(error_message)

    volume_mounts = container.attrs['Mounts']
    for volume_mount in volume_mounts:
      if DATA_DIR_NAME in volume_mount['Source']:
        return
    
    message = f"{bcolors.FAIL}Data directory is missing from container: {container.name}{bcolors.ENDC}"
    suggestion_message = f"{bcolors.BOLD}Data directory might have failed to mount{bcolors.ENDC}"
    error_message = f"{message}\n\n{suggestion_message}"

    raise ScaffoldValidateException(error_message)

