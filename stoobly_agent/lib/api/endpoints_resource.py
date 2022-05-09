import requests
import urllib
import pdb

from ..logger import Logger
from .interfaces import EndpointsIndexQueryParams
from .stoobly_api import StooblyApi

class EndpointsResource(StooblyApi):
  PROJECTS_ENDPOINT = 'endpoints'

  def index(self, **query_params: EndpointsIndexQueryParams) -> requests.Response:
    url = f"{self.service_url}/{self.PROJECTS_ENDPOINT}"

    Logger.instance().debug(f"{self.LOG_ID}.request_response:{url}?{urllib.parse.urlencode(query_params)}")

    return self.get(url, headers=self.default_headers, params=query_params)

  def show(self, endpoint_id: int, **query_params) -> requests.Response:
    url = f"{self.service_url}/{self.PROJECTS_ENDPOINT}/{endpoint_id}"

    Logger.instance().debug(f"{self.LOG_ID}.request_response:{url}?{urllib.parse.urlencode(query_params)}")

    return self.get(url, headers=self.default_headers, params=query_params)