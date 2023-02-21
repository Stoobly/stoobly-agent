import pdb
import subprocess

from typing import TypedDict

from stoobly_agent import COMMAND
from stoobly_agent.app.models.adapters.raw_http_response_adapter import RawHttpResponseAdapter

class MockOptions(TypedDict):
  data: str
  headers: dict
  method: str

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
    command = [COMMAND, 'request', 'mock', '--format', 'raw']

    if isinstance(options.get('method'), str):
      command.append('--request')
      command.append(f"{options.get('method')}")      

    if isinstance(options.get('data'), str):
      data_option = f"--data {options.get('data')}"
      command.append(data_option)

    if isinstance(options.get('headers'), dict):
      options = []
      for k, v in options.get('headers').items:
        options.append('--header')
        options.append(f"{k}: {v}")

      if len(options) > 0:
        command.append(' '.join(options))

    command.append(url)

    completed_process = subprocess.run(command, check=True, stdout=subprocess.PIPE)

    if completed_process.returncode == 0:
      adapter = RawHttpResponseAdapter(completed_process.stdout) 
      response = adapter.to_response()
      return response