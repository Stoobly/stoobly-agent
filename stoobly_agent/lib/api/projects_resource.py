import requests
import urllib
import pdb

from typing import TypedDict
from ..logger import Logger
from .interfaces import ProjectCreateParams, ProjectsIndexQueryParams
from .stoobly_api import StooblyApi

class ProjectsResource(StooblyApi):
  PROJECTS_ENDPOINT = 'projects'

  def create(self, **params: ProjectCreateParams):
    url = f"{self.service_url}/{self.PROJECTS_ENDPOINT}"

    Logger.instance().debug(f"{self.LOG_ID}.request_response:{url}?{urllib.parse.urlencode(params)}")

    return self.post(url, headers=self.default_headers, json=params)

  def index(self, **query_params: ProjectsIndexQueryParams) -> requests.Response:
    url = f"{self.service_url}/{self.PROJECTS_ENDPOINT}"

    Logger.instance().debug(f"{self.LOG_ID}.request_response:{url}?{urllib.parse.urlencode(query_params)}")

    return self.get(url, headers=self.default_headers, params=query_params)

  def show(self, project_id: int, **query_params) -> requests.Response:
    url = f"{self.service_url}/{self.PROJECTS_ENDPOINT}/{project_id}"

    Logger.instance().debug(f"{self.LOG_ID}.request_response:{url}?{urllib.parse.urlencode(query_params)}")

    return self.get(url, headers=self.default_headers, params=query_params)
