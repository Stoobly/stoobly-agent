import urllib

from ..logger import Logger
from .interfaces.requests_index_query_params import RequestsIndexQueryParams
from .stoobly_api import StooblyApi

class RequestsResource(StooblyApi):

  def create(self, project_id: str, raw_requests, params):
      url = f"{self.service_url}{self.REQUESTS_ENDPOINT}"

      body = {
          'project_id': project_id,
          **params,
      }

      return self.post(url, headers=self.default_headers, data=body, files={ 'requests': raw_requests })

  def index(self, project_id: int, query_params: RequestsIndexQueryParams):
    url = f"{self.service_url}{self.REQUESTS_ENDPOINT}"

    params = {
      'project_id': project_id,
      **query_params,
    }

    Logger.instance().debug(f"{self.LOG_ID}.request_response:{url}?{urllib.parse.urlencode(params)}")

    return self.get(url, headers=self.default_headers, params=params)

  def response(self, project_id: str, query_params):
    url = f"{self.service_url}{self.REQUESTS_ENDPOINT}/response"

    params = {
        'project_id': project_id,
        **query_params,
    }

    Logger.instance().debug(f"{self.LOG_ID}.request_response:{url}?{urllib.parse.urlencode(params)}")

    return self.get(
        url,
        allow_redirects=False,
        headers=self.default_headers,
        params=params,
        stream=True
    )

  def show(self, project_id: str, request_id: str, query_params):
      url = f"{self.service_url}{self.REQUESTS_ENDPOINT}/{request_id}"

      params = {
        'project_id': project_id,
        **query_params,
      }

      Logger.instance().debug(f"{self.LOG_ID}.request_response:{url}?{urllib.parse.urlencode(params)}")

      return self.get(url, headers=self.default_headers, params=params)