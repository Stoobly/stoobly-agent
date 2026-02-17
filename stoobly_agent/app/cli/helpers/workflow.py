import os

from stoobly_agent.app.cli.scaffold.app import App
from stoobly_agent.app.cli.scaffold.constants import APP_DIR_ENV, WORKFLOW_NAME_ENV
from stoobly_agent.app.cli.scaffold.context_lock import ContextLock

def workflow_running() -> bool:
  """Check if a workflow is currently running.

  Checks environment variables for WORKFLOW_NAME and verifies the context
  lock file exists.

  Returns:
    bool: True if workflow is running, False otherwise.
  """
  workflow_name = os.environ.get(WORKFLOW_NAME_ENV)

  if not workflow_name:
    return False

  # Get app directory from environment or use current directory
  app_dir = os.environ.get(APP_DIR_ENV) or os.getcwd()

  # If the data directory doesn't exist yet, no workflow can be running.
  # Avoids attempting to create it (and failing with PermissionError) just to check the lock file.
  from stoobly_agent.config.data_dir import DATA_DIR_NAME
  if not os.path.isdir(os.path.join(app_dir, DATA_DIR_NAME)):
    return False

  app = App(app_dir)

  context_lock = ContextLock(app)
  return os.path.exists(context_lock.lock_file_path())