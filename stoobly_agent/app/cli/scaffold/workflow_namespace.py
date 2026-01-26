import os
import shutil

from stoobly_agent.lib.logger import Logger

from .app import App
from .constants import DOTENV_PATH_ENV, DOTENV_FILE, NAMESERVERS_FILE

LOG_ID = 'WorkflowNamespace'

class WorkflowNamespace():

  def __init__(self, app: App, namespace: str = None):
    self._app = app
    self._namespace = namespace
    self._path = os.path.join(app.data_dir.tmp_dir_path, namespace or '')

    if not os.path.exists(self._path):
      os.makedirs(self._path, exist_ok=True)

  @property
  def app(self):
    return self._app

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
  def pid_file_extension(self):
    return '.pid'

  @property
  def run_script_path(self):
    return os.path.join(self.path, 'run.sh')

  @property
  def timestamp_file_extension(self):
    return '.timestamp'

  @property
  def traefik_config_path(self):
    return os.path.join(self.path, 'traefik.yml')


  def copy_dotenv(self):
    dotenv_path = os.environ.get(DOTENV_PATH_ENV) or '.env'

    if os.path.isfile(dotenv_path):
      shutil.copy(dotenv_path, self.dotenv_path)


  def log_file_path(self, workflow_name: str):
    """Get the path to the PID file for this workflow."""
    return os.path.join(self.path, f"{workflow_name}.log")

  def pid_file_path(self, workflow_name: str):
    """Get the path to the PID file for this workflow."""
    return os.path.join(self.path, f"{workflow_name}{self.pid_file_extension}")


  def remove_log_file(self, workflow_name: str):
    log_file_path = self.log_file_path(workflow_name)
    if os.path.exists(log_file_path):
      try:
        os.remove(log_file_path)
      except Exception as e:
        Logger.instance(LOG_ID).warning(f"Failed to remove log file: {e}")

  def remove_pid_file(self, workflow_name: str):
    pid_file_path = self.pid_file_path(workflow_name)
    if os.path.exists(pid_file_path):
      try:
        os.remove(pid_file_path)
      except Exception as e:
        Logger.instance(LOG_ID).warning(f"Failed to remove pid file: {e}")

  def remove_timestamp_file(self, workflow_name: str):
    timestamp_file_path = self.timestamp_file_path(workflow_name)
    if os.path.exists(timestamp_file_path):
      try:
        os.remove(timestamp_file_path)
      except Exception as e:
        Logger.instance(LOG_ID).warning(f"Failed to remove timestamp file: {e}")

  def timestamp_file_name(self, workflow_name: str):
    return f"{workflow_name}{self.timestamp_file_extension}"

  def timestamp_file_path(self, workflow_name: str):
    """Get the path to the timestamp file for this workflow."""
    return os.path.join(self.path, self.timestamp_file_name(workflow_name))

  def traefik_config_relative_path(self, path: str):
    if not path:
      return path
    return self.traefik_config_path.replace(path if path[len(path) - 1] == '/' else path + '/', '', 1)
