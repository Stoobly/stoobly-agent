import os
import pdb

from ...constants import SERVICE_HOSTNAME, SERVICE_PORT, SERVICE_PROXY_MODE, STOOBLY_CERTS_DIR
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
      '--headless',
      '--intercept',
      '--lifecycle-hooks-path', 'lifecycle_hooks.py',
      '--proxy-mode', SERVICE_PROXY_MODE,
      '--proxy-port', f"{SERVICE_PORT}",
      '--public-directory-path', 'public',
      '--response-fixtures-path', 'fixtures.yml',
      '--ssl-insecure'
    ]

    if config.scheme == 'https':
      command.append('--certs')
      command.append(os.path.join(STOOBLY_CERTS_DIR, f"{SERVICE_HOSTNAME}-joined.pem"))

    services = self.__workflow_builder.services
    proxy_name = self.__workflow_builder.proxy
    proxy_service = services.get(proxy_name) or {}

    services[proxy_name] = { 
      **proxy_service,
      **{ 'command': command, 'hostname': f"{SERVICE_HOSTNAME}" },
    }
