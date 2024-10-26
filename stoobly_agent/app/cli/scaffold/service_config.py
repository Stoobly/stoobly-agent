# Wraps the .config.yml file in the service folder

import dns.resolver
import pdb
import subprocess
import re

from .config import Config
from .constants import (
  SERVICE_DETACHED_ENV,
  SERVICE_DOCKER_COMPOSE_PATH_ENV,
  SERVICE_HOSTNAME_ENV,
  SERVICE_DNS_ENV,
  SERVICE_PRIORITY_ENV,
  SERVICE_PORT_ENV,
  SERVICE_PROXY_MODE_ENV,
  SERVICE_SCHEME_ENV
)

class ServiceConfig(Config):

  def __init__(self, dir: str, **kwargs):
    super().__init__(dir)

    self.__detached = None
    self.__docker_compose_path = None
    self.__hostname = None
    self.__dns = None
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
  def detached(self):
    return self.__detached

  @detached.setter
  def detached(self, v):
    self.__detached = v

  @property
  def docker_compose_path(self):
    return self.__docker_compose_path

  @docker_compose_path.setter
  def docker_compose_path(self, v):
    self.__docker_compose_path = v

  @property
  def hostname(self):
    return self.__hostname

  @hostname.setter
  def hostname(self, v):
    self.__hostname = v

  @property
  def dns(self):
    # If hostname is set then the service is external and we will need to configure the container's DNS.
    # If we don't configure the container's DNS, then Docker's embedded DNS will potentially
    # use configuration from the host's /etc/hosts file. The user may have configured their
    # /etc/hosts file to resolve requests to localhost
    #
    # See: 
    # https://forums.docker.com/t/docker-127-0-0-11-resolver-should-use-host-etc-hosts-file/55157
    # https://docs.docker.com/network/#dns-services
    # 
    # TODO: ideally we want to know if the service is built locally, if so, then no need to set DNS
    # since Docker's embedded DNS will resolve to it
    if self.hostname and not self.__dns:
      nameservers = self.__find_dns()
      self.__dns = nameservers[0] if nameservers else None
    return self.__dns

  @dns.setter
  def dns(self, v):
    self.__dns = v

  @property
  def port(self):
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
  def proxy_mode(self):
    if self.__proxy_mode:
      return self.__proxy_mode

    return f"reverse:{self.scheme}://{self.hostname}"

  @proxy_mode.setter
  def proxy_mode(self, v):
    self.__proxy_mode = v

  @property
  def scheme(self):
    return self.__scheme or 'https'

  @scheme.setter
  def scheme(self, v):
    self.__scheme = v

  def load(self, config = None):
    config = config or self.read()

    # Do not load dns from config, have it dynamically determined
    #self.dns = config.get(SERVICE_DNS_ENV)

    self.detached = config.get(SERVICE_DETACHED_ENV)
    self.docker_compose_path = config.get(SERVICE_DOCKER_COMPOSE_PATH_ENV)
    self.hostname = config.get(SERVICE_HOSTNAME_ENV)
    self.port = config.get(SERVICE_PORT_ENV)
    self.priority = config.get(SERVICE_PRIORITY_ENV)
    self.proxy_mode = config.get(SERVICE_PROXY_MODE_ENV)
    self.scheme = config.get(SERVICE_SCHEME_ENV)

  def write(self):
    config = {}

    if self.docker_compose_path:
      config[SERVICE_DOCKER_COMPOSE_PATH_ENV] = self.docker_compose_path

    if self.hostname:
      config[SERVICE_HOSTNAME_ENV] = self.hostname

    if self.dns:
      config[SERVICE_DNS_ENV] = self.dns
    
    if self.port:
      config[SERVICE_PORT_ENV] = self.port

    if self.priority:
      config[SERVICE_PRIORITY_ENV] = self.priority

    if self.scheme:
      config[SERVICE_SCHEME_ENV] = self.scheme

    config[SERVICE_DETACHED_ENV] = bool(self.detached)

    config[SERVICE_PROXY_MODE_ENV] = self.proxy_mode

    super().write(config)

  def __find_dns(self):
    dns_resolver = dns.resolver.Resolver()
    nameservers = dns_resolver.nameservers

    # If systemd-resolved is not used
    if nameservers != ['127.0.0.53']:
      return nameservers

    # Run the `resolvectl status` command and capture its output
    result = subprocess.run(['resolvectl', 'status'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Check if the command ran successfully
    if result.returncode != 0:
      return []

    # Extract the DNS servers using a regular expression
    #dns_servers = re.findall(r'DNS Servers: ([\d.]+(?:, [\d.]+)*)', result.stdout)
    pattern = re.compile('DNS Servers:(.*?)DNS Domain', re.DOTALL)
    match = re.findall(pattern, result.stdout)

    if not match:
      return []
      
    # Split the DNS servers string into a list
    dns_servers = match[0].strip().split("\n")
    return list(map(lambda dns_server: dns_server.strip(), dns_servers))