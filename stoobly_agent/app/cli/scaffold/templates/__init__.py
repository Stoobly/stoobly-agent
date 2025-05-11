import os
import pathlib

def __path():
  return os.path.join(pathlib.Path(__file__).parent.resolve())

def run_template_path():
  return os.path.join(__path(), 'run')