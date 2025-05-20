import pdb

from ..constants import WORKFLOW_MOCK_TYPE, WORKFLOW_RECORD_TYPE, WORKFLOW_TEST_TYPE
from ..docker.workflow.builder import WorkflowBuilder
from .constants import (
  CUSTOM_CONFIGURE, CUSTOM_INIT, CUSTOM_PUBLIC_GITIGNORE, MAINTAINED_CONFIGURE, MOCK_WORKFLOW_CUSTOM_FILES, MOCK_WORKFLOW_MAINTAINED_FILES, RECORD_WORKFLOW_CUSTOM_FILES, RECORD_WORKFLOW_MAINTAINED_FILES, TEST_WORKFLOW_CUSTOM_FILES, TEST_WORKFLOW_MAINTAINED_FILES
)

def custom_files(workflow: str, workflow_builder: WorkflowBuilder):
  files = []
  if workflow == WORKFLOW_MOCK_TYPE:
    files = MOCK_WORKFLOW_CUSTOM_FILES
  elif workflow == WORKFLOW_RECORD_TYPE:
    files = RECORD_WORKFLOW_CUSTOM_FILES
  elif workflow == WORKFLOW_TEST_TYPE:
    files = TEST_WORKFLOW_CUSTOM_FILES
  else:
    if workflow_builder.configure in workflow_builder.services:
      files.append(CUSTOM_CONFIGURE)

    if workflow_builder.init in workflow_builder.services:
      files.append(CUSTOM_INIT)

  # Fixtures are only relevant if the workflow is mock/test and if the service has a hostname
  if not workflow_builder.config.hostname:
    if CUSTOM_PUBLIC_GITIGNORE in files:
      files.remove(CUSTOM_PUBLIC_GITIGNORE)

  return files

def maintained_files(workflow: str, workflow_builder: WorkflowBuilder):
  files = []

  if workflow == WORKFLOW_MOCK_TYPE:
    files = MOCK_WORKFLOW_MAINTAINED_FILES
  elif workflow == WORKFLOW_RECORD_TYPE:
    files = RECORD_WORKFLOW_MAINTAINED_FILES
  elif workflow == WORKFLOW_TEST_TYPE:
    files = TEST_WORKFLOW_MAINTAINED_FILES
  else:
    if workflow_builder.configure in workflow_builder.services:
      files.append(MAINTAINED_CONFIGURE)

  return files