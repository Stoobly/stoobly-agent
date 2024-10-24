import os
import pdb
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
    services_dir = os.path.join(self.app.scaffold_dir_path, self.app.namespace)

    services = []
    for filename in os.listdir(services_dir):
      path = os.path.join(services_dir, filename)
      if not os.path.isdir(path):
        continue
      
      services.append(filename)

    return services

  # TODO: merge into 1 services property

  # Returns services that run in this specific workflow
  @property
  def services_ran(self) -> List[str]:
    services_dir = os.path.join(self.app.scaffold_dir_path, self.app.namespace)

    services = []
    for filename in os.listdir(services_dir):
      path = os.path.join(services_dir, filename)
      if not os.path.isdir(path):
        continue

      for sub_path in os.scandir(path):
        if os.path.isdir(sub_path):
          if sub_path.name == self.workflow_name:
            services.append(filename)

    return services

