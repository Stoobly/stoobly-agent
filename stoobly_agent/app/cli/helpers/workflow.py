import os

from stoobly_agent.app.cli.scaffold.app import App
from stoobly_agent.app.cli.scaffold.constants import APP_DIR_ENV, WORKFLOW_NAME_ENV, WORKFLOW_NAMESPACE_ENV
from stoobly_agent.app.cli.scaffold.workflow_namesapce import WorkflowNamespace

def workflow_running() -> bool:
  """Check if a workflow is currently running.
  
  Checks environment variables for WORKFLOW_NAME, and WORKFLOW_NAMESPACE.
  
  Returns:
    bool: True if workflow is running (file exists), False otherwise.
  """
  workflow_name = os.environ.get(WORKFLOW_NAME_ENV)
  workflow_namespace = os.environ.get(WORKFLOW_NAMESPACE_ENV)
  
  if not workflow_name:
    return False
  
  # Get app directory from environment or use current directory
  app_dir = os.environ.get(APP_DIR_ENV) or os.getcwd()
  app = App(app_dir)
  
  # Create workflow namespace
  workflow_namespace_obj = WorkflowNamespace(app, workflow_namespace)
  
  return os.path.exists(workflow_namespace_obj.lock_file_path(workflow_name))