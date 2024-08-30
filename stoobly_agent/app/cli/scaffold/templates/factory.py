from ..constants import WORKFLOW_MOCK_TYPE, WORKFLOW_RECORD_TYPE
from ..docker.workflow.builder import WorkflowBuilder
from .constants import CUSTOM_CONFIGURE, MAINTAINED_CONFIGURE, MOCK_WORKFLOW_CUSTOM_FILES, MOCK_WORKFLOW_MAINTAINED_FILES, RECORD_WORKFLOW_CUSTOM_FILES, RECORD_WORKFLOW_MAINTAINED_FILES

def custom_files(workflow: str, workflow_builder: WorkflowBuilder):
  files = []
  if workflow == WORKFLOW_MOCK_TYPE:
    files = MOCK_WORKFLOW_CUSTOM_FILES
  elif workflow == WORKFLOW_RECORD_TYPE:
    files = RECORD_WORKFLOW_CUSTOM_FILES
  else:
    if workflow_builder.configure in workflow_builder.services:
      files.append(CUSTOM_CONFIGURE)

  service_config = workflow_builder.config
  if not service_config.hostname:
    if CUSTOM_CONFIGURE in files:
      files.remove(CUSTOM_CONFIGURE)

  return files

def maintained_files(workflow: str, workflow_builder: WorkflowBuilder):
  files = []

  if workflow == WORKFLOW_MOCK_TYPE:
    files = MOCK_WORKFLOW_MAINTAINED_FILES
  elif workflow == WORKFLOW_RECORD_TYPE:
    files = RECORD_WORKFLOW_MAINTAINED_FILES
  else:
    if workflow_builder.configure in workflow_builder.services:
      files.append(MAINTAINED_CONFIGURE)

  service_config = workflow_builder.config
  if not service_config.hostname:
    files.remove(MAINTAINED_CONFIGURE)

  return files