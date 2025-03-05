import os

from .builder import Builder
from .constants import DOCKER_COMPOSE_BASE, DOCKERFILE_CONTEXT
from ..app_config import AppConfig

class AppBuilder(Builder):

  def __init__(self, config: AppConfig):
    super().__init__(config.dir, DOCKER_COMPOSE_BASE)

  @property
  def context_base(self):
    return 'context_base'

  @property
  def context_docker_file_path(self):
    return os.path.join(self.dir_path, DOCKERFILE_CONTEXT)

  @property
  def stoobly_base(self):
    return 'stoobly_base'