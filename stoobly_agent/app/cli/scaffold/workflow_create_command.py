import os
import pdb
import pathlib
import shutil

from typing import List, TypedDict, Union

from .docker.service.builder import ServiceBuilder
from .docker.workflow.mock_decorator import MockDecorator
from .docker.workflow.reverse_proxy_decorator import ReverseProxyDecorator
from .docker.workflow.builder import WorkflowBuilder
from .templates.factory import custom_files, maintained_files
from .workflow_command import WorkflowCommand

class BuildOptions(TypedDict):
  builder_class: type 
  service_builder: ServiceBuilder
  workflow_decorators: List[Union[MockDecorator, ReverseProxyDecorator]]

class WorkflowCreateCommand(WorkflowCommand):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)

    self.__env_vars = kwargs.get('env_vars') or []
    self.__force = not not kwargs.get('force')

    self.__templates_dir = os.path.join(pathlib.Path(__file__).parent.resolve(), 'templates', 'workflow')

  @property
  def build_templates_path(self):
    return os.path.join(self.__templates_dir, self.workflow_name, 'build')

  @property
  def env_vars(self):
    return self.__env_vars

  @property
  def force(self):
    return self.__force

  def build(self, **kwargs: BuildOptions):
    dest = os.path.join(self.workflow_path)
    if os.path.exists(dest) and self.force:
        shutil.rmtree(dest)

    if not os.path.exists(dest):
      os.makedirs(dest) 

    build_dir_path = self.build_dir_path
    if not os.path.exists(build_dir_path):
      os.makedirs(build_dir_path)

    dist_dir_path = self.dist_dir_path
    if not os.path.exists(dist_dir_path):
      os.makedirs(dist_dir_path)

    self.__write_custom_compose_file()
    self.__write_docker_compose_file(**kwargs)

    self.__copy_templates()

  def __copy_templates(self):
    templates_path = self.build_templates_path
    if not os.path.exists(templates_path):
      return

    build_dir_path = self.build_dir_path

    # Maintained files are files that will always be overwritten
    maintained_workflow_files = maintained_files(self.workflow_name)
    self.copy_files(templates_path, maintained_workflow_files, build_dir_path)

    # Custom files are files that may be modified by the user
    custom_workflow_files = custom_files(self.workflow_name)
    self.copy_files_no_replace(templates_path, custom_workflow_files, build_dir_path)

  def __write_custom_compose_file(self):
    dest = self.custom_compose_path
    if not os.path.exists(dest):
      with open(dest, 'w') as fp:
        fp.write('# Define services here')

  def __write_docker_compose_file(self, **kwargs):
    builder_class = kwargs.get('builder_class') or WorkflowBuilder
    service_builder = kwargs.get('service_builder') or ServiceBuilder(self.service_config)
    workflow_decorators: List[Union[MockDecorator, ReverseProxyDecorator]] = kwargs.get('workflow_decorators')

    workflow_builder = builder_class(self.workflow_path, service_builder)
    workflow_builder.build_all()

    if isinstance(workflow_decorators, list):
      for workflow_decorator in workflow_decorators:
        workflow_decorator(workflow_builder).decorate()

    workflow_builder.write()