from ..constants import WORKFLOW_MOCK_TYPE, WORKFLOW_RECORD_TYPE
from .constants import MOCK_WORKFLOW_CUSTOM_FILES, MOCK_WORKFLOW_MAINTAINED_FILES, RECORD_WORKFLOW_CUSTOM_FILES, RECORD_WORKFLOW_MAINTAINED_FILES

def custom_files(workflow: str):
  if workflow == WORKFLOW_MOCK_TYPE:
    return MOCK_WORKFLOW_CUSTOM_FILES
  elif workflow == WORKFLOW_RECORD_TYPE:
    return RECORD_WORKFLOW_CUSTOM_FILES
  else:
    return []

def maintained_files(workflow: str):
  if workflow == WORKFLOW_MOCK_TYPE:
    return MOCK_WORKFLOW_MAINTAINED_FILES
  elif workflow == WORKFLOW_RECORD_TYPE:
    return RECORD_WORKFLOW_MAINTAINED_FILES
  else:
    return []