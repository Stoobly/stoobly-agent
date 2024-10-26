import pdb

from .builder import WorkflowBuilder

class BuildDecorator():

  def __init__(self, workflow_builder: WorkflowBuilder):
    self.__workflow_builder = workflow_builder

  @property
  def workflow_builder(self):
    return self.__workflow_builder

  def decorate(self):
    service_builder = self.__workflow_builder.service_builder

    services = self.workflow_builder.services
    app_name = self.workflow_builder.app
    app_service = services.get(app_name) or {}

    services[app_name] = { 
      **app_service,
      **{ 
          'extends': service_builder.build_extends_proxy_base(self.workflow_builder.dir_path),
          'hostname': service_builder.config.hostname,
          'profiles': self.workflow_builder.profiles,
        } 
    }