import os

from stoobly_agent.app.settings import Settings
from stoobly_agent.config.constants import env_vars
from stoobly_agent.lib.api.keys.project_key import InvalidProjectKey, ProjectKey

def is_remote(settings: Settings):
  return settings.cli.features.remote or not not os.environ.get(env_vars.FEATURE_REMOTE)

def is_local(settings: Settings):
  is_local = True

  if is_remote(settings):
    project_key = settings.proxy.intercept.project_key

    try:
      return ProjectKey(project_key).is_local
    except InvalidProjectKey:
      pass

  return is_local