import os
import pdb

from stoobly_agent.config.data_dir import DataDir

from .env import Env
from .workflow_command import WorkflowCommand

class WorkflowRunCommand(WorkflowCommand):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

    self.__certs_dir_path = kwargs.get('certs_dir_path')
    self.__data_dir_path = kwargs.get('data_dir_path')
    self.__extra_compose_path = kwargs.get('extra_compose_path')
    self.__network = kwargs.get('network')

  @property
  def certs_dir_path(self):
    if not self.__certs_dir_path:
      data_dir = DataDir.instance()
      dir_path = os.path.join(data_dir.tmp_dir_path, 'certs')
      if not os.path.exists(dir_path):
          os.mkdir(dir_path)

    return self.__certs_dir_path

  @property
  def data_dir_path(self):
    if not self.__data_dir_path:
      data_dir = DataDir.instance()
      return os.path.dirname(data_dir.path) 

    return self.__data_dir_path

  @property
  def extra_compose_path(self):
    return self.__extra_compose_path

  @property
  def network(self):
    return self.__network

  def up(self):
    command = ['docker', 'compose']

    # Add docker compose file
    command.append(f"-f {self.compose_path}")

    # Add custom docker compose file
    if self.custom_services:
      command.append(f"-f {self.custom_compose_path}")

    command.append(f"--profile {self.workflow_name}") 
    command.append('up')
    command.append('-d')
    command.append('--build')

    self.write_env()

    return ' '.join(command)

  def down(self):
    command = ['docker', 'compose']

    # Add docker compose file
    command.append(f"-f {self.compose_path}")

    # Add custom docker compose file
    if self.custom_services:
      command.append(f"-f {self.custom_compose_path}")

    command.append(f"--profile {self.workflow_name}") 
    command.append('down')

    return ' '.join(command)

  def write_env(self):
    _config = {
      'CERTS_DIR': self.certs_dir_path,
      'DATA_DIR': self.data_dir_path,
      'USER_ID': os.getuid(),
    }

    if self.network:
      _config['NETWORK'] = self.network

    env_vars = self.config(_config)
    env_path = self.workflow_env_path
    Env(env_path).write(env_vars)