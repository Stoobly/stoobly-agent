import os

from stoobly_agent.app.cli.scaffold.templates.constants import CORE_GATEWAY_SERVICE_NAME, SERVICE_EXTENSION

from .config import Config
from .constants import (
  APP_COPY_ON_WORKFLOW_UP_ENV, APP_DOCKER_SOCKET_PATH_ENV, APP_NAME_ENV, APP_PLUGINS_DELMITTER, APP_PLUGINS_ENV, APP_PROXY_MODE_ENV, APP_PROXY_PORT_ENV, APP_RUNTIME_ENV, APP_UI_PORT_ENV, APP_VERSION_ENV, RUNTIME_DOCKER, RUNTIME_LOCAL
)

class AppConfig(Config):

  def __init__(self, dir: str):
    super().__init__(dir)

    self.__proxy_hostname = None
    self.__copy_on_workflow_up = False
    self.__docker_socket_path = '/var/run/docker.sock'
    self.__name = None
    self.__plugins = None
    self.__proxy_mode = None
    self.__proxy_port = None
    self.__runtime = None
    self.__ui_port = None

    self.load()

  @property
  def copy_on_workflow_up(self):
    return self.__copy_on_workflow_up

  @copy_on_workflow_up.setter
  def copy_on_workflow_up(self, v):
    self.__copy_on_workflow_up = v

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
  def plugins(self):
    return self.__plugins or []

  @plugins.setter
  def plugins(self, v: list):
    self.__plugins = v

  @property
  def runtime(self):
    return self.__runtime or RUNTIME_LOCAL

  @runtime.setter
  def runtime(self, v: str):
    self.__runtime = v

  @property
  def runtime_local(self):
    return self.runtime == RUNTIME_LOCAL

  @property
  def runtime_docker(self):
    return self.runtime == RUNTIME_DOCKER

  @property
  def proxy_hostname(self):
    if self.__proxy_hostname:
      return self.__proxy_hostname 

    if self.runtime_docker:
      return f"{CORE_GATEWAY_SERVICE_NAME}{SERVICE_EXTENSION}"

    return 'localhost'

  @proxy_hostname.setter
  def proxy_hostname(self, v):
    self.__proxy_hostname = v

  @property
  def proxy_mode(self):
    return self.__proxy_mode or 'regular'

  @proxy_mode.setter
  def proxy_mode(self, v):
    self.__proxy_mode = v

  @property
  def proxy_port(self):
    return self.__proxy_port or 8080

  @proxy_port.setter
  def proxy_port(self, v):
    self.__proxy_port = v

  @property
  def ui_port(self):
    return self.__ui_port or 4200

  @ui_port.setter
  def ui_port(self, v):
    self.__ui_port = v

  @property
  def version(self):
    return self.__version or None

  @version.setter
  def version(self, v):
    self.__version = v

  def load(self, config = None):
    config = config or self.read()

    self.copy_on_workflow_up = config.get(APP_COPY_ON_WORKFLOW_UP_ENV, False)
    self.name = config.get(APP_NAME_ENV)
    self.proxy_mode = config.get(APP_PROXY_MODE_ENV)
    self.proxy_port = config.get(APP_PROXY_PORT_ENV)
    self.ui_port = config.get(APP_UI_PORT_ENV)
    self.version = config.get(APP_VERSION_ENV)

    if config.get(APP_PLUGINS_ENV):
      plugins: str = config.get(APP_PLUGINS_ENV)
      self.plugins = plugins.split(APP_PLUGINS_DELMITTER)

    if config.get(APP_RUNTIME_ENV):
      self.runtime = config.get(APP_RUNTIME_ENV)

  def write(self):
    config = {}

    config[APP_COPY_ON_WORKFLOW_UP_ENV] = self.copy_on_workflow_up

    if self.docker_socket_path:
      config[APP_DOCKER_SOCKET_PATH_ENV] = self.docker_socket_path

    if self.name:
      config[APP_NAME_ENV] = self.name

    if self.plugins:
      config[APP_PLUGINS_ENV] = APP_PLUGINS_DELMITTER.join(self.plugins)

    if self.runtime:
      config[APP_RUNTIME_ENV] = self.runtime

    if self.proxy_mode:
      config[APP_PROXY_MODE_ENV] = self.proxy_mode

    if self.proxy_port:
      config[APP_PROXY_PORT_ENV] = self.proxy_port

    if self.ui_port:
      config[APP_UI_PORT_ENV] = self.ui_port
    
    if self.version:
      config[APP_VERSION_ENV] = self.version

    super().write(config)
