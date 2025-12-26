# Wraps the .config.yml file in the service folder
import hashlib
import os
import pdb
import re

from .app_config import AppConfig
from .config import Config
from .constants import (
  SERVICE_DETACHED_ENV,
  SERVICE_HOSTNAME_ENV,
  SERVICE_ID_ENV,
  SERVICE_LOCAL_ENV,
  SERVICE_NAME_ENV,
  SERVICE_PRIORITY_ENV,
  SERVICE_PORT_ENV,
  SERVICE_SCHEME_ENV,
  SERVICE_UPSTREAM_HOSTNAME_ENV,
  SERVICE_UPSTREAM_PORT_ENV,
  SERVICE_UPSTREAM_SCHEME_ENV,
)

class ServiceConfig(Config):

  def __init__(self, dir: str, **kwargs):
    super().__init__(dir)

    self.__app_config = AppConfig(self.app_config_dir_path)
    self.__detached = None
    self.__hostname = None
    self.__local = None
    self.__name = None
    self.__port = None
    self.__priority = None
    self.__scheme = None
    self.__upstream_hostname = None
    self.__upstream_port = None
    self.__upstream_scheme = None

    self.load()

    if 'detached' in kwargs:
      self.__detached = bool(kwargs.get('detached'))
    
    if 'hostname' in kwargs:
      self.__hostname = kwargs.get('hostname')

    if 'local' in kwargs:
      self.__local = kwargs.get('local')

    if 'name' in kwargs:
      self.__name = kwargs.get('name')
    elif 'service_name' in kwargs:
      self.__name = kwargs.get('service_name')

    if 'port' in kwargs:
      self.__port = kwargs.get('port')

    if 'priority' in kwargs:
      self.__priority = kwargs.get('priority')

    if 'scheme' in kwargs:
      self.__scheme = kwargs.get('scheme')

    if 'upstream_hostname' in kwargs:
      self.__upstream_hostname = kwargs.get('upstream_hostname')

    if 'upstream_port' in kwargs:
      self.__upstream_port = kwargs.get('upstream_port')

    if 'upstream_scheme' in kwargs:
      self.__upstream_scheme = kwargs.get('upstream_scheme')

  @property
  def app_config(self):
    return self.__app_config

  @property
  def app_config_dir_path(self):
    return os.path.dirname(self.dir)

  @property
  def detached(self) -> bool:
    return not not self.__detached

  @detached.setter
  def detached(self, v):
    self.__detached = v

  @property
  def id(self):
    return hashlib.md5(self.url.encode()).hexdigest()

  @property
  def hostname(self):
    return (self.__hostname or '').strip()

  @hostname.setter
  def hostname(self, v):
    self.__hostname = v

  @property
  def local(self):
    return self.__local

  @local.setter
  def local(self, v: bool):
    self.__local = not not v

  @property
  def name(self):
    return self.__name

  @name.setter
  def name(self, v: str):
    if not v:
      return

    SERVICE_NAME_PATTERN = re.compile(r'^[a-z0-9]([a-z0-9._-]*[a-z0-9])?$')

    if not bool(SERVICE_NAME_PATTERN.fullmatch(v)):
      raise ValueError(f"{v} must match {SERVICE_NAME_PATTERN}")

    self.__name = v

  @property
  def port(self) -> int:
    if not self.__port:
      if self.__scheme == 'https':
        return 443
      elif self.__scheme == 'http':
        return 80

    return self.__port

  @port.setter
  def port(self, v: int):
    if v == None:
      self.__port = v
    else:
      v = int(v)
      if v > 0 and v <= 65535:
        if v == self.__upstream_port and self.local:
          raise ValueError('port cannot be the same as upstream port')
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
  def scheme(self):
    if not self.__scheme and self.__port:
      if self.port == 443:
        return 'https'
      else:
        return 'http'

    return (self.__scheme or 'https').strip()

  @scheme.setter
  def scheme(self, v):
    if v and not v in ['http', 'https']:
      raise ValueError('scheme must be http or https')
    self.__scheme = v

  @property
  def tls(self) -> bool:
    return self.__scheme == 'https'

  @property
  def upstream_hostname(self) -> str:
    if self.local:
      if self.app_config.runtime_docker:
        return 'host.docker.internal'
      return 'localhost'
    return self.__upstream_hostname or self.hostname

  @upstream_hostname.setter
  def upstream_hostname(self, v: str):
    self.__upstream_hostname = v

  @property
  def upstream_port(self) -> int:
    return self.__upstream_port or self.port

  @upstream_port.setter
  def upstream_port(self, v: int):
    if v == None:
      self.__upstream_port = v
    else:
      v = int(v)
      if v > 0 and v <= 65535:
        if v == self.__port and self.local:
          raise ValueError('upstream port cannot be the same as port')
        self.__upstream_port = v
      else:
        raise ValueError('upstream port must be between 0 and 65535')

  @property
  def upstream_scheme(self):
    return self.__upstream_scheme or self.scheme

  @upstream_scheme.setter
  def upstream_scheme(self, v): 
    self.__upstream_scheme = v

  @property
  def url(self):
    if not self.hostname:
      return ''

    _url = f"{self.scheme}://{self.hostname}"

    if not self.port:
      return _url

    if self.scheme == 'http' and self.port == 80: 
      return _url

    if self.scheme == 'https' and self.port == 443:
      return _url

    return f"{_url}:{self.port}"

  def load(self, config = None):
    config = config or self.read()

    self.detached = config.get(SERVICE_DETACHED_ENV)
    self.hostname = config.get(SERVICE_HOSTNAME_ENV)
    self.local = config.get(SERVICE_LOCAL_ENV)
    self.name = config.get(SERVICE_NAME_ENV)
    self.port = config.get(SERVICE_PORT_ENV)
    self.priority = config.get(SERVICE_PRIORITY_ENV)
    self.scheme = config.get(SERVICE_SCHEME_ENV)
    self.upstream_hostname = config.get(SERVICE_UPSTREAM_HOSTNAME_ENV)
    self.upstream_port = config.get(SERVICE_UPSTREAM_PORT_ENV)
    self.upstream_scheme = config.get(SERVICE_UPSTREAM_SCHEME_ENV)

  def to_dict(self):
    return {
      'detached': self.detached,
      'hostname': self.hostname,
      'local': self.local,
      'name': self.name,
      'port': self.port,
      'priority': self.priority,
      'scheme': self.scheme if self.hostname else '',
      'upstream_hostname': self.upstream_hostname,
      'upstream_port': self.upstream_port,
      'upstream_scheme': self.upstream_scheme,
    }

  def write(self):
    config = {}

    if self.hostname:
      config[SERVICE_HOSTNAME_ENV] = self.hostname

    if self.local:
      config[SERVICE_LOCAL_ENV] = True

    if self.name:
      config[SERVICE_NAME_ENV] = self.name

    if self.port:
      config[SERVICE_PORT_ENV] = self.port

    if self.priority:
      config[SERVICE_PRIORITY_ENV] = self.priority

    if self.scheme:
      config[SERVICE_SCHEME_ENV] = self.scheme

    if self.upstream_hostname:
      config[SERVICE_UPSTREAM_HOSTNAME_ENV] = self.upstream_hostname

    if self.upstream_port:
      config[SERVICE_UPSTREAM_PORT_ENV] = self.upstream_port

    if self.upstream_scheme:
      config[SERVICE_UPSTREAM_SCHEME_ENV] = self.upstream_scheme

    config[SERVICE_DETACHED_ENV] = bool(self.detached)
    config[SERVICE_ID_ENV] = self.id

    super().write(config)