import pdb
import threading

from typing import TypedDict

from stoobly_agent.config.constants.statuses import REQUESTS_MODIFIED
from stoobly_agent.lib.api.agent_api import AgentApi
from stoobly_agent.lib.cache import Cache
from stoobly_agent.lib.logger import Logger

class Options(TypedDict):
  sync: bool

# Announce that a new request has been created
def publish_change(status: str, value: any, **options: Options):
  if options.get('sync'):
    return __publish_change_sync(status, value)

  from stoobly_agent.app.settings import Settings
  settings = Settings.instance()

  # If ui is not active, return
  if not settings.ui.active:
    return False

  ui_url = settings.ui.url

  if not ui_url:
    Logger.instance().warn('Settings.ui.url not configured')
    return False
  else:
    thread = threading.Thread(target=__put_status, args=(ui_url, status, value))
    thread.start()
    return True

def publish_requests_modified(value, **options: Options):
  return publish_change(REQUESTS_MODIFIED, value, **options)

def __publish_change_sync(status: str, value):
  cache = Cache.instance()
  cache.write(status, value)
  return True

def __put_status(ui_url, status, value):
    api: AgentApi = AgentApi(ui_url)
    api.update_status(status, value)