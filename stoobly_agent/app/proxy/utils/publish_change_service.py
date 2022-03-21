from stoobly_agent.lib.api.agent_api import AgentApi
from stoobly_agent.lib.logger import Logger
from stoobly_agent.app.settings import Settings

# Announce that a new request has been created
def publish_change(status: str):
  settings = Settings.instance()

  if not settings.is_headless() or settings.remote_enabled:
    return False

  agent_url = settings.agent_url

  if not agent_url:
    Logger.instance().warn('Settings.agent_url not configured')
    return False
  else:
    active_mode_settings = settings.active_mode_settings
    api: AgentApi = AgentApi(agent_url)
    api.update_status(status, active_mode_settings.get('project_key'))
    return True