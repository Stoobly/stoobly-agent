import pdb
import threading

from stoobly_agent.app.settings import Settings
from stoobly_agent.config.constants.statuses import REQUESTS_MODIFIED, SETTINGS_MODIFIED
from stoobly_agent.lib.api.agent_api import AgentApi
from stoobly_agent.lib.cache import Cache
from stoobly_agent.lib.logger import Logger

LOG_ID = 'PublishChange'

def publish_settings_modified(value):
  return __publish_change_sync(SETTINGS_MODIFIED, value)
 
def publish_requests_modified(value):
  settings: Settings = Settings.instance()

  # If not headless...
  if settings.ui.active:
    return __publish_change_sync(REQUESTS_MODIFIED, value)

  ui_url = settings.ui.url
  if not ui_url:
    return False

  return __publish_change_async(REQUESTS_MODIFIED, value, ui_url)

def __publish_change_async(status, value, ui_url: str):
  thread = threading.Thread(target=__put_status, args=(ui_url, status, value))
  thread.start()
  return True

def __publish_change_sync(status: str, value):
  cache = Cache.instance()
  cache.write(status, value)
  return True

def __put_status(ui_url, status, value):
    api: AgentApi = AgentApi(ui_url)
    try:
      api.update_status(status, value)
    except Exception as e:
      # Lazy import for runtime exception handling
      import requests
      if isinstance(e, requests.exceptions.ConnectionError):
        Logger.instance(LOG_ID).error(f"could not connect to {ui_url}")
      else:
        raise