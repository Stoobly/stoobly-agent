import urllib

from ..logger import Logger
from .interfaces import ProjectCreateParams, ProjectsIndexQueryParams, ProjectsIndexResponse
from .stoobly_api import StooblyApi

class ProjectsResource(StooblyApi):
  PROJECTS_ENDPOINT = 'projects'

  def create(self, **params: ProjectCreateParams):
    url = f"{self.service_url}/{self.PROJECTS_ENDPOINT}"

    return self.post(url, headers=self.default_headers, data=params)

  def index(self, **query_params: ProjectsIndexQueryParams) -> ProjectsIndexResponse:
    url = f"{self.service_url}/{self.PROJECTS_ENDPOINT}"

    Logger.instance().debug(f"{self.LOG_ID}.request_response:{url}?{urllib.parse.urlencode(query_params)}")

    return self.get(url, headers=self.default_headers, params=query_params)

