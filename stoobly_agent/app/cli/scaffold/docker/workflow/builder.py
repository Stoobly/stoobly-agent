import os
import pdb

from ...constants import (
  COMPOSE_TEMPLATE, SERVICE_HOSTNAME, 
  SERVICE_HOSTNAME_ENV, SERVICE_NAME_ENV, SERVICE_PORT, SERVICE_PORT_ENV, SERVICE_SCHEME, SERVICE_SCHEME_ENV, 
  WORKFLOW_CONTAINER_CONFIGURE_TEMPLATE, WORKFLOW_CONTAINER_INIT_TEMPLATE, WORKFLOW_CONTAINER_PROXY_TEMPLATE, WORKFLOW_NAME, WORKFLOW_NAME_ENV
)
from ..builder import Builder
from ..service.builder import ServiceBuilder

class WorkflowBuilder(Builder):

  def __init__(self, workflow_path: str, service_builder: ServiceBuilder):
    self._env = [SERVICE_NAME_ENV, WORKFLOW_NAME_ENV]
    self.__workflow_name = os.path.basename(workflow_path)
    super().__init__(workflow_path, COMPOSE_TEMPLATE.format(workflow=self.__workflow_name))

    self.__context = '../'
    self.__profiles = [WORKFLOW_NAME]

    if not service_builder:
      service_path = os.path.dirname(workflow_path)
      service_builder = ServiceBuilder(service_path)

    self.__service_builder = service_builder

  @property
  def app(self):
    return f"{self.namespace}.app"

  @property
  def base_compose_file_path(self):
    return os.path.relpath(self.service_builder.compose_file_path, self.dir_path)

  @property
  def config(self):
    return self.service_builder.config

  @property
  def configure(self):
    return WORKFLOW_CONTAINER_CONFIGURE_TEMPLATE.format(service_name=self.namespace)

  @property
  def context(self):
    return self.__context

  @property
  def context_docker_file_path(self):
    return os.path.relpath(self.service_builder.app_builder.context_docker_file_path, self.service_path)

  @property
  def init(self):
    return WORKFLOW_CONTAINER_INIT_TEMPLATE.format(service_name=self.namespace)

  @property
  def namespace(self):
    return f"{self.service_builder.service_name}"

  @property
  def profiles(self):
    return self.__profiles

  @property
  def proxy(self):
    return WORKFLOW_CONTAINER_PROXY_TEMPLATE.format(service_name=self.namespace)

  @property
  def service_builder(self):
    return self.__service_builder

  @property
  def service_path(self):
    return self.__service_builder.dir_path

  @property
  def workflow_name(self):
    return self.__workflow_name

  def build_all(self):
    # Resources
    if self.config.detached:
      self.with_volume(self.service_builder.service_name)

    # Services
    self.build_init()
    self.build_configure()

    if self.config.hostname:
      self.build_proxy() # Depends on configure, must call build_configure first

  def build_init(self):
    # If the init_base service does not exist, we can't extend from it, return
    if not self.service_builder.init_base_service:
      return

      return
    service = {
      'extends': self.service_builder.build_extends_init_base(self.dir_path),
      'profiles': self.profiles,
    }

    self.with_service(self.init, service)

  def build_configure(self):
    # If the configure_base service does not exist, we can't extend from it, return
    if not self.service_builder.configure_base_service:
      return

    depends_on = {}

    service = {
      'depends_on': depends_on,
      'extends': self.service_builder.build_extends_configure_base(self.dir_path),
      'profiles': self.profiles,
    }

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
    networks = {}

    service = {
      'depends_on': depends_on,
      'extends': self.service_builder.build_extends_proxy_base(self.dir_path),
      'networks': networks,
      'profiles': self.profiles,
    }

    if self.configure in self.services:
      depends_on[self.init] = {
        'condition': 'service_completed_successfully',
      }

      depends_on[self.configure] = {
        'condition': 'service_completed_successfully',
      }

    # Expose this container service to the public network 
    # so that it is accessible to other Stoobly services
    networks[self.egress_network_name] = {}

    self.with_service(self.proxy, service)

  def env_dict(self):
    env = {}
    for e in self._env:
      env[e] = '${' + e + '}'
    return env

  def initialize_custom_file(self):
    dest = self.custom_compose_file_path

    if not os.path.exists(dest):
      compose = {
        'services': {}
      }

      if self.networks:
        compose['networks'] = self.networks

      super().write(compose, dest)

  def write(self):
    compose = {
      'services': self.services,
    }

    if self.networks:
      compose['networks'] = self.networks

    if self.volumes:
      compose['volumes'] = self.volumes

    super().write(compose)

  def __with_url_environment(self, environment):
    environment[SERVICE_HOSTNAME_ENV] = SERVICE_HOSTNAME

    if self.config.scheme:
      environment[SERVICE_SCHEME_ENV] = SERVICE_SCHEME

    if self.config.port:
      environment[SERVICE_PORT_ENV] = SERVICE_PORT
