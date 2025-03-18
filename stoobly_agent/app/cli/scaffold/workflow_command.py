import os
import pdb
import yaml

from stoobly_agent.lib.logger import Logger

from .app import App
from .config import Config
from .constants import BIN_FOLDER_NAME, COMPOSE_TEMPLATE, CONFIG_FILE, ENV_FILE, PUBLIC_FOLDER_NAME
from .docker.constants import DOCKER_COMPOSE_CUSTOM
from .service_command import ServiceCommand

LOG_ID = 'WorkflowCommand'

class WorkflowCommand(ServiceCommand):

  def __init__(self, app: App, **kwargs):
    super().__init__(app, **kwargs)

    self.__workflow_name = kwargs['workflow_name']

  @property
  def bin_dir_path(self):
    return os.path.join(self.workflow_path, BIN_FOLDER_NAME)

  @property
  def compose_path(self):
    return os.path.join(
      self.data_dir_path,
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
    if not os.path.exists(self.compose_path):
      return []

    with open(self.compose_path, 'r') as fp:
      config = yaml.safe_load(fp)
      services = config.get('services')
      if not isinstance(services, dict):
        return []

      return services
        
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
      self.data_dir_path,
      self.custom_compose_relative_path
    )

  @property
  def custom_services(self):
    custom_compose = self.custom_compose

    if not custom_compose:
      return {}
    
    services = custom_compose.get('services')
    if not isinstance(services, dict):
      return {}

    return services

  @property
  def public_dir_path(self):
    return os.path.join(self.workflow_path, PUBLIC_FOLDER_NAME)

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
      self.data_dir_path,
      self.workflow_relative_path
    )

  @property
  def workflow_relative_path(self):
    return os.path.join(
      self.service_relative_path,
      self.workflow_name
    )

  @property
  def workflow_templates_root_dir(self):
    return os.path.join(self.templates_root_dir, 'workflow')
  
  def env(self, _c: dict):
    _config = self.app_config.read()
    _config.update(self.service_config)
    _config.update(self.workflow_config)
    _config.update(_c)
    return _config
