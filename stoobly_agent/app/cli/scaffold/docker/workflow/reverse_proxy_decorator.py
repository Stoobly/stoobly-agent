import os
import pdb

from urllib.parse import urlparse

from ...constants import SERVICE_HOSTNAME, SERVICE_PORT, STOOBLY_CERTS_DIR
from ...local.workflow.builder import WorkflowBuilder
from .command_decorator import CommandDecorator

class ReverseProxyDecorator(CommandDecorator):

  def __init__(self, workflow_builder: WorkflowBuilder):
    super().__init__(workflow_builder)

  @property
  def service_builder(self):
    return self.workflow_builder.service_builder

  def decorate(self):
    config = self.service_builder.config

    command = [
      '--headless',
      '--lifecycle-hooks-path', 'lifecycle_hooks.py',
      '--proxy-mode', self.proxy_mode,
      '--proxy-port', f"{SERVICE_PORT}",
      '--ssl-insecure'
    ]

    if config.scheme == 'https':
      command.append('--certs')
      command.append(os.path.join(STOOBLY_CERTS_DIR, f"{SERVICE_HOSTNAME}-joined.pem"))

    services = self.workflow_builder.services
    proxy_name = self.workflow_builder.proxy
    proxy_service = services.get(proxy_name) or {}

    additional_properties = { 'command': command }

    service = { 
      **proxy_service,
      **additional_properties,
    }

    services[proxy_name] = service 

