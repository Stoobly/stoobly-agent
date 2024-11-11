from collections import Counter
import os
from pathlib import Path
import pdb

from docker.models.containers import Container
import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry
import yaml

from stoobly_agent.app.cli.scaffold.constants import (
  FIXTURES_FOLDER_NAME,
  STOOBLY_HOME_DIR,
  WORKFLOW_RECORD_TYPE,
  WORKFLOW_TEST_TYPE,
)
from stoobly_agent.app.cli.scaffold.service_command import ServiceCommand
from stoobly_agent.app.cli.scaffold.service_composite import ServiceComposite
from stoobly_agent.app.cli.scaffold.validate_command import ValidateCommand
from stoobly_agent.app.cli.scaffold.validate_exceptions import ScaffoldValidateException
from stoobly_agent.config.data_dir import DATA_DIR_NAME

from .app import App


class ServiceValidateCommand(ServiceCommand, ValidateCommand):
  def __init__(self, app: App, **kwargs):
    ServiceCommand.__init__(self, app, **kwargs)
    ValidateCommand.__init__(self)

    self.workflow_name = kwargs['workflow_name']
    self.hostname = self.service_config.hostname
    self.service_composite = ServiceComposite(app_dir_path=app.dir_path, target_workflow_name=self.workflow_name, service_name=self.service_name, hostname=self.hostname)

  @property
  def fixtures_dir_path(self):
    return os.path.join(self.workflow_path, FIXTURES_FOLDER_NAME)
  
  @property
  def workflow_path(self):
    return os.path.join(
      self.scaffold_dir_path,
      self.workflow_relative_path
    )
  @property
  def workflow_relative_path(self):
    return os.path.join(
      self.service_relative_path,
      self.workflow_name
    )

  def is_local(self):
    with open (self.service_composite.docker_compose_path,'rb') as f:
      docker_compose_file_content = yaml.safe_load(f)
      if docker_compose_file_content and docker_compose_file_content.get('services'):
        return True

      # We can potentially check the port too someday

    return False

  def is_external(self):
    return not self.is_local()

  def hostname_reachable(self, url: str) -> None:
    # Retry HTTP request. Source: https://stackoverflow.com/questions/15431044/can-i-set-max-retries-for-requests-request
    s = requests.Session()
    retries = Retry(total=5,
                    backoff_factor=0.1,
                    status_forcelist=[ 500, 502, 503, 504 ])
    s.mount('http://', HTTPAdapter(max_retries=retries))
    response = s.get(url=url)

    if not response.ok:
      raise ScaffoldValidateException(f"Host is not reachable: {url}")
 
  def validate_hostname(self, url: str) -> None:
    print(f"Validating hostname: {url}")
    self.hostname_reachable(url)

    # TODO: add to /etc/hosts? provide route inside Docker container with --add-host

    # TODO: check logs of proxy. lifecycle hook for custom logging?
    # TODO: does mitmproxy support json logging?

  # TODO: might be better in WorkflowValidateCommand
  # Check fixtures folder mounted into container
  def validate_fixtures_folder(self, container: Container):
    
    if self.workflow_name == WORKFLOW_RECORD_TYPE:
      print(f"Skipping validating fixtures folder in workflow: {self.workflow_name}")
      return

    print(f"Validating fixtures folder in container: {container.name}")

    data_dir_mounted = False
    # TODO: add destination folder as constant, use in main path too
    data_dir = f"{STOOBLY_HOME_DIR}/{DATA_DIR_NAME}"
    volume_mounts = container.attrs['Mounts']
    for volume_mount in volume_mounts:
      if volume_mount['Destination'] == data_dir:
        data_dir_mounted = True
        break
    if not data_dir_mounted:
      raise ScaffoldValidateException(f"Data directory is not mounted for: {container.name}")

    # Only the running proxy containers will be checkable
    if container.status == 'exited':
      print(f"Skipping validating fixtures folder contents because container is exited: {container.name}")
      return

    # Check contents of fixtures folder to confirm it's shared
    fixtures_folder_path = f"{STOOBLY_HOME_DIR}/{self.workflow_name}/{FIXTURES_FOLDER_NAME}"
    exec_result = container.exec_run(f"ls -A {fixtures_folder_path}")
    output = exec_result.output

    fixtures_folder_contents_container = output.decode('ascii').split('\n')
    if fixtures_folder_contents_container[-1] == '':
      fixtures_folder_contents_container.pop()
    fixtures_folder_contents_scaffold = os.listdir(self.fixtures_dir_path)

    if Counter(fixtures_folder_contents_container) != Counter(fixtures_folder_contents_scaffold):
      raise ScaffoldValidateException('Contents of fixtures folder is not equal')

  # TODO: might not need this if the hostname is reachable and working
  def proxy_environment_variables_exist(self, container: Container) -> None:
    environment_variables = container.attrs['Config']['Env']
    virtual_host_exists = False
    virtual_port_exists = False
    virtual_proto_exists = False

    for environment_variable in environment_variables:
      environment_variable_name, environment_variable_value = environment_variable.split('=')
      if environment_variable_name == 'VIRTUAL_HOST':
        virtual_host_exists = True
      elif environment_variable_name == 'VIRTUAL_PORT':
        virtual_port_exists = True
      elif environment_variable_name == 'VIRTUAL_PROTO':
        virtual_proto_exists = True

    assert (virtual_host_exists and virtual_port_exists and virtual_proto_exists)
  
  def validate_proxy_container(self, service_proxy_container: Container):
    print(f"Validating proxy container: {service_proxy_container.name}")
    if not service_proxy_container.attrs:
      raise ScaffoldValidateException(f"Container attributes are missing for: {container.name}")

    if not self.service_config.detached:
      self.validate_fixtures_folder(service_proxy_container)

    self.proxy_environment_variables_exist(service_proxy_container)

  def validate_service_container(self):
    pass
  
  def validate(self, **kwargs) -> bool:
    print(f"Validating service: {self.service_name}")

    if (self.workflow_name not in [WORKFLOW_TEST_TYPE]) and self.service_config.hostname:
      url = f"{self.service_config.scheme}://{self.hostname}"
      self.validate_hostname(url)

    self.validate_init_containers(self.service_composite.service_init_container_name, self.service_composite.service_configure_container_name)

    # Service init containers have a mounted dist folder unlike the core init container
    init_container = self.docker_client.containers.get(self.service_composite.service_init_container_name)
    self.validate_fixtures_folder(init_container)

    if self.service_config.hostname:
      service_proxy_container = self.docker_client.containers.get(self.service_composite.service_proxy_container_name)
      self.validate_proxy_container(service_proxy_container)

    if self.is_local():
      print(f"Validating local user defined service: {self.service_name}")
      # Validate docker-compose path exists
      docker_compose_path = f"{self.app_dir_path}/{DATA_DIR_NAME}/docker/{self.service_composite.service_name}/{self.workflow_name}/docker-compose.yml"
      destination_path = Path(docker_compose_path)
      assert destination_path.is_file()

      # Validate docker-compose.yml file has contents
      # with open(destination_path) as f:
      #   if self.service_name not in f.read():
      #     assert False

      service_container = self.docker_client.containers.get(self.service_composite.service_container_name)
      if service_container.status == 'exited':
        return False

    if self.service_config.detached:
      service_container = self.docker_client.containers.get(self.service_composite.service_container_name)
      self.validate_detached(service_container)

    print()

    return True

