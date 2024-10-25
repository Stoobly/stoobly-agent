import os

from typing import List

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
    return list(map(lambda path: os.path.basename(path), self.service_paths))

  @property
  def service_paths(self):
    services_dir = os.path.join(self.app.scaffold_dir_path, self.app.namespace)

    services = []
    for filename in os.listdir(services_dir):
      path = os.path.join(services_dir, filename)
      if not os.path.isdir(path):
        continue
      
      services.append(path)

    return services

  def service_paths_from_services(self, services: List[str]):
    app_namespace_path = self.app.namespace_path
    return list(map(lambda service: os.path.join(app_namespace_path, service), services))
