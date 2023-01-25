import pdb
from stoobly_agent.app.settings import Settings
from stoobly_agent.lib.api.keys.project_key import LOCAL_PROJECT_ID, ProjectKey

class Model():
  def __init__(self, settings: Settings):
    self.settings = settings

    project_key = ProjectKey(settings.proxy.intercept.project_key)

    if int(project_key.id) == LOCAL_PROJECT_ID:
      self.as_local()
    else:
      self.as_remote()

  # Override
  def as_local(self):
    pass

  # Override
  def as_remote(self):
    pass