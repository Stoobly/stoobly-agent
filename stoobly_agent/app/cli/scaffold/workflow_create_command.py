import os
import pdb
import shutil

from typing import List, TypedDict, Union

from stoobly_agent.app.cli.scaffold.local.service.builder import ServiceBuilder

from .app import App
from .constants import WORKFLOW_TEMPLATE_OPTION
from .docker.service.builder import DockerServiceBuilder

from .docker.workflow.builder import DockerWorkflowBuilder
from .templates.factory import custom_files, maintained_files
from .local.workflow.builder import WorkflowBuilder
from .workflow_command import WorkflowCommand

class BuildOptions(TypedDict):
  service_builder: DockerServiceBuilder
  template: WORKFLOW_TEMPLATE_OPTION
  workflow_decorators: list

class WorkflowCreateCommand(WorkflowCommand):

  def __init__(self, app: App, **kwargs):
    super().__init__(app, **kwargs)

    self.__env_vars: List[str] = kwargs.get('env') or []
    self.__force = not not kwargs.get('force')

  @property
  def workflow_templates_path(self):
    return self.build_workflow_templates_path(self.workflow_name)

  @property
  def env_vars(self):
    return self.__env_vars

  @property
  def force(self):
    return self.__force

  @property
  def create_docker_files(self):
    """Determine if Docker files should be created based on app config runtime setting."""
    return self.app_config.runtime_docker

  def build(self, **kwargs: BuildOptions):
    # Create workflow folder
    dest = os.path.join(self.workflow_path)
    if os.path.exists(dest) and self.force:
        shutil.rmtree(dest)

    if not os.path.exists(dest):
      os.makedirs(dest) 

    service_builder = kwargs.get('service_builder')
    workflow_builder = None

    # Create workflow maintained compose file only if Docker files are enabled
    if self.create_docker_files:
      if not service_builder:
        service_builder = DockerServiceBuilder(self.service_config)
        service_builder.load()

      workflow_builder = DockerWorkflowBuilder(self.workflow_path, service_builder)
      workflow_builder.build(kwargs.get('workflow_decorators'))
    else:
      if not service_builder:
        service_builder = ServiceBuilder(self.service_config)

      workflow_builder = WorkflowBuilder(self.workflow_path, service_builder)
    
    self.__copy_templates(workflow_builder, kwargs.get('template'))

    if not self.workflow_config.empty:
      self.workflow_config.write()

  def build_workflow_templates_path(self, workflow_name: str):
    return os.path.join(self.workflow_templates_root_dir, workflow_name)

  def __copy_templates(self, workflow_builder: WorkflowBuilder, template: WORKFLOW_TEMPLATE_OPTION = None):
    if not template:
      templates_path = self.workflow_templates_path
    else:
      templates_path = self.build_workflow_templates_path(template)

    if not os.path.exists(templates_path):
      return

    # Maintained files are files that will always be overwritten
    maintained_workflow_files = maintained_files(template or self.workflow_name, workflow_builder)
    self.copy_files(templates_path, maintained_workflow_files, self.workflow_path)

    # Custom files are files that may be modified by the user
    custom_workflow_files = custom_files(template or self.workflow_name, workflow_builder)
    self.copy_files_no_replace(templates_path, custom_workflow_files, self.workflow_path)

