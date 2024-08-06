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

  def services(self, namespace: str):
    services_dir = os.path.join(self.app.path, namespace)

    services = []
    for filename in os.listdir(services_dir):
      path = os.path.join(services_dir, filename)
      if not os.path.isdir(path):
        continue
      
      services.append(filename)

    return services
