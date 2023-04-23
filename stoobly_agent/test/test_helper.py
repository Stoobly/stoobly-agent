import os
import pdb

from stoobly_agent import VERSION
from stoobly_agent.config.constants.env_vars import ENV
from stoobly_agent.app.settings.constants.mode import TEST

from stoobly_agent.app.settings import Settings
from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.lib.orm import ORM
from stoobly_agent.lib.orm.migrate_service import migrate

DETERMINISTIC_GET_REQUEST_URL = 'https://dog.ceo/api/breeds/list/all'
NON_DETERMINISTIC_GET_REQUEST_URL = 'https://www.google.com'

def reset():
  os.environ[ENV] = TEST

  DataDir.instance().remove() # Clean data dir for testing

  ORM.instance().initialize_db()
  migrate(VERSION)

  Settings.instance().reset_and_load()

  return Settings.instance()

reset()