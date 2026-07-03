import json
import os
import pdb
import shutil

from io import BytesIO
from pathlib import Path

from stoobly_agent import VERSION
from stoobly_agent.config.constants.env_vars import ENV
from stoobly_agent.app.settings.constants.mode import TEST

from stoobly_agent.app.settings import Settings
from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.lib.orm import ORM
from stoobly_agent.lib.orm.migrate_service import migrate

DETERMINISTIC_GET_REQUEST_URL = 'https://dog.ceo/api/breeds/list/all'
NON_DETERMINISTIC_GET_REQUEST_URL = 'https://www.google.com'

with open(Path(__file__).parent / 'mock_data' / 'deterministic_get_request_response.json') as fp:
  DETERMINISTIC_GET_REQUEST_RESPONSE = json.load(fp)

DETERMINISTIC_GET_REQUEST_RESPONSE_BODY = json.dumps(
  DETERMINISTIC_GET_REQUEST_RESPONSE,
  separators=(',', ':'),
).encode()

def make_deterministic_get_request_response():
  import requests
  from urllib3 import HTTPResponse

  headers = {'Content-Type': 'application/json'}
  res = requests.Response()
  res.status_code = 200
  res.headers = headers
  res._content = DETERMINISTIC_GET_REQUEST_RESPONSE_BODY
  res.url = DETERMINISTIC_GET_REQUEST_URL
  res.raw = HTTPResponse(
    body=BytesIO(DETERMINISTIC_GET_REQUEST_RESPONSE_BODY),
    decode_content=False,
    headers=headers,
    preload_content=False,
  )
  return res

def reset(dir_name = 'stoobly-agent-test'):
  os.environ[ENV] = TEST

  # Create a temporary folder using tmpfile
  temp_dir = os.path.join('/tmp', dir_name)
  if os.path.exists(temp_dir):
    shutil.rmtree(temp_dir)
  os.makedirs(temp_dir, exist_ok=True)
  os.chdir(temp_dir)

  data_dir: DataDir = DataDir.instance()
  data_dir.create()

  orm = ORM.instance()
  orm._db = None
  ORM.configure()
  migrate(VERSION)

  settings: Settings = Settings.instance()
  settings.reset_and_load()

  return settings

def assert_orm_request_equivalent(request_1, request_2):
  assert request_1.latency == request_2.latency
  assert request_1.method == request_2.method
  assert request_1.raw == request_2.raw
  assert request_1.status == request_2.status
  assert request_1.url == request_2.url

reset()
