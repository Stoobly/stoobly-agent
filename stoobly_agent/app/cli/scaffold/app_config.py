from .config import Config
from .constants import APP_NAME_ENV, APP_NETWORK_ENV, APP_UI_PORT_ENV

class AppConfig(Config):

  def __init__(self, dir: str):
    super().__init__(dir)

    self.__name = None
    self.__network = None

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
  def ui_port(self):
    return self.__ui_port

  @ui_port.setter
  def ui_port(self, v):
    self.__ui_port = v

  def load(self, config = None):
    config = config or self.read()

    self.name = config.get(APP_NAME_ENV)
    self.network = config.get(APP_NETWORK_ENV)
    self.ui_port = config.get(APP_UI_PORT_ENV)
    
  def write(self):
    config = {}

    if self.name:
      config[APP_NAME_ENV] = self.name

    if self.network:
      config[APP_NETWORK_ENV] = self.network

    if self.ui_port:
      config[APP_UI_PORT_ENV] = self.ui_port

    super().write(config)