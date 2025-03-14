# Wraps the .config.yml file in the service folder
import pdb

from .config import Config
from .constants import (
  SERVICE_DETACHED_ENV,
  SERVICE_HOSTNAME_ENV,
  SERVICE_PRIORITY_ENV,
  SERVICE_PORT_ENV,
  SERVICE_PROXY_MODE_ENV,
  SERVICE_SCHEME_ENV
)

class ServiceConfig(Config):

  def __init__(self, dir: str, **kwargs):
    super().__init__(dir)

    self.__detached = None
    self.__hostname = None
    self.__port = None
    self.__priority = None
    self.__proxy_mode = None
    self.__scheme = None

    self.load()

    if 'detached' in kwargs:
      self.__detached = bool(kwargs.get('detached'))
    
    if 'hostname' in kwargs:
      self.__hostname = kwargs.get('hostname')

    if 'port' in kwargs:
      self.__port = kwargs.get('port')

    if 'priority' in kwargs:
      self.__priority = kwargs.get('priority')

    if 'proxy_mode' in kwargs:
      self.__proxy_mode = kwargs.get('proxy_mode')

    if 'scheme' in kwargs:
      self.__scheme = kwargs.get('scheme')

  @property
  def detached(self) -> bool:
    return not not self.__detached

  @detached.setter
  def detached(self, v):
    self.__detached = v

  @property
  def hostname(self):
    return (self.__hostname or '').strip()

  @hostname.setter
  def hostname(self, v):
    self.__hostname = v

  @property
  def port(self):
    if not self.__port:
      if self.scheme == 'https':
        return '443' 
      elif self.scheme == 'http':
        return '80'

    return self.__port

  @port.setter
  def port(self, v):
    self.__port = v

  @property
  def priority(self):
    _priority = self.__priority
    _priority = float('inf') if _priority == None else float(_priority)

    if _priority == float('inf'):
      return _priority

    return float(_priority)

  @priority.setter
  def priority(self, v):
    self.__priority = v

  @property
  def proxy_mode(self) -> str:
    if self.__proxy_mode:
      return (self.__proxy_mode or '').strip()

    if not self.hostname:
      return ''

    _proxy_mode = f"reverse:{self.scheme}://{self.hostname}"

    if not self.port:
      return _proxy_mode

    if self.scheme == 'http' and self.port == '80': 
      return _proxy_mode

    if self.scheme == 'https' and self.port == '443':
      return _proxy_mode

    return f"{_proxy_mode}:{self.port}"

  @proxy_mode.setter
  def proxy_mode(self, v):
    self.__proxy_mode = v

  @property
  def scheme(self):
    return (self.__scheme or 'https').strip()

  @scheme.setter
  def scheme(self, v):
    self.__scheme = v

  def load(self, config = None):
    config = config or self.read()

    self.detached = config.get(SERVICE_DETACHED_ENV)
    self.hostname = config.get(SERVICE_HOSTNAME_ENV)
    self.port = config.get(SERVICE_PORT_ENV)
    self.priority = config.get(SERVICE_PRIORITY_ENV)
    self.proxy_mode = config.get(SERVICE_PROXY_MODE_ENV)
    self.scheme = config.get(SERVICE_SCHEME_ENV)

  def to_dict(self):
    return {
      'detached': self.detached,
      'hostname': self.hostname,
      'port': self.port,
      'priority': self.priority,
      'proxy_mode': self.proxy_mode,
      'scheme': self.scheme if self.hostname else '',
    }

  def write(self):
    config = {}

    if self.hostname:
      config[SERVICE_HOSTNAME_ENV] = self.hostname

    if self.port:
      config[SERVICE_PORT_ENV] = self.port

    if self.priority:
      config[SERVICE_PRIORITY_ENV] = self.priority

    if self.scheme:
      config[SERVICE_SCHEME_ENV] = self.scheme

    config[SERVICE_DETACHED_ENV] = bool(self.detached)

    config[SERVICE_PROXY_MODE_ENV] = self.proxy_mode

    super().write(config)