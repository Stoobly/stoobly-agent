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
    return self.app.service_paths

  def service_paths_from_services(self, services: List[str]):
    app_namespace_path = self.app.namespace_path
    return list(map(lambda service: os.path.join(app_namespace_path, service), services))
