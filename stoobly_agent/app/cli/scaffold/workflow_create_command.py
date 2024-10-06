import os
import pdb
import shutil

from typing import List, TypedDict, Union

from .app import App
from .constants import COMPOSE_TEMPLATE, WORKFLOW_MOCK_TYPE, WORKFLOW_RECORD_TYPE, WORKFLOW_TEST_TYPE, WORKFLOW_TEMPLATE
from .docker.service.builder import ServiceBuilder
from .docker.workflow.mock_decorator import MockDecorator
from .docker.workflow.reverse_proxy_decorator import ReverseProxyDecorator
from .docker.workflow.builder import WorkflowBuilder
from .templates.factory import custom_files, maintained_files
from .templates.constants import (
 CORE_BUILD_SERVICE_NAME, CORE_GATEWAY_SERVICE_NAME, CORE_MOCK_UI_SERVICE_NAME, CORE_MOCK_WORKFLOW
)
from .workflow_command import WorkflowCommand

CORE_WORKFLOWS = [WORKFLOW_MOCK_TYPE, WORKFLOW_RECORD_TYPE, WORKFLOW_TEST_TYPE]

class BuildOptions(TypedDict):
  builder_class: type 
  headless: bool
  service_builder: ServiceBuilder
  template: WORKFLOW_TEMPLATE
  workflow_decorators: List[Union[MockDecorator, ReverseProxyDecorator]]

class WorkflowCreateCommand(WorkflowCommand):

  def __init__(self, app: App, **kwargs):
    super().__init__(app, **kwargs)

    self.__env_vars: List[str] = kwargs.get('env') or []
    self.__force = not not kwargs.get('force')

  @property
  def build_templates_path(self):
    return self.workflow_build_templates_path(self.workflow_name)

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

    build_dir_path = self.build_dir_path
    if not os.path.exists(build_dir_path):
      os.makedirs(build_dir_path)

    dist_dir_path = self.dist_dir_path
    if not os.path.exists(dist_dir_path):
      os.makedirs(dist_dir_path)

    # Create workflow custom compose file
    self.__write_custom_compose_file()

    # Create workflow maintained compose file
    workflow_builder = self.__write_docker_compose_file(**kwargs)
    self.__copy_templates(workflow_builder, kwargs.get('template'))

    # Create core services for a custom workflow
    # For now the core services are not differentiated by workflow thus no need to pass in 'template'
    if self.workflow_name not in CORE_WORKFLOWS:
      self.__add_core_services(kwargs.get('headless'))

  def workflow_build_templates_path(self, workflow_name: str):
    return os.path.join(self.workflow_templates_root_dir, workflow_name, 'build')

  # A custom workflow may depend on a core service
  # However, currently core services are not built but copied
  # For now, tailor the copied core service to the custom workflow
  def __add_core_service(self, service_name):
    app_templates_root_dir = self.app_templates_root_dir
    service_src = os.path.join(app_templates_root_dir, service_name, CORE_MOCK_WORKFLOW)
    service_dest = os.path.join(self.scaffold_namespace_path, service_name, self.workflow_name)

    if os.path.exists(service_dest):
      shutil.rmtree(service_dest)
    shutil.copytree(service_src, service_dest)

    compose_file_src = os.path.join(service_dest, COMPOSE_TEMPLATE.format(workflow=CORE_MOCK_WORKFLOW))
    compose_file_dest = os.path.join(service_dest, COMPOSE_TEMPLATE.format(workflow=self.workflow_name))
    os.rename(compose_file_src, compose_file_dest)

    # Replace workflow name
    with open(compose_file_dest, 'r+') as fp:
      contents = fp.read()
      fp.seek(0)
      fp.write(contents.replace(CORE_MOCK_WORKFLOW, self.workflow_name))
      fp.truncate()

  def __add_core_services(self, headless):
    self.__add_core_service(CORE_BUILD_SERVICE_NAME)

    # If not headless, then create gateway and mock ui core services
    if not headless:
      self.__add_core_service(CORE_GATEWAY_SERVICE_NAME) 
      self.__add_core_service(CORE_MOCK_UI_SERVICE_NAME)

  def __copy_templates(self, workflow_builder: WorkflowBuilder, template: WORKFLOW_TEMPLATE = None):
    if not template:
      templates_path = self.build_templates_path
    else:
      templates_path = self.workflow_build_templates_path(template)

    if not os.path.exists(templates_path):
      return

    build_dir_path = self.build_dir_path

    # Maintained files are files that will always be overwritten
    maintained_workflow_files = maintained_files(self.workflow_name, workflow_builder)
    self.copy_files(templates_path, maintained_workflow_files, build_dir_path)

    # Custom files are files that may be modified by the user
    custom_workflow_files = custom_files(self.workflow_name, workflow_builder)
    self.copy_files_no_replace(templates_path, custom_workflow_files, build_dir_path)

  def __write_custom_compose_file(self):
    dest = self.custom_compose_path
    if not os.path.exists(dest):
      with open(dest, 'w') as fp:
        fp.write('# Define services here')

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

    return workflow_builder