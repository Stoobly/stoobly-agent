# Wraps the .config.yml file in the workflow folder
import pdb

from .config import Config
from .constants import WORKFLOW_TEMPLATE_ENV

class WorkflowConfig(Config):

  def __init__(self, dir: str, **kwargs):
    super().__init__(dir)

    self.__template = None

    self.load()

    if 'template' in kwargs:
      self.__template = kwargs.get('template')

  @property
  def empty(self):
    return not self.template

  @property
  def template(self):
    return (self.__template or '').strip()

  @template.setter
  def template(self, v):
    self.__template = v

  def load(self, config = None):
    config = config or self.read()

    self.template = config.get(WORKFLOW_TEMPLATE_ENV)

  def to_dict(self):
    return {
      'template': self.template,
    }

  def write(self):
    config = {}

    if self.template:
      config[WORKFLOW_TEMPLATE_ENV] = self.template

    super().write(config)