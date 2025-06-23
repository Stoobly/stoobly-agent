import os

from .config import Config
from .constants import APP_NAME_ENV, APP_NETWORK_ENV, APP_PLUGINS_DELMITTER, APP_PLUGINS_ENV

class AppConfig(Config):

  def __init__(self, dir: str):
    super().__init__(dir)

    self.__name = None
    self.__network = None
    self.__plugins = None

    self.load()

  @property
  def name(self):
    return self.__name

  @name.setter
  def name(self, v):
    self.__name = v

  @property
  def network(self):
    return self.__network

  @network.setter
  def network(self, v):
    self.__network = v

  @property
  def plugins(self):
    return self.__plugins or []

  @plugins.setter
  def plugins(self, v: list):
    self.__plugins = v

  def load(self, config = None):
    config = config or self.read()

    self.name = config.get(APP_NAME_ENV)
    self.network = config.get(APP_NETWORK_ENV)

    if config.get(APP_PLUGINS_ENV):
      plugins: str = config.get(APP_PLUGINS_ENV)
      self.plugins = plugins.split(APP_PLUGINS_DELMITTER)
    
  def write(self):
    config = {}

    if self.name:
      config[APP_NAME_ENV] = self.name

    if self.network:
      config[APP_NETWORK_ENV] = self.network

    if self.plugins:
      config[APP_PLUGINS_ENV] = APP_PLUGINS_DELMITTER.join(self.plugins)

    super().write(config)