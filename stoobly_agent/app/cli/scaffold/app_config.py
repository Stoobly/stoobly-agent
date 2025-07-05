from .config import Config
from .constants import APP_DOCKER_SOCKET_PATH_ENV, APP_NAME_ENV, APP_UI_PORT_ENV

class AppConfig(Config):

  def __init__(self, dir: str):
    super().__init__(dir)

    self.__docker_socket_path = '/var/run/docker.sock'
    self.__name = None
    self.__ui_port = None

    self.load()

  @property
  def docker_socket_path(self):
    return self.__docker_socket_path

  @docker_socket_path.setter
  def docker_socket_path(self, v):
    self.__docker_socket_path = v

  @property
  def name(self):
    return self.__name

  @name.setter
  def name(self, v):
    self.__name = v

  @property
  def ui_port(self):
    return self.__ui_port

  @ui_port.setter
  def ui_port(self, v):
    self.__ui_port = v

  def load(self, config = None):
    config = config or self.read()

    self.name = config.get(APP_NAME_ENV)
    self.ui_port = config.get(APP_UI_PORT_ENV)
    
  def write(self):
    config = {}

    if self.docker_socket_path:
      config[APP_DOCKER_SOCKET_PATH_ENV] = self.docker_socket_path

    if self.name:
      config[APP_NAME_ENV] = self.name

    if self.ui_port:
      config[APP_UI_PORT_ENV] = self.ui_port

    super().write(config)