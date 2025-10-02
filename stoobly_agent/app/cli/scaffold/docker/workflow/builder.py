import os
import pdb

from typing import List, Union

from ...constants import (
  WORKFLOW_CONTAINER_CONFIGURE_TEMPLATE, WORKFLOW_CONTAINER_INIT_TEMPLATE, WORKFLOW_CONTAINER_PROXY_TEMPLATE, WORKFLOW_NAME
)
from ...local.workflow.builder import WorkflowBuilder
from ..builder import Builder
from ..constants import DOCKER_COMPOSE_WORKFLOW
from ..service.builder import DockerServiceBuilder
from .mock_decorator import MockDecorator
from .reverse_proxy_decorator import ReverseProxyDecorator


class DockerWorkflowBuilder(Builder, WorkflowBuilder):

  def __init__(self, workflow_path: str, service_builder: DockerServiceBuilder):
    WorkflowBuilder.__init__(self, workflow_path, service_builder)
    Builder.__init__(self, workflow_path, DOCKER_COMPOSE_WORKFLOW)

    self._context = '../'
    self._profiles = [WORKFLOW_NAME]

  @property
  def app(self):
    return f"{self.namespace}.app"

  @property
  def base_compose_file_path(self):
    return os.path.relpath(self.service_builder.compose_file_path, self.dir_path)

  @property
  def configure(self):
    return WORKFLOW_CONTAINER_CONFIGURE_TEMPLATE.format(service_name=self.namespace)

  @property
  def context(self):
    return self._context

  @property
  def context_docker_file_path(self):
    return os.path.relpath(self.service_builder.app_builder.context_docker_file_path, self.service_path)

  @property
  def init(self):
    return WORKFLOW_CONTAINER_INIT_TEMPLATE.format(service_name=self.namespace)

  @property
  def namespace(self):
    return f"{self.service_builder.service_name}"

  @property
  def profiles(self):
    return self._profiles

  @property
  def proxy(self):
    return WORKFLOW_CONTAINER_PROXY_TEMPLATE.format(service_name=self.namespace)

  def build_all(self):
    # Resources
    if self.config.detached:
      self.with_volume(self.service_builder.service_name)

    # Services
    self.build_init()
    self.build_configure()

    if self.config.hostname:
      self.build_proxy() # Depends on configure, must call build_configure first

  def build_init(self):
    # If the init_base service does not exist, we can't extend from it, return
    if not self.service_builder.init_base_service:
      return

    service = {
      'extends': self.service_builder.build_extends_init_base(self.dir_path),
      'profiles': self.profiles,
    }

    self.with_service(self.init, service)

  def build_configure(self):
    # If the configure_base service does not exist, we can't extend from it, return
    if not self.service_builder.configure_base_service:
      return

    depends_on = {}

    service = {
      'depends_on': depends_on,
      'extends': self.service_builder.build_extends_configure_base(self.dir_path),
      'profiles': self.profiles,
    }

    if self.init in self.services:
      depends_on[self.init] = {
        'condition': 'service_completed_successfully',
      }

    self.with_service(self.configure, service)

  def build_proxy(self):
    # If the proxy_base service does not exist, we can't extend from it, return
    if not self.service_builder.proxy_base_service:
      return

    depends_on = {}
    networks = {}

    service = {
      'depends_on': depends_on,
      'extends': self.service_builder.build_extends_proxy_base(self.dir_path),
      'networks': networks,
      'profiles': self.profiles,
    }

    if self.configure in self.services:
      depends_on[self.configure] = {
        'condition': 'service_completed_successfully',
      }

    # Expose this container service to the public network 
    # so that it is accessible to other Stoobly services
    networks[self.egress_network_name] = {}

    self.with_service(self.proxy, service)

  def build(self, workflow_decorators: List[Union[MockDecorator, ReverseProxyDecorator]] = None):
    """Build the Docker workflow with all components and decorators."""

    # Build all workflow components
    self.build_all()

    # Apply workflow decorators if provided
    if isinstance(workflow_decorators, list):
      for workflow_decorator in workflow_decorators:
        workflow_decorator(self).decorate()

    # Write the compose file
    self.write()

    return self

  def write(self):
    compose = {
      'services': self.services,
    }

    if self.networks:
      compose['networks'] = self.networks

    if self.volumes:
      compose['volumes'] = self.volumes

    super().write(compose)

