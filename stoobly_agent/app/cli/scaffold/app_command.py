import os
import shutil

from .app_config import AppConfig
from .command import Command

class AppCommand(Command):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)

    if not kwargs['app_dir_path']:
        kwargs['app_dir_path'] = os.getcwd()

    self.__app_dir_path = kwargs.get('app_dir_path')
    self.__config = AppConfig(self.app_namespace_path)
    self.__config.network = kwargs.get('network') or os.path.basename(self.app_dir_path)

  @property
  def app_dir_path(self):
    return self.__app_dir_path

  @property
  def app_config(self):
    return self.__config

  @property
  def app_config_path(self):
    return self.__config.path

  @property
  def app_namespace_exists(self):
    return os.path.exists(self.app_namespace_path)

  @property
  def app_namespace_path(self):
    return os.path.join(self.app_dir_path, self.namespace)

  def config(self, _c: dict):
    _config = self.app_config.read()
    _config.update(_c)
    return _config

  # TODO: remove
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

  def copy_files_no_replace(self, source_dir: str, src_files: list, dest_dir: str):
    return self.copy_files(source_dir, src_files, dest_dir, False)

  def copy_files(self, source_dir: str, src_files: list, dest_dir: str, replace_ok=True):
    # Ensure the destination directory exists
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    for file in src_files:
      src_file_path = os.path.join(source_dir, file)
      if not os.path.isfile(src_file_path):
        continue
      
      if not os.path.exists(src_file_path):
        continue

      dest_subdir = os.path.join(dest_dir, os.path.dirname(file))

      if os.path.exists(os.path.join(dest_dir, file)) and not replace_ok:
        continue

      if not os.path.exists(dest_subdir):
        os.makedirs(dest_subdir, exist_ok=True)

      shutil.copy(src_file_path, dest_subdir)
