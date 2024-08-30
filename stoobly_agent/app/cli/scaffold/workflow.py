import os

from .app import App

class Workflow():

  def __init__(self, workflow_name: str, app: App):
    self.__app = app
    self.__workflow_name = workflow_name

  @property
  def app(self):
    return self.__app

  @property
  def workflow_name(self):
    return self.__workflow_name

  @property
  def service(self):
    return self._service

  @service.setter
  def service(self, v):
    self._service = v

  @property
  def services(self):
    services_dir = os.path.join(self.app.scaffold_dir_path, self.app.namespace)

    services = []
    for filename in os.listdir(services_dir):
      path = os.path.join(services_dir, filename)
      if not os.path.isdir(path):
        continue
      
      services.append(filename)

    return services
