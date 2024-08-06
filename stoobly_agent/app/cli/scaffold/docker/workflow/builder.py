import os
import pdb

from ...constants import DIST_FOLDER_NAME, SERVICE_HOSTNAME, SERVICE_HOSTNAME_ENV, SERVICE_PORT, SERVICE_PORT_ENV, SERVICE_SCHEME, SERVICE_SCHEME_ENV, STOOBLY_HOME_DIR
from ..builder import Builder
from ..service.builder import ServiceBuilder

class WorkflowBuilder(Builder):

  def __init__(self, workflow_path: str, service_builder: ServiceBuilder):
    self.__workflow_name = os.path.basename(workflow_path)
    super().__init__(workflow_path, f"docker-compose.{self.__workflow_name}.yml")

    self.__context = './'
    self.__profiles = [self.__workflow_name]

    if not service_builder:
      service_path = os.path.dirname(workflow_path)
      service_builder = ServiceBuilder(service_path)

    self.__service_builder = service_builder

    if self.config.hostname:
      self.with_public_network()

    self.load()
  
  @property
  def app(self):
    return f"{self.namespace}.app"

  @property
  def base_compose_file_path(self):
    return os.path.relpath(self.service_builder.compose_file_path, self.dir_path)

  @property
  def init(self):
    return f"{self.namespace}.init"

  @property
  def config(self):
    return self.service_builder.config

  @property
  def configure(self):
    return f"{self.namespace}.configure"

  @property
  def context(self):
    return self.__context

  @property
  def context_build(self):
    return {
      'context': self.context,
      'dockerfile': self.context_docker_file_path,
    }

  @property
  def context_docker_file_path(self):
    return os.path.relpath(self.service_builder.app_builder.context_docker_file_path, self.dir_path)

  @property
  def dist_volume(self):
    return f"./{DIST_FOLDER_NAME}:{STOOBLY_HOME_DIR}/{DIST_FOLDER_NAME}"

  @property
  def namespace(self):
    return f"{self.service_builder.service_name}"

  @property
  def profiles(self):
    return self.__profiles

  @property
  def proxy(self):
    return f"{self.namespace}.proxy"

  @property
  def proxy_build(self):
    return {
      'context': self.context,
      'dockerfile': self.proxy_docker_file_path,
    }

  @property
  def proxy_docker_file_path(self):
    return os.path.relpath(self.service_builder.app_builder.proxy_docker_file_path, self.dir_path)

  @property
  def service_builder(self):
    return self.__service_builder

  @property
  def workflow_name(self):
    return self.__workflow_name

  def build_all(self):
    # Resources
    self.with_network(self.service_builder.service_name)
    
    if self.config.detached:
      self.with_volume(self.service_builder.service_name)

    # Services
    self.build_init()

    if self.config.hostname:
      self.with_public_network()
      self.build_proxy()
      self.build_configure()

  def build_init(self):
    volumes = []
    service = {
      'build': self.context_build,
      'extends': self.service_builder.build_extends_init_base(self.dir_path),
      'profiles': self.profiles,
      'volumes': volumes
    }

    volumes.append(self.dist_volume)

    self.with_service(self.init, service)

  def build_configure(self):
    # If the configure_base service does not exist, we can't extend from it, return
    if not self.service_builder.configure_base_service:
      return

    depends_on = {}
    environment = {}

    service = {
      'build': self.context_build,
      'depends_on': depends_on,
      'environment': environment,
      'extends': self.service_builder.build_extends_configure_base(self.dir_path),
      'profiles': self.profiles,
    }

    environment[SERVICE_HOSTNAME_ENV] = SERVICE_HOSTNAME
    environment[SERVICE_PORT_ENV] = SERVICE_PORT
    environment[SERVICE_SCHEME_ENV] = SERVICE_SCHEME

    if self.init in self.services:
      depends_on[self.init] = {
        'condition': 'service_completed_successfully',
      }

    self.with_service(self.configure, service)

  def build_proxy(self):
    # If the proxy_base service does not exist, we can't extend from it, return
    if not self.service_builder.proxy_base_service:
      return

    depends_on = {}
    environment = {}
    extra_hosts = []
    networks = [self.service_builder.service_name]
    volumes = [self.dist_volume]

    service = {
      'build': self.proxy_build, 
      'depends_on': depends_on,
      'environment': environment,
      'extra_hosts': extra_hosts,
      'extends': self.service_builder.build_extends_proxy_base(self.dir_path),
      'networks': networks,
      'profiles': self.profiles,
      'volumes': volumes
    }

    if self.configure in self.services:
      depends_on[self.init] = {
        'condition': 'service_completed_successfully',
      }

      depends_on[self.configure] = {
        'condition': 'service_completed_successfully',
      }

    if self.config.hostname:
      environment['VIRTUAL_HOST'] = SERVICE_HOSTNAME
      environment['VIRTUAL_PORT'] = SERVICE_PORT
      environment['VIRTUAL_PROTO'] = SERVICE_SCHEME
      networks.append(self.public_network_name)

      if self.config.dns:
        service['dns'] = self.config.dns

    if self.config.detached:
      volumes.append(f"{self.service_builder.service_name}:{STOOBLY_HOME_DIR}/.stoobly")

    self.with_service(self.proxy, service)

  def write(self):
    super().write({
      'networks': self.networks,
      'services': self.services,
      'version': self.version,
      'volumes': self.volumes,
    })
