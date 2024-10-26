import os
import pdb
import shutil

from .app import App
from .constants import COMPOSE_TEMPLATE, WORKFLOW_MOCK_TYPE, WORKFLOW_RECORD_TYPE, WORKFLOW_TEST_TYPE
from .service_workflow import ServiceWorkflow
from .workflow_command import WorkflowCommand

CORE_WORKFLOWS = [WORKFLOW_MOCK_TYPE, WORKFLOW_RECORD_TYPE, WORKFLOW_TEST_TYPE]

class WorkflowCopyCommand(WorkflowCommand):

  def __init__(self, app: App, **kwargs):
    super().__init__(app, **kwargs)

    self.__force = not not kwargs.get('force')

  @property
  def force(self):
    return self.__force

  def copy(self, destination_workflow_name: str):
    destination_workflow = ServiceWorkflow(self.service_name, destination_workflow_name, self.app)

    # Create workflow folder
    dest = os.path.join(destination_workflow.path)
    if os.path.exists(dest) and self.force:
        shutil.rmtree(dest)

    if not os.path.exists(dest):
      os.makedirs(dest) 

    self.app.copy_folders_and_hidden_files(self.workflow_path, dest)

    compose_file_src = os.path.join(dest, COMPOSE_TEMPLATE.format(workflow=self.workflow_name))
    compose_file_dest = os.path.join(dest, COMPOSE_TEMPLATE.format(workflow=destination_workflow_name))
    os.rename(compose_file_src, compose_file_dest)

    # Replace workflow name
    with open(compose_file_dest, 'r+') as fp:
      contents = fp.read()
      fp.seek(0)
      fp.write(contents.replace(self.workflow_name, destination_workflow_name))
      fp.truncate()