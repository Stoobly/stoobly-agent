import os
import pdb
import socket
import time

from collections import Counter
from docker import errors as docker_errors
from pathlib import Path

import yaml
from docker.models.containers import Container

from stoobly_agent.app.cli.scaffold.constants import (
  PUBLIC_FOLDER_NAME,
  SERVICES_NAMESPACE,
  STOOBLY_DATA_DIR,
  WORKFLOW_RECORD_TYPE,
  WORKFLOW_TEST_TYPE,
)
from stoobly_agent.app.cli.scaffold.docker.constants import APP_INGRESS_NETWORK_TEMPLATE
from stoobly_agent.app.cli.scaffold.hosts_file_manager import HostsFileManager
from stoobly_agent.app.cli.scaffold.service_command import ServiceCommand
from stoobly_agent.app.cli.scaffold.service_docker_compose import ServiceDockerCompose
from stoobly_agent.app.cli.scaffold.validate_command import ValidateCommand
from stoobly_agent.app.cli.scaffold.validate_exceptions import ScaffoldValidateException
from stoobly_agent.config.data_dir import DATA_DIR_NAME
from stoobly_agent.lib.logger import bcolors

from .app import App


class ServiceWorkflowValidateCommand(ServiceCommand, ValidateCommand):
  def __init__(self, app: App, **kwargs):
    ServiceCommand.__init__(self, app, **kwargs)
    ValidateCommand.__init__(self)

    self.workflow_name = kwargs['workflow_name']
    self.hostname = self.service_config.hostname
    self.service_docker_compose = ServiceDockerCompose(
      app_dir_path=app.dir_path, target_workflow_name=self.workflow_name, service_name=self.service_name, hostname=self.hostname
    )

  @property
  def public_dir_path(self):
    return os.path.join(self.workflow_path, PUBLIC_FOLDER_NAME)
  
  @property
  def workflow_path(self):
    return os.path.join(
      self.data_dir_path,
      self.workflow_relative_path
    )
  @property
  def workflow_relative_path(self):
    return os.path.join(
      self.service_relative_path,
      self.workflow_name
    )

  def is_local(self):
    with open (self.service_docker_compose.docker_compose_path,'rb') as f:
      docker_compose_file_content = yaml.safe_load(f)
      if docker_compose_file_content and docker_compose_file_content.get('services'):
        return True

      # We can potentially check the port too someday

    return False

  def is_external(self):
    return not self.is_local()

  def hostname_reachable(self, hostname: str, port: int) -> bool:
    print(f"Validating connection to hostname: {hostname}, port: {port}")
    timeout = 1
    retries = 15
    delay = 0.100

    for attempt in range(retries):
      try:
        with socket.create_connection((hostname, port), timeout=timeout):
          return True
      except (socket.timeout, socket.error):
        if attempt < retries - 1:
          time.sleep(delay)

    hostname_not_reachable_message = f"{bcolors.FAIL}Connection failed to hostname: {hostname}, port: {port}, num_retries: {retries}{bcolors.ENDC}"
    suggestion_message = f"{bcolors.BOLD}Try confirming that {hostname} is reachable from your machine or environment.{bcolors.ENDC}"
    error_message = f"{hostname_not_reachable_message}\n\n{suggestion_message}"
    raise ScaffoldValidateException(error_message)

  # Check if hostname is defined in hosts file
  def hostname_exists(self, hostname: str) -> bool:
    print(f"Validating hostname exists in hosts file for hostname: {hostname}")

    hosts_file_manager = HostsFileManager()
    host_mapping = hosts_file_manager.find_host(hostname)
    if host_mapping:
      print(f"Correct hosts mapping found for {hostname}")
      return True

    hosts_file_path = hosts_file_manager.get_hosts_file_path()

    missing_host_message = f"{bcolors.FAIL}Missing hosts mapping for {hostname}{bcolors.ENDC}"
    suggestion_message = f"{bcolors.BOLD}Confirm hostname '{hostname}' is in your hosts file at '{hosts_file_path}'. If not there, please add it{bcolors.ENDC}"
    error_message = f"{missing_host_message}\n\n{suggestion_message}"
    raise ScaffoldValidateException(error_message)
 
  def validate_hostname(self, hostname: str, port: int) -> None:
    print(f"Validating hostname: {hostname}")

    self.hostname_exists(hostname)

    self.hostname_reachable(hostname, port)

    # TODO: check logs of proxy. lifecycle hook for custom logging? Does mitmproxy support json logging?

  def validate_internal_hostname(self, url: str) -> None:
    print(f"Validating hostname inside Docker network, url: {url}")
    
    # See WorkflowRunCommand for how 'network' is generated
    # Debug command=f"curl -k --max-time {timeout_seconds} {url} --verbose",
    network = f"{self.workflow_name}.{self.app.network}" 
    timeout_seconds = 1
    http_code_format = '"%{http_code}"'
    output = self.docker_client.containers.run(
      image='curlimages/curl:8.11.0',
      command=f"curl -k -s -o /dev/null -w {http_code_format} --max-time {timeout_seconds} {url}",
      network=APP_INGRESS_NETWORK_TEMPLATE.format(network=network),
      stderr=True,
      remove=True,
    )

    # Note: 499 error could also mean success because it shows the proxy
    # connection is working, but we haven't recorded anything yet
    logs = output.decode('ascii')
    if logs != '200' and  logs != '499':
      raise ScaffoldValidateException(f"Error reaching {url} from inside Docker network with logs: \n{logs}")

  # Check public folder exists in container
  def validate_public_folder(self, container: Container):
    
    if self.workflow_name == WORKFLOW_RECORD_TYPE:
      print(f"Skipping validating public folder in workflow: {self.workflow_name}, container: {container.name}")
      return

    print(f"Validating public folder in container: {container.name}")

    data_dir_mounted = False
    volume_mounts = container.attrs['Mounts']

    for volume_mount in volume_mounts:
      if volume_mount['Destination'] == STOOBLY_DATA_DIR:
        data_dir_mounted = True
        break
    if not data_dir_mounted:
      raise ScaffoldValidateException(f"Data directory is not mounted for: {container.name}")

    # Only the running proxy containers will be checkable
    if container.status == 'exited':
      print(f"Skipping validating public folder contents because container is exited: {container.name}")
      return

    # Check contents of public folder to confirm it's shared
    public_folder_path = f"{PUBLIC_FOLDER_NAME}"
    exec_result = container.exec_run(f"ls -A {public_folder_path}")
    output = exec_result.output

    public_folder_contents_container = output.decode('ascii').split('\n')
    if public_folder_contents_container[-1] == '':
      public_folder_contents_container.pop()
    public_folder_contents_scaffold = os.listdir(self.public_dir_path)

    if Counter(public_folder_contents_container) != Counter(public_folder_contents_scaffold):
      raise ScaffoldValidateException(f"public folder was not mounted properly, expected {self.public_dir_path} to exist in container path {public_folder_path}")

  def validate_proxy_container(self, service_proxy_container: Container):
    print(f"Validating proxy container: {service_proxy_container.name}")

    if service_proxy_container.status == 'exited' or service_proxy_container.attrs['State']['ExitCode'] != 0:
      raise ScaffoldValidateException(f"Proxy container is exited: {service_proxy_container.name}")
    if service_proxy_container.status != 'running':
      raise ScaffoldValidateException(f"Proxy container is not running: {service_proxy_container.name}")
    if not service_proxy_container.attrs:
      raise ScaffoldValidateException(f"Container attributes are missing for: {service_proxy_container.name}")

    if not self.service_config.detached:
      self.validate_public_folder(service_proxy_container)

  def validate_service_container(self):
    pass
  
  def validate(self) -> bool:
    print(f"Validating service: {self.service_name}")

    url = self.service_config.url

    if self.service_config.hostname and self.workflow_name not in [WORKFLOW_TEST_TYPE]:
      self.validate_hostname(self.hostname, self.service_config.port)
    
    # Test workflow won't expose services that are detached and have a hostname to the host such as assets.
    # Need to test connection from inside the Docker network
    if self.service_config.hostname and self.workflow_name == WORKFLOW_TEST_TYPE:
      try:
        self.validate_internal_hostname(url)
      except ScaffoldValidateException:
        time.sleep(1)
        # Retry once
        self.validate_internal_hostname(url)

    self.validate_init_containers(self.service_docker_compose.init_container_name, self.service_docker_compose.configure_container_name)

    # Service init containers have a mounted dist folder unlike the core init container
    init_container = self.docker_client.containers.get(self.service_docker_compose.init_container_name)
    self.validate_public_folder(init_container)

    if self.service_config.hostname:
      try:
        service_proxy_container = self.docker_client.containers.get(self.service_docker_compose.proxy_container_name)
      except docker_errors.NotFound:
        error_message = self._ValidateCommand__generate_container_not_found_error(self.service_docker_compose.proxy_container_name)
        raise ScaffoldValidateException(error_message)

      self.validate_proxy_container(service_proxy_container)

    # External services won't have a container to check
    if self.is_local() or self.service_config.detached:
      container_name = self.service_docker_compose.container_name
      try:
        service_container = self.docker_client.containers.get(container_name)
      except docker_errors.NotFound:
        error_message = self._ValidateCommand__generate_container_not_found_error(container_name)
        raise ScaffoldValidateException(error_message)
      if service_container.status == 'exited' or service_container.attrs['State']['ExitCode'] != 0:
        raise ScaffoldValidateException(f"Custom container is exited: {service_container.name}")
      if service_container.status != 'running':
        raise ScaffoldValidateException(f"Custom container is not running: {service_container.name}")
    
    if self.is_local():
      print(f"Validating local user defined service: {self.service_name}")
      # Validate docker-compose path exists
      docker_compose_path = f"{self.app_dir_path}/{DATA_DIR_NAME}/{SERVICES_NAMESPACE}/{self.service_docker_compose.service_name}/{self.workflow_name}/docker-compose.yml"
      destination_path = Path(docker_compose_path)

      if not destination_path.exists():
        message = f"{bcolors.FAIL}Docker Compose file does not exist: {destination_path}{bcolors.ENDC}"
        suggestion_message = f"{bcolors.BOLD}A missing Docker Compose file often means it got deleted by accident. Please restore from backup or rerun the scaffold service create command.{bcolors.ENDC}"
        error_message = f"{message}\n\n{suggestion_message}"
        raise ScaffoldValidateException(error_message)
      if not destination_path.is_file():
        raise ScaffoldValidateException(f"Docker compose path is not a file: {destination_path}")

      # Validate docker-compose.yml file has the service defined
      with open(destination_path) as f:
        if self.service_name not in f.read():
          message = f"{bcolors.FAIL}Custom container service is not defined in Docker Compose file: {destination_path}{bcolors.ENDC}"
          suggestion_message = f"{bcolors.BOLD}Please add your service definition. See https://docs.docker.com/reference/compose-file/services {bcolors.ENDC}"
          error_message = f"{message}\n\n{suggestion_message}"
          raise ScaffoldValidateException(error_message)

    if self.service_config.detached:
      self.validate_detached(service_container)

    print(f"{bcolors.OKGREEN}✔ Done validating service: {self.service_name}, success!{bcolors.ENDC}\n")

    return True

