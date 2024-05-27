import os

from .app_command import AppCommand
from .config import Config
from .constants import CONFIG_FILE

class ServiceCommand(AppCommand):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)

    self.__service_name = kwargs.get('service_name')

  @property
  def service_config(self):
    return Config(self.service_config_path).read()

  @property
  def service_config_path(self):
    return os.path.join(self.service_path, CONFIG_FILE)

  @property
  def service_name(self):
    return self.__service_name

  @property
  def service_exists(self):
    return os.path.exists(self.service_path)

  @property
  def service_path(self):
    return os.path.join(
      self.app_dir_path,
      self.service_relative_path
    )

  @property
  def service_relative_path(self):
    return os.path.join(
      self.namespace,
      self.service_name,
    )

  def config(self, _c: dict):
    _config = self.app_config
    _config.update(self.service_config)
    _config.update(_c)
    return _config