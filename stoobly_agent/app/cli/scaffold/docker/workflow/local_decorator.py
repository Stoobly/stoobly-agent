from ...local.workflow.builder import WorkflowBuilder

class LocalDecorator():

  def __init__(self, workflow_builder: WorkflowBuilder):
    self.__workflow_builder = workflow_builder

  @property
  def workflow_builder(self):
    return self.__workflow_builder

  @property
  def service_builder(self):
    return self.workflow_builder.service_builder

  def decorate(self):
    proxy_name = self.workflow_builder.proxy
    services = self.workflow_builder.services

    if not proxy_name in services:
      services[proxy_name] = {}

    if 'extra_hosts' not in services[proxy_name]:
      services[proxy_name]['extra_hosts'] = []

    services[proxy_name]['extra_hosts'].append('host.docker.internal:host-gateway')