from stoobly_agent.app.settings import Settings
from stoobly_agent.lib.api.agent_api import AgentApi
from stoobly_agent.lib.api.keys import ProjectKey
from stoobly_agent.lib.logger import Logger

# Announce that a new request has been created
def publish_change(status: str):
  settings = Settings.instance()

  # If ui is not active or if remote is not enabled, return
  if not settings.ui.active or not settings.cli.features.remote:
    return False

  ui_url = settings.ui.url

  if not ui_url:
    Logger.instance().warn('Settings.ui.url not configured')
    return False
  else:
    api: AgentApi = AgentApi(ui_url)
    project_key = ProjectKey(settings.proxy.intercept.project_key)
    api.update_status(status, project_key.id)
    return True