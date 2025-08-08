import os

from dotenv import dotenv_values

from .config import Config
from .constants import DOTENV_FILE
from .env import Env

class WorkflowEnv(Config):

  def __init__(self, dir: str):
    super().__init__(dir, DOTENV_FILE)

    self.__env_vars = {}

  def get(self, key):
    return self.__env_vars.get(key)

  def load(self):
    self.__env_vars = self.read()

  def write(self, env_vars: dict, dotenv_path: str = None):
    if dotenv_path and os.path.exists(dotenv_path):
      env_vars = { **env_vars, **dotenv_values(dotenv_path) }

    Env(self.path).write(env_vars)
    self.__env_vars = env_vars