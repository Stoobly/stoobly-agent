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
  app = App(app_dir)

  context_lock = ContextLock(app)
  return os.path.exists(context_lock.lock_file_path())