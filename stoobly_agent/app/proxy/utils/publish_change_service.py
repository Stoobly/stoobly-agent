import pdb
import threading

from stoobly_agent.app.settings import Settings
from stoobly_agent.lib.api.agent_api import AgentApi
from stoobly_agent.lib.api.keys import ProjectKey
from stoobly_agent.lib.logger import Logger

# Announce that a new request has been created
def publish_change(status: str):
  settings = Settings.instance()

  # If ui is not active, return
  if not settings.ui.active:
    return False

  ui_url = settings.ui.url

  if not ui_url:
    Logger.instance().warn('Settings.ui.url not configured')
    return False
  else:
    project_key = ProjectKey(settings.proxy.intercept.project_key)
    thread = threading.Thread(target=__put_status, args=(ui_url, status, project_key.id))
    thread.start()
    return True

def __put_status(ui_url, status, project_id):
    api: AgentApi = AgentApi(ui_url)
    api.update_status(status, project_id)