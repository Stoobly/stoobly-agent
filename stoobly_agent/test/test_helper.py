import os
import pdb

from stoobly_agent.config.constants.env_vars import ENV

os.environ[ENV] = 'test'

from stoobly_agent.lib.orm.migrate_service import migrate

migrate()

def value_not_match_error(v1, v2):
  return f"Got {v1}, expected {v2}"