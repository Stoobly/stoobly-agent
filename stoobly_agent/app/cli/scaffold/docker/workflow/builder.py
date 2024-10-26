import os
import pdb

from typing import List

from ...constants import (
  COMPOSE_TEMPLATE, SERVICE_HOSTNAME, SERVICE_HOSTNAME_ENV, SERVICE_NAME_ENV, SERVICE_PORT, SERVICE_PORT_ENV, SERVICE_SCHEME, 
  SERVICE_SCHEME_ENV, STOOBLY_HOME_DIR, WORKFLOW_NAME_ENV
)
from ..builder import Builder
from ..service.builder import ServiceBuilder
from ...templates.constants import SERVICE_HOSTNAME_BUILD_ARG

class WorkflowBuilder(Builder):

  def __init__(self, workflow_path: str, service_builder: ServiceBuilder):
    self._env = [SERVICE_NAME_ENV, WORKFLOW_NAME_ENV]
    self.__workflow_name = os.path.basename(workflow_path)
    super().__init__(workflow_path, COMPOSE_TEMPLATE.format(workflow=self.__workflow_name))

    self.__context = '../'
    self.__profiles = [self.__workflow_name]
    self.__workdir = os.path.join(STOOBLY_HOME_DIR, self.workflow_name)

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
    return os.path.relpath(self.service_builder.app_builder.context_docker_file_path, self.service_path)

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
    args = {}
    args[SERVICE_HOSTNAME_BUILD_ARG] = SERVICE_HOSTNAME

    return {
      'args': args,
      'context': self.context,
      'dockerfile': self.proxy_docker_file_path,
    }

  @property
  def proxy_docker_file_path(self):
    return os.path.relpath(self.service_builder.app_builder.proxy_docker_file_path, self.service_path)

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
    self.with_network(self.service_builder.service_name)
    
    if self.config.detached:
      self.with_volume(self.service_builder.service_name)

    # Services
    self.build_init()
    self.build_configure()

    if self.config.hostname:
      self.with_public_network()
      self.build_proxy() # Depends on configure, must call build_configure first

  def build_init(self):
    environment = { **self.env_dict() }
    volumes = []

    service = {
      'build': self.context_build,
      'environment': environment,
      'extends': self.service_builder.build_extends_init_base(self.dir_path),
      'profiles': self.profiles,
      'volumes': volumes,
      'working_dir': self.__workdir,
    }

    if self.config.hostname:
      self.__with_url_environment(environment)

    if self.config.detached:
      volumes.append(f"{self.service_builder.service_name}:{STOOBLY_HOME_DIR}/.stoobly")

    self.with_service(self.init, service)

  def build_configure(self):
    # If the configure_base service does not exist, we can't extend from it, return
    if not self.service_builder.configure_base_service:
      return

    depends_on = {}
    environment = { **self.env_dict() }
    volumes = []

    service = {
      'build': self.context_build,
      'depends_on': depends_on,
      'environment': environment,
      'extends': self.service_builder.build_extends_configure_base(self.dir_path),
      'profiles': self.profiles,
      'volumes': volumes,
      'working_dir': self.__workdir,
    }

    if self.config.hostname:
      self.__with_url_environment(environment)

    if self.init in self.services:
      depends_on[self.init] = {
        'condition': 'service_completed_successfully',
      }

    if self.config.detached:
      volumes.append(f"{self.service_builder.service_name}:{STOOBLY_HOME_DIR}/.stoobly")

    self.with_service(self.configure, service)

  def build_proxy(self):
    # If the proxy_base service does not exist, we can't extend from it, return
    if not self.service_builder.proxy_base_service:
      return

    depends_on = {}
    environment = { **self.env_dict() }
    extra_hosts = []
    networks = [self.service_builder.service_name]
    volumes = []

    service = {
      'build': self.proxy_build, 
      'depends_on': depends_on,
      'environment': environment,
      'extra_hosts': extra_hosts,
      'extends': self.service_builder.build_extends_proxy_base(self.dir_path),
      'networks': networks,
      'profiles': self.profiles,
      'volumes': volumes,
      'working_dir': self.__workdir,
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

      # Expose this container service to the public network 
      # so that it is accessible to other Stoobly services
      networks.append(self.public_network_name)

    if self.config.detached:
      volumes.append(f"{self.service_builder.service_name}:{STOOBLY_HOME_DIR}/.stoobly")

    self.with_service(self.proxy, service)

  def env_dict(self):
    env = {}
    for e in self._env:
      env[e] = '${' + e + '}'
    return env

  def initialize_custom_file(self):
    dest = self.custom_compose_file_path

    if not os.path.exists(dest):
      super().write({
        'networks': self.networks,
        'services': {}
      }, dest)

  def with_env(self, v: List[str]): 
    if not isinstance(v, list):
      return self
    self._env += v
    return self

  def write(self):
    super().write({
      'networks': self.networks,
      'services': self.services,
      'volumes': self.volumes,
    })

  def __with_url_environment(self, environment):
    environment[SERVICE_HOSTNAME_ENV] = SERVICE_HOSTNAME

    if self.config.scheme:
      environment[SERVICE_SCHEME_ENV] = SERVICE_SCHEME

    if self.config.port:
      environment[SERVICE_PORT_ENV] = SERVICE_PORT
