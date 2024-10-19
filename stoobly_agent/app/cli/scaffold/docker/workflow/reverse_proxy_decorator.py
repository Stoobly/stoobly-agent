import pdb

from ...constants import SERVICE_DNS, SERVICE_HOSTNAME, SERVICE_PORT
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
      '--certs', f"../{SERVICE_HOSTNAME}-joined.pem",
      '--headless',
      '--lifecycle-hooks-path', 'lifecycle_hooks.py',
      '--proxy-mode', config.proxy_mode,
      '--proxy-port', f"{SERVICE_PORT}",
      '--ssl-insecure'
    ]

    services = self.workflow_builder.services
    proxy_name = self.workflow_builder.proxy
    proxy_service = services.get(proxy_name) or {}

    # proxying forwards requests to the actual service
    # If we set the 'hostname' property, this will cause an "infinite loop"

    service = { 
      **proxy_service,
      **{ 'command': command },
    }

    # If we are reverse proxying to potentially an external host,
    # Docker's embedded DNS will use the host's /etc/host file as part of the resolution process
    # This can lead the hostname to resolve to localhost instead of the service's actual IP address
    if config.dns and not config.detached:
      service['dns'] = SERVICE_DNS

    services[proxy_name] = service 


