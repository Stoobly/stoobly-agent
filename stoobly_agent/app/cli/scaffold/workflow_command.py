import os
import pdb
import yaml

from stoobly_agent.lib.logger import Logger

from .config import Config
from .constants import BUILD_FOLDER_NAME, COMPOSE_TEMPLATE, CONFIG_FILE, DIST_FOLDER_NAME, DOCKER_COMPOSE_CUSTOM, ENV_FILE
from .service_command import ServiceCommand

LOG_ID = 'WorkflowCommand'

class WorkflowCommand(ServiceCommand):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)

    self.__workflow_name = kwargs['workflow_name']

  @property
  def dist_dir_path(self):
    return os.path.join(self.workflow_path, DIST_FOLDER_NAME)

  @property
  def build_dir_path(self):
    return os.path.join(self.workflow_path, BUILD_FOLDER_NAME)

  @property
  def compose_path(self):
    return os.path.join(
      self.app_dir_path,
      self.compose_relative_path
    )

  @property
  def compose_relative_path(self):
    return os.path.join(
      self.workflow_relative_path, 
      COMPOSE_TEMPLATE.format(workflow=self.workflow_name)
    )

  @property
  def containers(self):
    _containers = []
    if not os.path.exists(self.compose_path):
      return []

    with open(self.compose_path, 'r') as fp:
      config = yaml.safe_load(fp)
      services = config.get('services')
      if not isinstance(services, dict):
        return []

      for service in services:
        _containers.append(f"{self.workflow_name}-{service}-1")
        
    return _containers

  @property
  def custom_compose(self):
    if os.path.exists(self.custom_compose_path):
      with open(self.custom_compose_path, 'r') as fp:
        compose = yaml.safe_load(fp)
        if compose and not isinstance(compose, dict):
          Logger.instance(LOG_ID).warn(f"Could not parse {self.custom_compose_path} as YAML")
          return {}
        return compose

  @property
  def custom_compose_relative_path(self):
    return os.path.join(
      self.workflow_relative_path,
      DOCKER_COMPOSE_CUSTOM
    )

  @property
  def custom_compose_path(self):
    return os.path.join(
      self.app_dir_path,
      self.custom_compose_relative_path
    )

  @property
  def custom_services(self):
    custom_compose = self.custom_compose

    if not custom_compose:
      return []
    
    services = custom_compose.get('services')
    if not isinstance(services, list):
      return []

    return services

  @property
  def workflow_config(self):
    return Config(self.workflow_config_path).read()

  @property
  def workflow_config_path(self):
    return os.path.join(self.workflow_path, CONFIG_FILE)

  @property
  def workflow_env_path(self):
    return os.path.join(self.workflow_path, ENV_FILE)

  @property
  def workflow_exists(self):
    return os.path.exists(self.workflow_path)

  @property
  def workflow_name(self):
    return self.__workflow_name

  @property
  def workflow_path(self):
    return os.path.join(
      self.app_dir_path,
      self.workflow_relative_path
    )

  @property
  def workflow_relative_path(self):
    return os.path.join(
      self.service_relative_path,
      self.workflow_name
    )
  
  def env(self, _c: dict):
    _config = self.app_config.read()
    _config.update(self.service_config)
    _config.update(self.workflow_config)
    _config.update(_c)
    return _config
