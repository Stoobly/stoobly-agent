import os
import pdb

from ...constants import (
  SERVICE_HOSTNAME, SERVICE_PORT, STOOBLY_CERTS_DIR,
)
from ...local.workflow.builder import WorkflowBuilder
from .command_decorator import CommandDecorator

class MockDecorator(CommandDecorator):

  def __init__(self, workflow_builder: WorkflowBuilder):
    super().__init__(workflow_builder)

  @property
  def service_builder(self):
    return self.workflow_builder.service_builder

  def decorate(self):
    config = self.service_builder.config

    command = [
      '--headless',
      '--intercept',
      '--lifecycle-hooks-path', 'lifecycle_hooks.py',
      '--proxy-mode', self.proxy_mode,
      '--proxy-port', f"{SERVICE_PORT}",
      '--public-directory-path', 'public',
      '--response-fixtures-path', 'fixtures.yml',
      '--ssl-insecure'
    ]

    if config.scheme == 'https':
      command.append('--certs')
      command.append(os.path.join(STOOBLY_CERTS_DIR, f"{SERVICE_HOSTNAME}-joined.pem"))

    command.append('--request-log-enable')

    services = self.workflow_builder.services
    proxy_name = self.workflow_builder.proxy
    proxy_service = services.get(proxy_name) or {}

    services[proxy_name] = { 
      **proxy_service,
      **{ 'command': command },
    }
