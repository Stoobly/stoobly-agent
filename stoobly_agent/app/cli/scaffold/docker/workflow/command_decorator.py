from ...constants import (
  SERVICE_UPSTREAM_HOSTNAME, SERVICE_UPSTREAM_PORT, SERVICE_UPSTREAM_SCHEME,
)
from ...local.workflow.builder import WorkflowBuilder

class CommandDecorator():

  def __init__(self, workflow_builder: WorkflowBuilder):
    self.__workflow_builder = workflow_builder

  @property
  def workflow_builder(self):
    return self.__workflow_builder

  @property
  def proxy_mode(self):
    config = self.workflow_builder.config

    if config.upstream_hostname == 'host.docker.internal':
      return f"upstream:{SERVICE_UPSTREAM_SCHEME}://{SERVICE_UPSTREAM_HOSTNAME}:{SERVICE_UPSTREAM_PORT}"

    if config.hostname != config.upstream_hostname or config.scheme != config.upstream_scheme or config.port != config.upstream_port:
      return f"reverse:{SERVICE_UPSTREAM_SCHEME}://{SERVICE_UPSTREAM_HOSTNAME}:{SERVICE_UPSTREAM_PORT}"

    return 'regular'