import os
import pdb

from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.lib.logger import Logger

from .app import App
from .constants import APP_NETWORK_ENV, CERTS_DIR_ENV, CONTEXT_DIR_ENV, SERVICE_NAME_ENV, USER_ID_ENV, WORKFLOW_NAME_ENV
from .env import Env
from .workflow_command import WorkflowCommand

LOG_ID = 'WorkflowRunCommand'

class WorkflowRunCommand(WorkflowCommand):
  def __init__(self, app: App, **kwargs):
    super().__init__(app, **kwargs)

    self.__current_working_dir = os.getcwd()
    self.__certs_dir_path = app.certs_dir_path
    self.__context_dir_path = app.context_dir_path
    self.__extra_compose_path = kwargs.get('extra_compose_path')
    self.__network = kwargs.get('network') or app.network

  @property
  def certs_dir_path(self):
    if not self.__certs_dir_path:
      data_dir = DataDir.instance()
      dir_path = os.path.join(data_dir.tmp_dir_path, 'certs')
      if not os.path.exists(dir_path):
          os.mkdir(dir_path)

    return self.__certs_dir_path

  @property
  def context_dir_path(self):
    if not self.__context_dir_path:
      data_dir = DataDir.instance()
      return os.path.dirname(data_dir.path) 

    return self.__context_dir_path

  @property
  def current_working_dir(self):
    return self.__current_working_dir

  @current_working_dir.setter
  def current_working_dir(self, v):
    self.__current_working_dir = v

  @property
  def extra_compose_path(self):
    return self.__extra_compose_path

  @property
  def network(self):
    return self.__network

  def create_network(self):
    return f"docker network create {self.network} 2> /dev/null"

  def up(self):
    if not os.path.exists(self.compose_path):
      return ''

    command = ['COMPOSE_IGNORE_ORPHANS=true', 'docker', 'compose']

    # Add docker compose file
    command.append(f"-f {os.path.relpath(self.compose_path, self.__current_working_dir)}")

    # Add custom docker compose file
    custom_services = self.custom_services
  
    if custom_services:
      uses_profile = False
      for service_name in custom_services:
        service = custom_services[service_name]
        profiles = service.get('profiles')
        if isinstance(profiles, list):
          if self.workflow_name in profiles:
            uses_profile = True
            break
      if not uses_profile:
        # TODO: looking into why warning does not print in docker
        Logger.instance(LOG_ID).error(f"Missing {self.workflow_name} profile in custom compose file")

      command.append(f"-f {os.path.relpath(self.custom_compose_path, self.__current_working_dir)}")

    if self.extra_compose_path:
      command.append(f"-f {os.path.relpath(self.extra_compose_path, self.__current_working_dir)}")

    command.append(f"--profile {self.workflow_name}") 
    command.append('up')
    command.append('-d')
    command.append('--build')

    self.write_env()

    return ' '.join(command)

  def down(self):
    if not os.path.exists(self.compose_path):
      return ''
  
    command = ['docker', 'compose']

    # Add docker compose file
    command.append(f"-f {os.path.relpath(self.compose_path, os.getcwd())}")

    # Add custom docker compose file
    if self.custom_services:
      command.append(f"-f {os.path.relpath(self.custom_compose_path, self.__current_working_dir)}")

    if self.extra_compose_path:
      command.append(f"-f {os.path.relpath(self.extra_compose_path, self.__current_working_dir)}")

    command.append(f"--profile {self.workflow_name}") 
    command.append('down')

    return ' '.join(command)

  def write_env(self):
    _config = {}
    _config[CERTS_DIR_ENV] = self.certs_dir_path
    _config[CONTEXT_DIR_ENV] = self.context_dir_path
    _config[SERVICE_NAME_ENV] = self.service_name
    _config[USER_ID_ENV] = os.getuid()
    _config[WORKFLOW_NAME_ENV] = self.workflow_name

    if self.network:
      _config[APP_NETWORK_ENV] = self.network

    env_vars = self.config(_config)
    env_path = self.workflow_env_path
    Env(env_path).write(env_vars)