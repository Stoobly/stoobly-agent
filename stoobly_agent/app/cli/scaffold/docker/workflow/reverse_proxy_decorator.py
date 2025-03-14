import os
import pdb

from urllib.parse import urlparse

from ...constants import SERVICE_HOSTNAME, SERVICE_PORT, SERVICE_PROXY_MODE, STOOBLY_CERTS_DIR
from .builder import WorkflowBuilder

class ReverseProxyDecorator():

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
      '--lifecycle-hooks-path', 'lifecycle_hooks.py',
      '--proxy-mode', SERVICE_PROXY_MODE,
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

    # Proxying forwards requests to the actual service
    # If the destination hostname is the same as the service's hostname, then
    # If we set the 'hostname' property, this will cause an "infinite loop"
    proxy_mode_toks = config.proxy_mode.split(':', 1)

    if len(proxy_mode_toks) > 1:
      directed = proxy_mode_toks[0] == 'reverse' or proxy_mode_toks[0] == 'upstream'
      if directed:
        spec = proxy_mode_toks[1]
        uri = urlparse(spec)
        if uri.hostname != self.service_builder.config.hostname:
          additional_properties['hostname'] = f"{SERVICE_HOSTNAME}"

    service = { 
      **proxy_service,
      **additional_properties,
    }

    services[proxy_name] = service 

