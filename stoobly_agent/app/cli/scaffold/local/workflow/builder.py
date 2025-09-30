import os

from ...constants import SERVICE_NAME_ENV, WORKFLOW_NAME_ENV, WORKFLOW_NAMESPACE_ENV
from ..service.builder import ServiceBuilder

class WorkflowBuilder():

  def __init__(self, workflow_path: str, service_builder: ServiceBuilder):
    self._env = [SERVICE_NAME_ENV, WORKFLOW_NAME_ENV, WORKFLOW_NAMESPACE_ENV]
    self._service_builder = service_builder
    self._workflow_name = os.path.basename(workflow_path)

  @property
  def config(self):
    return self._service_builder.config

  @property
  def service_builder(self):
    return self._service_builder

  @property
  def service_path(self):
    return self._service_builder.dir_path

  @property
  def workflow_name(self):
    return self._workflow_name

  def env_dict(self):
    env = {}
    for e in self._env:
      env[e] = '${' + e + '}'
    return env
