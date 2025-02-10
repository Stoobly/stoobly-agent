from .config import Config
from .constants import ENV_FILE
from .env import Env

class WorkflowEnv(Config):

  def __init__(self, dir: str):
    super().__init__(dir, ENV_FILE)

    self.__env_vars = {}

  def get(self, key):
    return self.__env_vars.get(key)

  def load(self):
    self.__env_vars = self.read()

  def write(self, env_vars: dict):
    Env(self.path).write(env_vars)
    self.__env_vars = env_vars