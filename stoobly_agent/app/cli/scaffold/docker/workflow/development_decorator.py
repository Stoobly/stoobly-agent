from ...constants import SERVICE_DNS

from .builder import WorkflowBuilder

class DevelopmentDecorator():

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
    proxy_name = self.workflow_builder.proxy
    services = self.workflow_builder.services

    # If we are reverse proxying to potentially an external host,
    # Docker's embedded DNS will use the host's /etc/host file as part of the resolution process
    # This can lead the hostname to resolve to localhost instead of the service's actual IP address
    if not config.detached:
      if not proxy_name in services:
        services[proxy_name] = {}

      services[proxy_name]['dns'] = SERVICE_DNS