import os
import yaml

from .constants import CONFIG_FILE

class Config():

  def __init__(self, dir: str, file_name = None):
    self.__dir = dir
    self.__path = os.path.join(dir, file_name or CONFIG_FILE)

  @property
  def dir(self):
    return self.__dir

  @property
  def path(self):
    return self.__path

  def read(self, source: str = None):
    if not source:
      source = self.path

    config = {}

    if os.path.exists(source):
      with open(source, 'r') as fp:
        config = yaml.safe_load(fp)
        
    return config

  def write(self, config: dict):
    config_path = os.path.join(self.path)
    with open(config_path, 'w') as fp:
      yaml.dump(config, fp)