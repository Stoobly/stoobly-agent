import os
import pdb
import shutil

from typing import List, TypedDict, Union

from .app import App
from .constants import WORKFLOW_MOCK_TYPE, WORKFLOW_RECORD_TYPE, WORKFLOW_TEST_TYPE, WORKFLOW_TEMPLATE
from .docker.service.builder import ServiceBuilder
from .docker.workflow.mock_decorator import MockDecorator
from .docker.workflow.reverse_proxy_decorator import ReverseProxyDecorator
from .docker.workflow.builder import WorkflowBuilder
from .templates.factory import custom_files, maintained_files
from .workflow_command import WorkflowCommand

CORE_WORKFLOWS = [WORKFLOW_MOCK_TYPE, WORKFLOW_RECORD_TYPE, WORKFLOW_TEST_TYPE]

class BuildOptions(TypedDict):
  builder_class: type 
  service_builder: ServiceBuilder
  template: WORKFLOW_TEMPLATE
  workflow_decorators: List[Union[MockDecorator, ReverseProxyDecorator]]

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

  def build(self, **kwargs: BuildOptions):
    # Create workflow folder
    dest = os.path.join(self.workflow_path)
    if os.path.exists(dest) and self.force:
        shutil.rmtree(dest)

    if not os.path.exists(dest):
      os.makedirs(dest) 

    # Create workflow maintained compose file
    workflow_builder = self.__write_docker_compose_file(**kwargs)
    self.__copy_templates(workflow_builder, kwargs.get('template'))

  def build_workflow_templates_path(self, workflow_name: str):
    return os.path.join(self.workflow_templates_root_dir, workflow_name)

  def __copy_templates(self, workflow_builder: WorkflowBuilder, template: WORKFLOW_TEMPLATE = None):
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

  def __write_docker_compose_file(self, **kwargs: BuildOptions):
    builder_class = kwargs.get('builder_class') or WorkflowBuilder
    service_builder = kwargs.get('service_builder') or ServiceBuilder(self.service_config)
    workflow_decorators: List[Union[MockDecorator, ReverseProxyDecorator]] = kwargs.get('workflow_decorators')

    workflow_builder = builder_class(self.workflow_path, service_builder)
    workflow_builder.with_env(list(self.env_vars))
    workflow_builder.build_all()

    if isinstance(workflow_decorators, list):
      for workflow_decorator in workflow_decorators:
        workflow_decorator(workflow_builder).decorate()

    workflow_builder.write()
    workflow_builder.initialize_custom_file()

    return workflow_builder