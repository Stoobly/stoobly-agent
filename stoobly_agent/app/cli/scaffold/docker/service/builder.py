import os
import pdb

from typing import List

from stoobly_agent.config.data_dir import DATA_DIR_NAME

from ...app_config import AppConfig
from ...constants import (
  APP_DIR, DOCKER_NAMESPACE, SERVICE_NAME, SERVICE_NAME_ENV, 
  SERVICE_HOSTNAME, SERVICE_HOSTNAME_ENV, SERVICE_NAME_ENV, SERVICE_PORT, SERVICE_PORT_ENV, SERVICE_SCHEME, SERVICE_SCHEME_ENV, 
  STOOBLY_HOME_DIR, STOOBLY_HOME_DIR, 
  WORKFLOW_NAME, WORKFLOW_NAME_ENV, WORKFLOW_SCRIPTS, WORKFLOW_TEMPLATE
)
from ...service_config import ServiceConfig
from ..app_builder import AppBuilder
from ..builder import Builder
from ..constants import DOCKER_COMPOSE_BASE

class ServiceBuilder(Builder):

  def __init__(self, config: ServiceConfig, app_builder: AppBuilder = None):
    service_path = config.dir
    super().__init__(service_path, DOCKER_COMPOSE_BASE)

    if not app_builder:
      app_dir = os.path.dirname(service_path)
      app_builder = AppBuilder(AppConfig(app_dir))
    self.app_builder = app_builder

    self.__config = config
    self.__env = [SERVICE_NAME_ENV, WORKFLOW_NAME_ENV]
    self.__service_name = os.path.basename(service_path)
    self.__working_dir = os.path.join(
      STOOBLY_HOME_DIR, DATA_DIR_NAME, DOCKER_NAMESPACE, SERVICE_NAME, WORKFLOW_NAME
    )

  @property
  def app_base(self):
    return f"{self.service_name}.app_base"

  @property
  def config(self):
    return self.__config

  @property
  def configure_base(self):
    return f"{self.service_name}.configure_base"

  @property
  def configure_base_service(self):
    return self.services.get(self.configure_base)

  @property
  def extends_service(self):
    if self.config.detached:
      return self.app_builder.stoobly_base
    else:
      return self.app_builder.context_base

  @property
  def init_base(self):
    return f"{self.service_name}.init_base"

  @property
  def init_base_service(self):
    return self.services.get(self.init_base)

  @property
  def proxy_base(self):
    return f"{self.service_name}.proxy_base"

  @property
  def proxy_base_service(self):
    return self.services.get(self.proxy_base)

  @property
  def service_name(self):
    return self.__service_name

  def build_extends_init_base(self, source_dir: str):
    return self.build_extends(self.init_base, source_dir)

  def build_extends_configure_base(self, source_dir: str):
    return self.build_extends(self.configure_base, source_dir)

  def build_extends_proxy_base(self, source_dir: str):
    return self.build_extends(self.proxy_base, source_dir)

  def build_proxy_base(self):
    if not self.config.hostname:
      return

    service_id = self.config.id
    environment = { **self.env_dict() }
    labels = [
      'traefik.enable=true',
      f"traefik.http.routers.{service_id}.rule=Host(`{SERVICE_HOSTNAME}`)",
      f"traefik.http.routers.{service_id}.entrypoints={SERVICE_PORT}",
      f"traefik.http.services.{service_id}.loadbalancer.server.port={SERVICE_PORT}"
    ]
    volumes = []

    if self.config.detached:
      self.__with_detached_volumes(volumes)

    if self.config.tls:
      labels.append(f"traefik.http.routers.{service_id}.tls=true")

    base = {
      'environment': environment,
      'extends': {
        'file': os.path.relpath(self.app_builder.compose_file_path, self.dir_path),
        'service': self.extends_service
      },
      'labels': labels,
      'working_dir': self.__working_dir,
    }

    if len(volumes):
      base['volumes'] = volumes

    self.with_service(self.proxy_base, base)

  def build_init_base(self):
    environment = { **self.env_dict() }
    volumes = [f"{APP_DIR}:/app"]

    if self.config.hostname:
      self.__with_url_environment(environment)

    if self.config.detached:
      self.__with_detached_volumes(volumes)

    self.with_service(self.init_base, {
      'command': [f"{WORKFLOW_SCRIPTS}/{WORKFLOW_TEMPLATE}/.init", 'bin/init'],
      'environment': environment,
      'extends': {
        'file': os.path.relpath(self.app_builder.compose_file_path, self.dir_path),
        'service': self.extends_service
      },
      'volumes': volumes,
      'working_dir': self.__working_dir,
    })

  def build_configure_base(self):
    environment = { **self.env_dict() }
    volumes = []

    if self.config.hostname:
      self.__with_url_environment(environment)

    if self.config.detached:
      self.__with_detached_volumes(volumes)

    base = {
      'command': [f"{WORKFLOW_SCRIPTS}/{WORKFLOW_TEMPLATE}/.configure", 'bin/configure'],
      'environment': environment,
      'extends': {
        'file': os.path.relpath(self.app_builder.compose_file_path, self.dir_path),
        'service': self.extends_service
      },
      'working_dir': self.__working_dir,
    }

    if len(volumes):
      base['volumes'] = volumes

    self.with_service(self.configure_base, base)

  def env_dict(self):
    env = {}
    for e in self.__env:
      env[e] = '${' + e + '}'
    return env

  def with_env(self, v: List[str]): 
    if not isinstance(v, list):
      return self
    self.__env += v
    return self

  def write(self):
    self.build_init_base()
    self.build_configure_base()

    if self.config.hostname:
      self.build_proxy_base()

    compose = {
      'services': self.services,
    }

    if self.networks:
      compose['networks'] = self.networks

    super().write(compose)

  def __with_detached_volumes(self, volumes: list):
    # Mount named volume
    volumes.append(f"{self.service_name}:{STOOBLY_HOME_DIR}/{DATA_DIR_NAME}")

    # Mount docker folder
    volumes.append(f"../:{STOOBLY_HOME_DIR}/{DATA_DIR_NAME}/{DOCKER_NAMESPACE}")

  def __with_url_environment(self, environment):
    environment[SERVICE_HOSTNAME_ENV] = SERVICE_HOSTNAME

    if self.config.scheme:
      environment[SERVICE_SCHEME_ENV] = SERVICE_SCHEME

    if self.config.port:
      environment[SERVICE_PORT_ENV] = SERVICE_PORT