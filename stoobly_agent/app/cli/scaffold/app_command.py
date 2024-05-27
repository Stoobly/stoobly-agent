import os

from .command import Command
from .config import Config
from .constants import CONFIG_FILE

class AppCommand(Command):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)

    if not kwargs['app_dir_path']:
        kwargs['app_dir_path'] = os.getcwd()

    self.__app_dir_path = kwargs.get('app_dir_path')

  @property
  def app_dir_path(self):
    return self.__app_dir_path

  @property
  def app_config(self):
    return Config(self.app_config_path).read()

  @property
  def app_config_path(self):
    return os.path.join(self.app_namespace_path, CONFIG_FILE)

  @property
  def app_namespace_exists(self):
    return os.path.exists(self.app_namespace_path)

  @property
  def app_namespace_path(self):
    return os.path.join(self.app_dir_path, self.namespace)

  def config(self, _c: dict):
    _config = self.app_config
    _config.update(_c)
    return _config

  def format(self, dir_path: str, handler = None):
    for subdir, dirs, files in os.walk(dir_path):
      for file in files:
        path = os.path.join(subdir, file)
        basename = os.path.basename(path)

        if not basename.startswith('docker-compose') or not basename.endswith('.yml'):
          continue

        with open(path, 'r+') as fp:
          contents = fp.read()

          if handler:
            try:
              fp.seek(0)
              fp.write(handler(path, contents))
              fp.truncate()
            except KeyError:
              pass
