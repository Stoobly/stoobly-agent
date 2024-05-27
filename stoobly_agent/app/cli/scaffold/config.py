import os
import yaml

class Config():

  def __init__(self, path: str):
    self.__path = path

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