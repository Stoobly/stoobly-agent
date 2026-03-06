import os
import pdb
import shutil

from copy import deepcopy
from typing import Union

from .app import App
from .constants import WORKFLOW_MOCK_TYPE, WORKFLOW_RECORD_TYPE, WORKFLOW_TEST_TYPE
from .local.service.builder import ServiceBuilder
from .docker.service.builder import DockerServiceBuilder
from .docker.workflow.decorators_factory import get_workflow_decorators
from .service_command import ServiceCommand
from .workflow_create_command import WorkflowCreateCommand

class ServiceCreateCommand(ServiceCommand):

  def __init__(self, app: App, **kwargs):
    super().__init__(app, **kwargs)

    self.__upstream_port = kwargs.get('upstream_port') or []
    self.__env_vars = kwargs.get('env') or []
    self.__workflows = kwargs.get('workflow') or [WORKFLOW_RECORD_TYPE, WORKFLOW_MOCK_TYPE, WORKFLOW_TEST_TYPE]

  @property
  def upstream_port(self):
    return self.__upstream_port

  @property
  def env_vars(self):
    return self.__env_vars

  @property
  def workflows(self):
    return self.__workflows

  @property
  def create_docker_files(self):
    """Determine if Docker files should be created based on app config runtime setting."""
    return self.app_config.runtime_docker

  def build(self):
    # Choose builder based on app runtime configuration
    if self.app_config.runtime_docker:
      service_builder = DockerServiceBuilder(self.service_config)
    else:
      service_builder = ServiceBuilder(self.service_config)
    
    service_builder.with_env(list(self.env_vars))
    service_decorators = []

    for service_decorator in service_decorators:
      service_decorator(service_builder).decorate()

    service_builder.write()

    workflow_kwargs = {
      'app_dir_path': self.app_dir_path,
      'namespace': self.scaffold_namespace, 
      'service_name': self.service_name,
    }

    if WORKFLOW_MOCK_TYPE in self.workflows:
      self.__build_with_mock_workflow(service_builder, **workflow_kwargs)

    if WORKFLOW_RECORD_TYPE in self.workflows:
      service_builder_copy = deepcopy(service_builder)
      service_builder_copy.with_upstream_port(self.upstream_port)
      self.__build_with_record_workflow(service_builder_copy, **workflow_kwargs)

    if WORKFLOW_TEST_TYPE in self.workflows:
      self.__build_with_test_workflow(service_builder, **workflow_kwargs)

    self.service_config.write()

  def reset(self):
    dest = self.service_path

    if os.path.exists(dest):
      shutil.rmtree(dest)

  def __build_with_mock_workflow(self, service_builder: Union[ServiceBuilder, DockerServiceBuilder], **kwargs):
    mock_workflow = WorkflowCreateCommand(self.app, **{ **kwargs, **{ 'workflow_name': WORKFLOW_MOCK_TYPE }})

    workflow_decorators = get_workflow_decorators(WORKFLOW_MOCK_TYPE, self.service_config)
    mock_workflow.build(service_builder=service_builder, workflow_decorators=workflow_decorators)

  def __build_with_record_workflow(self, service_builder: Union[ServiceBuilder, DockerServiceBuilder], **kwargs):
    record_workflow = WorkflowCreateCommand(self.app, **{ **kwargs, **{ 'workflow_name': WORKFLOW_RECORD_TYPE }})

    workflow_decorators = get_workflow_decorators(WORKFLOW_RECORD_TYPE, self.service_config)
    record_workflow.build(service_builder=service_builder, workflow_decorators=workflow_decorators)

  def __build_with_test_workflow(self, service_builder: Union[ServiceBuilder, DockerServiceBuilder], **kwargs):
    mock_workflow = WorkflowCreateCommand(self.app, **{ **kwargs, **{ 'workflow_name': WORKFLOW_TEST_TYPE }})

    workflow_decorators = get_workflow_decorators(WORKFLOW_TEST_TYPE, self.service_config)
    mock_workflow.build(service_builder=service_builder, workflow_decorators=workflow_decorators)