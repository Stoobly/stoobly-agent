import os
import pdb

from stoobly_agent.config.data_dir import DataDir

from .app import App
from .constants import APP_NETWORK_ENV, CERTS_DIR_ENV, CONTEXT_DIR_ENV, USER_ID_ENV
from .env import Env
from .workflow_command import WorkflowCommand

class WorkflowRunCommand(WorkflowCommand):
  def __init__(self, app: App, **kwargs):
    super().__init__(app, **kwargs)

    self.__current_working_dir = os.getcwd()
    self.__certs_dir_path = app.certs_dir_path
    self.__context_dir_path = app.context_dir_path
    self.__extra_compose_path = kwargs.get('extra_compose_path')
    self.__network = app.network

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

  def up(self):
    if not os.path.exists(self.compose_path):
      return ''

    command = ['docker', 'compose']

    # Add docker compose file
    command.append(f"-f {os.path.relpath(self.compose_path, self.__current_working_dir)}")

    # Add custom docker compose file
    if self.custom_services:
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
    _config[USER_ID_ENV] = os.getuid()

    if self.network:
      _config[APP_NETWORK_ENV] = self.network

    env_vars = self.config(_config)
    env_path = self.workflow_env_path
    Env(env_path).write(env_vars)