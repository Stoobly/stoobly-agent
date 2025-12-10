import os
import pdb

from .app import App
from .app_command import AppCommand
from .app_config import AppConfig
from .service_config import ServiceConfig


class ServiceCommand(AppCommand):

  def __init__(self, app: App, **kwargs):
    super().__init__(app)
    self.__service_name = kwargs.get('service_name')

    if kwargs.get('service_name'):
      self.__config = ServiceConfig(self.service_path, **kwargs)

  @property
  def service_config(self):
    if not self.service_name:
      raise Exception("Service name is required")

    return self.__config

  @service_config.setter
  def service_config(self, value):
    self.__config = value

  @property
  def service_config_path(self):
    return self.__config.path

  @property
  def service_name(self):
    return self.__service_name

  @service_name.setter
  def service_name(self, value):
    self.__service_name = value

  @property
  def service_exists(self):
    return os.path.exists(self.service_path)

  @property
  def service_path(self):
    return os.path.join(
      self.data_dir_path,
      self.service_relative_path
    )

  @property
  def service_relative_path(self):
    return os.path.join(
      self.scaffold_namespace,
      self.service_name,
    )

  @property
  def service_templates_root_dir(self):
    return os.path.join(self.templates_root_dir, 'build', 'services')

  def config(self, _c: dict):
    _config = self.app_config.read()
    _config.update(self.service_config.read())
    _config.update(_c)
    return _config

