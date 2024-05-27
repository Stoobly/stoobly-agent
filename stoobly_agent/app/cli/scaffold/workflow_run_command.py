import os

from stoobly_agent.config.data_dir import DataDir

from .constants import ENV_FILE
from .env import Env
from .workflow_command import WorkflowCommand

class WorkflowRunCommand(WorkflowCommand):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

    data_dir = DataDir.instance()

    if not kwargs['certs_dir_path']:
        kwargs['certs_dir_path'] = os.path.join(data_dir.tmp_dir_path, 'certs')
        if not os.path.exists(kwargs['certs_dir_path']):
            os.mkdir(kwargs['certs_dir_path'])

    if not kwargs['data_dir_path']:
        kwargs['data_dir_path'] = data_dir.path 

    self.__certs_dir_path = kwargs.get('certs_dir_path')
    self.__data_dir_path = kwargs.get('data_dir_path')
    self.__network = kwargs.get('network')

  @property
  def certs_dir_path(self):
    return self.__certs_dir_path or '/tmp'

  @property
  def data_dir_path(self):
    return self.__data_dir_path

  @property
  def network(self):
    return self.__network

  def build_with_docker(self):
    self.as_docker()

    command = ['docker-compose']

    command.append(f"-f {self.compose_path}")
    command.append(f"--profile {self.workflow_name}") 

    self.write_env()

    command.append('up')
    command.append('--build')
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