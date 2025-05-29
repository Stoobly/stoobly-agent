import os
import pdb

from stoobly_agent.app.cli.scaffold.app import App
from stoobly_agent.app.cli.scaffold.constants import (
  COMPOSE_TEMPLATE,
  WORKFLOW_MOCK_TYPE,
  WORKFLOW_RECORD_TYPE,
  WORKFLOW_TEST_TYPE,
)
from stoobly_agent.app.cli.scaffold.docker.constants import DOCKER_COMPOSE_BASE
from stoobly_agent.app.cli.scaffold.service import Service
from stoobly_agent.app.cli.scaffold.service_command import ServiceCommand
from stoobly_agent.app.cli.scaffold.service_workflow import ServiceWorkflow
from stoobly_agent.lib.logger import Logger


LOG_ID = 'ServiceUpdateCommand'

class ServiceUpdateCommand(ServiceCommand):

  def __init__(self, app: App, **kwargs):
    super().__init__(app, **kwargs)

  def rename(self, new_service_name: str) -> Service:
    service = self.__rename_service_dir(self.service_path, new_service_name)
    self.__update_internal_container_specs(service.dir_path, self.service_name, new_service_name)
    return service

  def __rename_service_dir(self, dir_path: str, new_name: str) -> Service:
    new_dir_path = os.path.join(self.app.scaffold_namespace_path, new_name)
    os.rename(dir_path, new_dir_path)

    service = Service(new_name, self.app)
    return service

  def __update_internal_container_specs(self, service_path: str, old_service_name: str, new_service_name: str):
    CORE_WORKFLOWS = [WORKFLOW_MOCK_TYPE, WORKFLOW_RECORD_TYPE, WORKFLOW_TEST_TYPE]
    workflows = CORE_WORKFLOWS

    compose_file_base = os.path.join(service_path, DOCKER_COMPOSE_BASE)
    self.__rename_service_compose_inplace(compose_file_base, old_service_name, new_service_name)

    for workflow in workflows:
      service_workflow = ServiceWorkflow(new_service_name, workflow, self.app)
      compose_file = os.path.join(service_workflow.path, COMPOSE_TEMPLATE.format(workflow=workflow))

      self.__rename_service_compose_inplace(compose_file, old_service_name, new_service_name)

  # Based on: https://stackoverflow.com/a/17548459
  def __rename_service_compose_inplace(self, filename: str, old_string: str, new_string: str) -> None:
    # Safely read the input filename using 'with'
    with open(filename) as f:
      s = f.read()
      if old_string not in s:
        Logger.instance(LOG_ID).error('"{old_string}" not found in {filename}.'.format(**locals()))
        return

    # Safely write the changed content, if found in the file
    with open(filename, 'w') as f:
      Logger.instance(LOG_ID).debug('Changing "{old_string}" to "{new_string}" in {filename}'.format(**locals()))
      s = s.replace(old_string, new_string)
      f.write(s)
