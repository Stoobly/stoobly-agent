import os
import pathlib
import shutil

from .app import App
from .app_config import AppConfig
from .command import Command

class AppCommand(Command):

  def __init__(self, app: App):
    super().__init__(app)

    self.__config = AppConfig(self.scaffold_namespace_path)
    self.__config.network = app.network

  @property
  def app_dir_path(self):
    return self.app.dir_path

  @property
  def app_dir_exists(self):
    return os.path.exists(self.app_dir_path)

  @property
  def app_config(self):
    return self.__config

  @property
  def app_config_path(self):
    return self.__config.path

  @property
  def app_namespace_path(self):
    return self.app.namespace_path

  @property
  def app_templates_root_dir(self):
    return os.path.join(self.templates_root_dir, 'app')

  @property
  def scaffold_dir_path(self):
    return self.app.scaffold_dir_path

  @property
  def scaffold_namespace_path(self):
    return self.app.scaffold_namespace_path

  @property
  def templates_root_dir(self):
    return os.path.join(pathlib.Path(__file__).parent.resolve(), 'templates')

  def config(self, _c: dict):
    _config = self.app_config.read()
    _config.update(_c)
    return _config

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
