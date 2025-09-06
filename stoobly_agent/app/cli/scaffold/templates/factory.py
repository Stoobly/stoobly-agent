import pdb

from ..constants import WORKFLOW_MOCK_TYPE, WORKFLOW_RECORD_TYPE, WORKFLOW_TEST_TYPE
from ..local.workflow.builder import WorkflowBuilder
from ..docker.workflow.builder import DockerWorkflowBuilder
from .constants import (
  CUSTOM_CONFIGURE, CUSTOM_INIT, CUSTOM_PUBLIC_GITIGNORE, MAINTAINED_CONFIGURE, 
  MOCK_WORKFLOW_CUSTOM_FILES, MOCK_WORKFLOW_CUSTOM_LOCAL_FILES, MOCK_WORKFLOW_MAINTAINED_FILES, MOCK_WORKFLOW_CUSTOM_DOCKER_FILES,
  RECORD_WORKFLOW_CUSTOM_FILES, RECORD_WORKFLOW_CUSTOM_LOCAL_FILES, RECORD_WORKFLOW_MAINTAINED_FILES, RECORD_WORKFLOW_CUSTOM_DOCKER_FILES,
  TEST_WORKFLOW_CUSTOM_FILES, TEST_WORKFLOW_CUSTOM_LOCAL_FILES, TEST_WORKFLOW_MAINTAINED_FILES, TEST_WORKFLOW_CUSTOM_DOCKER_FILES
)

def custom_files(workflow: str, workflow_builder: WorkflowBuilder = None):
  files = []
  if workflow == WORKFLOW_MOCK_TYPE:
    files = MOCK_WORKFLOW_CUSTOM_FILES.copy()
  elif workflow == WORKFLOW_RECORD_TYPE:
    files = RECORD_WORKFLOW_CUSTOM_FILES.copy()
  elif workflow == WORKFLOW_TEST_TYPE:
    files = TEST_WORKFLOW_CUSTOM_FILES.copy()
  else:
    files.append(CUSTOM_CONFIGURE)
    files.append(CUSTOM_INIT)

  # Add Docker-specific files if workflow_builder is a DockerWorkflowBuilder
  if isinstance(workflow_builder, DockerWorkflowBuilder):
    if workflow == WORKFLOW_MOCK_TYPE:
      files.extend(MOCK_WORKFLOW_CUSTOM_DOCKER_FILES)
    elif workflow == WORKFLOW_RECORD_TYPE:
      files.extend(RECORD_WORKFLOW_CUSTOM_DOCKER_FILES)
    elif workflow == WORKFLOW_TEST_TYPE:
      files.extend(TEST_WORKFLOW_CUSTOM_DOCKER_FILES)
  else:
    if workflow == WORKFLOW_MOCK_TYPE:
      files.extend(MOCK_WORKFLOW_CUSTOM_LOCAL_FILES)
    elif workflow == WORKFLOW_RECORD_TYPE:
      files.extend(RECORD_WORKFLOW_CUSTOM_LOCAL_FILES)
    elif workflow == WORKFLOW_TEST_TYPE:
      files.extend(TEST_WORKFLOW_CUSTOM_LOCAL_FILES)

  # Fixtures are only relevant if the workflow is mock/test and if the service has a hostname
  if workflow_builder and not workflow_builder.config.hostname:
    if CUSTOM_PUBLIC_GITIGNORE in files:
      files.remove(CUSTOM_PUBLIC_GITIGNORE)

  return files

def maintained_files(workflow: str, workflow_builder: WorkflowBuilder = None):
  files = []

  if workflow == WORKFLOW_MOCK_TYPE:
    files = MOCK_WORKFLOW_MAINTAINED_FILES.copy()
  elif workflow == WORKFLOW_RECORD_TYPE:
    files = RECORD_WORKFLOW_MAINTAINED_FILES.copy()
  elif workflow == WORKFLOW_TEST_TYPE:
    files = TEST_WORKFLOW_MAINTAINED_FILES.copy()
  else:
    files.append(MAINTAINED_CONFIGURE)

  return files