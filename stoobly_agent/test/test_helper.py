import os
import pdb

from stoobly_agent import VERSION
from stoobly_agent.config.constants.env_vars import ENV
from stoobly_agent.app.settings.constants.mode import TEST

os.environ[ENV] = TEST

from stoobly_agent.lib.orm.migrate_service import migrate

migrate(VERSION)