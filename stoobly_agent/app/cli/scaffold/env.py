import os

from .constants import ENV_FILE

DELIMITTER = "\n"

class Env():

  def __init__(self, path: str):
    self.__path = path

  @property
  def path(self):
    return self.__path

  def read(self, source: str = None):
    if not source:
      source = self.path

    env_vars = {}

    if os.path.exists(source):
      with open(source, 'r') as fp:
        contents = fp.read()

        rows = contents.split(DELIMITTER)
        for row in rows:
          el = row.split("=")
          if len(el) != 2:
            continue
          env_vars[el[0]] = el[1]

    return env_vars

  # Priority: env_vars, source_env_vars, dest_env_vars
  def merge(self, defaults_path: str, env_vars: dict = {}):
    source_env_vars = self.read()
    dest_env_vars = self.read(defaults_path)
    dest_env_vars.update(source_env_vars)
    dest_env_vars.update(env_vars)
    return env_vars

  def write(self, env_vars: dict):
    env_file_path = os.path.join(self.path)
    with open(env_file_path, 'w') as fp:
      contents = []
      for var in env_vars:
          contents.append(f"{var}={env_vars[var]}")
      fp.write(DELIMITTER.join(contents))