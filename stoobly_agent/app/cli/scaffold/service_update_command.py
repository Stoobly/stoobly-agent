import os
import pdb

from stoobly_agent.app.cli.scaffold.app import App
from stoobly_agent.app.cli.scaffold.constants import (
  WORKFLOW_MOCK_TYPE,
  WORKFLOW_RECORD_TYPE,
  WORKFLOW_TEST_TYPE,
)
from stoobly_agent.app.cli.scaffold.service import Service
from stoobly_agent.app.cli.scaffold.service_command import ServiceCommand
from stoobly_agent.app.cli.scaffold.service_create_command import ServiceCreateCommand
from stoobly_agent.app.cli.scaffold.service_config import ServiceConfig
from stoobly_agent.lib.logger import Logger


LOG_ID = 'ServiceUpdateCommand'

class ServiceUpdateCommand(ServiceCommand):

  def __init__(self, app: App, **kwargs):
    super().__init__(app, **kwargs)

  def rename(self, new_service_name: str) -> Service:
    service = self.__rename_service_dir(self.service_path, new_service_name)

    self.service_config = ServiceConfig(service.dir_path)
    self.service_name = new_service_name

    self.__update_internal_container_specs(service.dir_path, self.service_name, new_service_name)

    return service

  def __rename_service_dir(self, dir_path: str, new_name: str) -> Service:
    new_dir_path = os.path.join(self.app.scaffold_namespace_path, new_name)
    os.rename(dir_path, new_dir_path)

    service = Service(new_name, self.app)
    return service

  def __update_internal_container_specs(self, service_path: str, old_service_name: str, new_service_name: str):
    # TODO: update to include custom workflows
    CORE_WORKFLOWS = [WORKFLOW_MOCK_TYPE, WORKFLOW_RECORD_TYPE, WORKFLOW_TEST_TYPE]
    workflows = CORE_WORKFLOWS

    kwargs = {}
    kwargs['app_dir_path'] = self.app.dir_path
    kwargs['service_name'] = self.service_name
    kwargs['workflow'] = CORE_WORKFLOWS
    command = ServiceCreateCommand(self.app, **kwargs)
    command.build()
