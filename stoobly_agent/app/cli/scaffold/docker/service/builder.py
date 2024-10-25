import os
import pdb

from ...app_config import AppConfig
from ...constants import SERVICE_HOSTNAME, SERVICE_HOSTNAME_ENV, SERVICE_PORT, SERVICE_PORT_ENV, SERVICE_SCHEME, SERVICE_SCHEME_ENV
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
    self.__service_name = os.path.basename(service_path)

    self.load()

  @property
  def app_base(self):
    return f"{self.service_name}.app_base"

  @property
  def init_base(self):
    return f"{self.service_name}.init_base"

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

    args = {}
    self.with_service(self.proxy_base, {
      'build': {
        'args': args,
      },
      'extends': {
        'file': os.path.relpath(self.app_builder.compose_file_path, self.dir_path),
        'service': self.app_builder.proxy_base
      }
    })

    args[SERVICE_HOSTNAME_ENV] = f"{SERVICE_HOSTNAME}"

  def build_init_base(self):
    environment = {}
    self.with_service(self.init_base, {
      'command': ['bin/.init', 'dist'],
      'environment': environment,
      'extends': {
        'file': os.path.relpath(self.app_builder.compose_file_path, self.dir_path),
        'service': self.app_builder.context_base
      }
    })

  def build_configure_base(self):
    environment = {}
    self.with_service(self.configure_base, {
      'command': ['bin/.configure'],
      'environment': environment,
      'extends': {
        'file': os.path.relpath(self.app_builder.compose_file_path, self.dir_path),
        'service': self.app_builder.context_base
      }
    })

  def write(self):
    self.build_init_base()
    self.build_configure_base()

    if self.config.hostname:
      self.build_proxy_base()

    super().write({
      'networks': self.networks,
      'services': self.services,
    })