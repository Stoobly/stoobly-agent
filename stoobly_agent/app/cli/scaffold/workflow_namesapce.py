import os
import shutil

from .app import App
from .constants import DOTENV_PATH_ENV, DOTENV_FILE, NAMESERVERS_FILE

class WorkflowNamespace():

  def __init__(self, app: App, namespace: str = None):
    self._app = app
    self._namespace = namespace
    self._path = os.path.join(app.data_dir.tmp_dir_path, namespace or '')

  @property
  def dotenv_path(self):
    return os.path.join(self.path, DOTENV_FILE)

  @property
  def nameservers_path(self):
    return os.path.join(self.path, NAMESERVERS_FILE)

  @property
  def namespace(self):
    return self._namespace

  @property
  def path(self):
    return self._path

  @property
  def run_script_path(self):
    return os.path.join(self.path, 'run.sh')

  @property
  def traefik_config_path(self):
    return os.path.join(self.path, 'traefik.yml')

  def copy_dotenv(self):
    dotenv_path = os.environ.get(DOTENV_PATH_ENV) or '.env'

    if os.path.isfile(dotenv_path):
      shutil.copy(dotenv_path, self.dotenv_path)

  def traefik_config_relative_path(self, path: str):
    if not path:
      return path
    return self.traefik_config_path.replace(path if path[len(path) - 1] == '/' else path + '/', '', 1)