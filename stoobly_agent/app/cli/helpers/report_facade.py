import requests

from stoobly_agent.lib.api.reports_resource import ReportsResource
from stoobly_agent.app.settings import Settings

class ReportFacade():

  def __init__(self, settings: Settings):
    self.settings = settings

  def create(self, project_key: str, name: str, description: str = ''):
    api = ReportsResource(self.settings.remote.api_url, self.settings.remote.api_key)

    res: requests.Response = api.from_project_key(
      project_key, 
      lambda project_id: api.create(
        project_id, {
          'description': description,
          'name': name,
        }
      )
    )

    if not res.ok:
      raise AssertionError(res.content)

    return res.json()

  def index(self, project_key: str, kwargs: dict):
    api = ReportsResource(self.settings.remote.api_url, self.settings.remote.api_key)

    res: requests.Response = api.from_project_key(
      project_key, 
      lambda project_id: api.index(
        project_id, kwargs
      )
    )

    if not res.ok:
      raise AssertionError(res.content)

    return res.json()
