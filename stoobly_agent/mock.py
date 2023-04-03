import inspect
import os
import pdb
import subprocess

from typing import TypedDict

from stoobly_agent import COMMAND
from stoobly_agent.app.models.adapters.raw_http_response_adapter import RawHttpResponseAdapter
from stoobly_agent.config.constants.env_vars import ENV
from stoobly_agent.app.settings.constants.mode import TEST

class MockOptions(TypedDict):
  data: str
  headers: dict
  method: str
  project_key: str
  scenario_key: str

class Mock():

  @classmethod
  def get(cls, url: str, **options: MockOptions):
    return cls.mock(url, **{
      **options,
      'method': 'GET',
    }) 

  @classmethod
  def post(cls, url: str, **options: MockOptions):
    return cls.mock(url, **{
      **options,
      'method': 'POST',
    })

  @classmethod
  def put(cls, url: str, **options: MockOptions):
    return cls.mock(url, **{
      **options,
      'method': 'PUT',
    })

  @classmethod
  def delete(cls, url: str, **options: MockOptions):
    return cls.mock(url, **{
      **options,
      'method': 'DELETE',
    })

  @staticmethod
  def mock(url: str, **options: MockOptions):
    command = [COMMAND, 'mock', '--format', 'raw']

    if isinstance(options.get('data'), str):
      data_option = f"--data {options['data']}"
      command.append(data_option)

    if isinstance(options.get('headers'), dict):
      options = []
      for k, v in options['headers'].items:
        options.append('--header')
        options.append(f"{k}: {v}")

      if len(options) > 0:
        command.append(' '.join(options))

    if isinstance(options.get('project_key'), str):
      command.append('--project_key')
      command.append(options['project_key'])

    if isinstance(options.get('method'), str):
      command.append('--request')
      command.append(f"{options['method']}")      

    if isinstance(options.get('scenario_key'), str):
      command.append('--scenario_key')
      command.append(options['scenario_key'])

    command.append(url)

    # We do not want the child process to run in test mode
    if os.environ.get(ENV) == TEST:
      del os.environ[ENV]

    # Change dir to caller file's directory
    dir_path = inspect.stack()[2].filename # Path of calling method
    parent_dir = os.path.dirname(dir_path)
    if len(parent_dir) > 0:
      os.chdir(parent_dir)

    completed_process = subprocess.run(command, check=True, stdout=subprocess.PIPE)

    if completed_process.returncode == 0:
      adapter = RawHttpResponseAdapter(completed_process.stdout) 
      response = adapter.to_response()
      return response