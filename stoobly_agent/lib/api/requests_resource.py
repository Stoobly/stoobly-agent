import urllib

from ..logger import Logger
from .interfaces.requests_index_query_params import RequestsIndexQueryParams
from .stoobly_api import StooblyApi

class RequestsResource(StooblyApi):

  def index(self, project_id: int, query_params: RequestsIndexQueryParams):
    url = f"{self.service_url}{self.REQUESTS_ENDPOINT}"

    params = {
      'project_id': project_id,
      **query_params,
    }

    Logger.instance().debug(f"{self.LOG_ID}.request_response:{url}?{urllib.parse.urlencode(params)}")

    return self.get(url, headers=self.default_headers, params=params)

  def show(self, project_id: str, request_id: str, query_params):
      url = f"{self.service_url}{self.REQUESTS_ENDPOINT}/{request_id}"

      params = {
        'project_id': project_id,
        **query_params,
      }

      Logger.instance().debug(f"{self.LOG_ID}.request_response:{url}?{urllib.parse.urlencode(params)}")

      return self.get(url, headers=self.default_headers, params=params)