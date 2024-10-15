import os

from .app import App

class Service():

  def __init__(self, service_name: str, app: App):
    self.__app = app
    self.__service_name = service_name

  @property
  def app(self):
    return self.__app

  @property
  def dir_path(self):
    return os.path.join(self.app.namespace_path, self.service_name)

  @property
  def service_name(self):
    return self.__service_name

  @property
  def workflow_dir_path(self, workflow_name: str):
    return os.path.join(self.dir_path, workflow_name)