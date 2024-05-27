import os
import pdb
import pathlib
import shutil

from .constants import SERVICE_TEMPLATE_VARIABLE, WORKFLOW_CI_TYPE, WORKFLOW_DEVELOPMENT_TYPE, WORKFLOW_TEMPLATE_VARIABLE
from .env import Env
from .workflow_command import WorkflowCommand

class WorkflowCreateCommand(WorkflowCommand):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)

    self.__env_vars = kwargs.get('env_vars') or []
    self.__force = not not kwargs.get('force')
    self.__type = kwargs.get('type') or WORKFLOW_DEVELOPMENT_TYPE

    self.__templates_dir = os.path.join(pathlib.Path(__file__).parent.resolve(), 'templates', 'workflow')

  @property
  def ci_template_path(self):
    return os.path.join(self.__templates_dir, 'ci')

  @property
  def development_template_path(self):
    return os.path.join(self.__templates_dir, 'development')

  @property
  def env_vars(self):
    return self.__env_vars

  @property
  def force(self):
    return self.__force

  @property
  def type(self):
    return self.__type

  def build_with_docker(self):
    self.as_docker()
    dest = os.path.join(self.workflow_path)

    if os.path.exists(dest) and self.force:
        shutil.rmtree(dest)

    if self.type == WORKFLOW_CI_TYPE:
      shutil.copytree(self.ci_template_path, dest, dirs_exist_ok=True)
    elif self.type == WORKFLOW_DEVELOPMENT_TYPE:
      shutil.copytree(self.development_template_path, dest, dirs_exist_ok=True)

    shutil.move(os.path.join(self.workflow_path, 'docker-compose.workflow.yml') , self.compose_path)
    self.format(self.compose_path, self.__format_handler)

  def __format_handler(self, path: str, contents: str):
    contents = contents.replace(SERVICE_TEMPLATE_VARIABLE, self.service_name)
    return contents.replace(WORKFLOW_TEMPLATE_VARIABLE, self.workflow_name)