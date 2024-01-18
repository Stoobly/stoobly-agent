import pdb
import requests

from stoobly_agent.app.settings import Settings
from stoobly_agent.lib.api.keys.project_key import LOCAL_PROJECT_ID, ProjectKey
from stoobly_agent.lib.logger import Logger

class Model():
  def __init__(self, settings: Settings, **options):
    self.adapter = None
    self.is_local = False
    self.settings = settings

    if not settings.cli.features.remote:
      self.as_local()
    else:
      if 'access_token' in options:
        if options.get('access_token'):
          self.as_remote()
        else:
          self.as_local() 
      else:
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

  def handle_request_error(self, e: requests.exceptions.RequestException):
      response: requests.Response = e.response

      if response:
        Logger.instance().error(f"{response.status_code} {response.content}")
        return response.content, response.status_code
      else:
        return 'Unknown Error', 0