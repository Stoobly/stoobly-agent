import os

from stoobly_agent.app.cli.scaffold.app import App
from stoobly_agent.app.cli.scaffold.constants import APP_DIR_ENV, CONTEXT_DIR_MOUNT_ENV, WORKFLOW_NAME_ENV
from stoobly_agent.app.cli.scaffold.context_lock import ContextLock
from stoobly_agent.config.data_dir import DATA_DIR_NAME


def workflow_running() -> bool:
  """Check if a workflow is currently running.

  Checks environment variables for WORKFLOW_NAME and verifies the context
  lock file exists.

  Inside a Docker container APP_DIR contains the host path (not accessible
  inside the container); CONTEXT_DIR_MOUNT holds the container-local equivalent.

  Returns:
    bool: True if workflow is running, False otherwise.
  """
  if not os.environ.get(WORKFLOW_NAME_ENV):
    return False

  app_dir_env = os.environ.get(APP_DIR_ENV)

  if app_dir_env and os.path.isdir(os.path.join(app_dir_env, DATA_DIR_NAME)):
    # In local env: APP_DIR points to a real, accessible path.
    app_dir = app_dir_env
  else:
    # In Docker container: APP_DIR is the host path, not accessible here.
    # CONTEXT_DIR_MOUNT is the container-local equivalent (e.g. /home/stoobly).
    app_dir = os.environ.get(CONTEXT_DIR_MOUNT_ENV) or os.getcwd()

  if not os.path.isdir(os.path.join(app_dir, DATA_DIR_NAME)):
    return False

  app = App(app_dir)
  context_lock = ContextLock(app)
  return os.path.exists(context_lock.lock_file_path())

