import os
import pdb

from .app_command import AppCommand
from .service_config import ServiceConfig

class ServiceCommand(AppCommand):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.__service_name = kwargs.get('service_name')

    self.__config = ServiceConfig(self.service_path)
    if kwargs.get('detached') != None:
      self.__config.detached = kwargs.get('detached')
    
    if kwargs.get('hostname') != None:
      self.__config.hostname = kwargs.get('hostname')

    if kwargs.get('port') != None:
      self.__config.port = kwargs.get('port')

    if kwargs.get('priority') != None:
      self.__config.priority = kwargs.get('priority')

    if kwargs.get('proxy_mode') != None:
      self.__config.proxy_mode = kwargs.get('proxy_mode')

    if kwargs.get('scheme') != None:
      self.__config.scheme = kwargs.get('scheme')

  @property
  def service_config(self):
    return self.__config

  @property
  def service_config_path(self):
    return self.__config.path

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
    _config = self.app_config.read()
    _config.update(self.service_config.read())
    _config.update(_c)
    return _config