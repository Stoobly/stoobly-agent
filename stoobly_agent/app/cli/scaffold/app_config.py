from .config import Config
from .constants import APP_NETWORK_ENV

class AppConfig(Config):

  def __init__(self, dir: str):
    super().__init__(dir)

    self.__network = None

    self.load()

  @property
  def network(self):
    return self.__network

  @network.setter
  def network(self, v):
    self.__network = v

  def load(self, config = None):
    config = config or self.read()

    self.__network = config.get(APP_NETWORK_ENV)
    
  def write(self):
    config = {}

    if self.network:
      config[APP_NETWORK_ENV] = self.network

    super().write(config)