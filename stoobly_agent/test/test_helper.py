import os
import pdb
import shutil
import tempfile

from stoobly_agent import VERSION
from stoobly_agent.config.constants.env_vars import ENV
from stoobly_agent.app.settings.constants.mode import TEST

from stoobly_agent.app.settings import Settings
from stoobly_agent.config.data_dir import DATA_DIR_NAME, DataDir
from stoobly_agent.lib.orm import ORM
from stoobly_agent.lib.orm.migrate_service import migrate

DETERMINISTIC_GET_REQUEST_URL = 'https://dog.ceo/api/breeds/list/all'
NON_DETERMINISTIC_GET_REQUEST_URL = 'https://www.google.com'

def reset(dir_name = 'stoobly-agent-test'):
  os.environ[ENV] = TEST

  # Create a temporary folder using tmpfile
  temp_dir = os.path.join('/tmp', dir_name)
  if os.path.exists(temp_dir):
    shutil.rmtree(temp_dir)
  os.makedirs(temp_dir)
  os.chdir(temp_dir)

  data_dir: DataDir = DataDir.instance()
  data_dir.create()

  ORM.instance().initialize_db()
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
