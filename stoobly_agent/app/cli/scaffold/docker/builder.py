import os
import pathlib
import pdb
import yaml

from .constants import APP_EGRESS_NETWORK, APP_EGRESS_NETWORK_NAME, APP_INGRESS_NETWORK, APP_INGRESS_NETWORK_NAME, DOCKER_COMPOSE_CUSTOM 

class Builder():

  def __init__(self, dir_path: str, compose_file_name: str):
    self.__compose_file_name = compose_file_name
    self.__dir_path = dir_path
    self.__networks = {}
    self.__services = {}
    self.__templates_dir = os.path.join(pathlib.Path(__file__).parent.parent.resolve(), 'templates')
    self.__volumes = {}

  @property
  def compose_file_name(self):
    return self.__compose_file_name

  @property
  def compose_file_path(self):
    return os.path.join(self.dir_path, self.compose_file_name)

  @property
  def custom_compose_file_path(self):
    return os.path.join(
      self.dir_path,
      DOCKER_COMPOSE_CUSTOM
    )

  @property
  def dir_path(self):
    return self.__dir_path

  @property
  def egress_network(self):
    return self.__networks.get(APP_EGRESS_NETWORK_NAME)

  @property
  def egress_network_name(self):
    return APP_EGRESS_NETWORK_NAME

  @property
  def networks(self):
    return self.__networks

  @property
  def services(self):
    return self.__services

  @property
  def templates_dir(self):
    return self.__templates_dir

  @property
  def volumes(self):
    return self.__volumes

  def build_extends(self, service_name: str, source_dir: str):
    return {
      'file': os.path.relpath(self.compose_file_path, source_dir),
      'service': service_name
    }

  # If the file already exists, load the specified resources
  def load(self):
    if not os.path.exists(self.compose_file_path):
      return

    with open(self.compose_file_path, 'r') as fp:
      contents = yaml.safe_load(fp) or {}

      networks = contents.get('networks')
      if isinstance(networks, dict):
        self.__networks = networks

      services = contents.get('services')
      if isinstance(services, dict):
        self.__services = services

      volumes = contents.get('volumes')
      if isinstance(volumes, dict):
        self.__volumes = volumes

  def with_network(self, network):
    self.__networks[network] = {
      'name': f"{APP_EGRESS_NETWORK}.{network}"
    }
    return self

  def with_egress_network(self, network = APP_EGRESS_NETWORK):
    self.__networks[APP_EGRESS_NETWORK_NAME] = {
      'external': True,
      'name': network,
    }
    return self

  def with_ingress_network(self, network = APP_INGRESS_NETWORK):
    self.__networks[APP_INGRESS_NETWORK_NAME] = {
      'external': True,
      'name': network,
    }
    return self

  def with_service(self, service_name: str, service: dict):
    self.__services[service_name] = service
    return self

  def with_volume(self, volume_name: str, volume: dict = {}):
    self.__volumes[volume_name] = volume
    return self

  def write(self, compose: dict, path = None):
    path = path or self.compose_file_path
    parent_dir = os.path.dirname(path)

    if not os.path.exists(parent_dir):
      os.makedirs(parent_dir)

    with open(path, 'w') as fp:
      yaml.dump(compose, fp, allow_unicode=True)
      fp.close()