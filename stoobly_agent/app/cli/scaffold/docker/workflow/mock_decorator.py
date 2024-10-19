import pdb

from ...constants import SERVICE_HOSTNAME, SERVICE_PORT, SERVICE_SCHEME
from .builder import WorkflowBuilder

class MockDecorator():

  def __init__(self, workflow_builder: WorkflowBuilder):
    self.__workflow_builder = workflow_builder

  @property
  def workflow_builder(self):
    return self.__workflow_builder

  @property
  def service_builder(self):
    return self.workflow_builder.service_builder

  def decorate(self):
    config = self.service_builder.config

    command = [
      '--certs', f"../{SERVICE_HOSTNAME}-joined.pem",
      '--headless',
      '--intercept',
      '--lifecycle-hooks-path', 'lifecycle_hooks.py',
      '--proxy-mode', config.proxy_mode,
      '--proxy-port', f"{SERVICE_PORT}",
      '--response-fixtures-path', 'fixtures.yml',
      '--ssl-insecure'
    ]

    services = self.__workflow_builder.services
    proxy_name = self.__workflow_builder.proxy
    proxy_service = services.get(proxy_name) or {}

    services[proxy_name] = { 
      **proxy_service,
      **{ 'command': command, 'hostname': f"{SERVICE_HOSTNAME}" },
    }