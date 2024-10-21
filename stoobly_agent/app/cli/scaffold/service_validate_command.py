import pdb

from docker.models.containers import Container
from pathlib import Path
from requests.adapters import HTTPAdapter
from urllib3 import Retry
import yaml
from stoobly_agent.app.cli.scaffold.constants import DIST_FOLDER_NAME, STOOBLY_HOME_DIR
from stoobly_agent.app.cli.scaffold.service_command import ServiceCommand
from stoobly_agent.app.cli.scaffold.validate_command import ValidateCommand
from stoobly_agent.app.cli.scaffold.service_composite import ServiceComposite
from stoobly_agent.config.data_dir import DATA_DIR_NAME

from .app import App

import requests


class ServiceValidateCommand(ServiceCommand, ValidateCommand):
  def __init__(self, app: App, **kwargs):
    # super().__init__(app, **kwargs)
    ServiceCommand.__init__(self, app, **kwargs)
    ValidateCommand.__init__(self)

    self.workflow_name = kwargs['workflow_name']
    self.hostname = self.service_config.hostname
    self.service_composite = ServiceComposite(app_dir_path=app.dir_path, target_workflow_name=self.workflow_name, service_name=self.service_name, hostname=self.hostname)

  # @property
  # def app_name(self):
  #   return self.app.name

  def is_local(self):
    with open (self.service_composite.docker_compose_path,'rb') as f:
      docker_compose_file_content = yaml.safe_load(f)
      if docker_compose_file_content and docker_compose_file_content.get('services'):
        return True

      # line_count = 0
      # for line in f:
      #   line_count += 1
      # if line_count > 3:
      #   return True

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

    assert response.ok
 
  def validate_hostname(self, url: str) -> None:
    self.hostname_reachable(url)

    # TODO: add to /etc/hosts? provide route inside Docker container with --add-host

    # TODO: check logs of proxy. lifecycle hook for custom logging?
    # TODO: does mitmproxy support json logging?

  # Check dist folder mounted into container
  def validate_dist_folder(self, container: Container):
    dist_folder_exists = False
    # TODO: add destination folder as constant, use in main path too
    dist_folder = f"{STOOBLY_HOME_DIR}/{self.workflow_name}/{DIST_FOLDER_NAME}"

    volume_mounts = container.attrs['Mounts']
    for volume_mount in volume_mounts:
      if volume_mount['Destination'] == dist_folder:
        dist_folder_exists = True
        break
    assert dist_folder_exists

    # Check contents of dist folder to confirm it's shared
    # Only the running proxy containers will be checkable
    if not container.status == 'exited':
      exec_result = container.exec_run(f"ls {dist_folder}")
      output = exec_result.output
      if 'shared_file.txt' not in output.decode('ascii'):
        assert False
  
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
    assert service_proxy_container.attrs
 
    self.validate_dist_folder(service_proxy_container)

    self.proxy_environment_variables_exist(service_proxy_container)

  def validate_service_container(self):
    pass
  
  def validate(self, **kwargs) -> bool:
    print(f"Validating service_name: {self.service_name}")
    # print(f"hostname: {self.service_composite.hostname}")
    # print(f"is_local: {self.is_local()}")

    url = f"http://{self.hostname}"
    if self.workflow_name not in ['ci', 'test']:
      self.validate_hostname(url)

    all_containers = self.docker_client.containers.list(all=True)
    self.validate_init_containers(all_containers, self.service_composite.service_init_container_name, self.service_composite.service_configure_container_name)

    # Service init containers have a mounted dist folder unlike the core init container
    init_container = self.docker_client.containers.get(self.service_composite.service_init_container_name)
    self.validate_dist_folder(init_container)

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

    return True

