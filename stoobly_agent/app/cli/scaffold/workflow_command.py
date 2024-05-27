import os

from .config import Config
from .constants import COMPOSE_TEMPLATE, CONFIG_FILE, ENV_FILE
from .service_command import ServiceCommand

class WorkflowCommand(ServiceCommand):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)

    self.__workflow_name = kwargs['workflow_name']

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
  
  def config(self, _c: dict):
    _config = self.app_config
    _config.update(self.service_config)
    _config.update(self.workflow_config)
    _config.update(_c)
    return _config
