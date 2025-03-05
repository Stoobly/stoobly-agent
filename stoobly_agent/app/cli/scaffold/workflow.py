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
    return list(map(lambda path: os.path.basename(path), self.service_paths))

  @property
  def service_paths(self):
    all_service_paths = self.app.service_paths
    return list(filter(lambda path: os.path.exists(os.path.join(path, self.workflow_name)), all_service_paths))

  # TODO: merge into 1 services property

  # Returns services that run in this specific workflow
  @property
  def services_ran(self) -> List[str]:
    services_dir = os.path.join(self.app.data_dir_path, self.app.scaffold_namespace)

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

  def service_paths_from_services(self, services: List[str]):
    scaffold_namespace_path = self.app.scaffold_namespace_path
    return list(map(lambda service: os.path.join(scaffold_namespace_path, service), services))
