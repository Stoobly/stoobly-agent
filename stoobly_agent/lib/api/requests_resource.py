import pdb
import urllib

from ..logger import Logger
from .interfaces import RequestCreateParams, RequestsIndexQueryParams, RequestShowQueryParams
from .stoobly_api import StooblyApi

class RequestsResource(StooblyApi):

  def create(self, **body_params: RequestCreateParams):
      url = f"{self.service_url}{self.REQUESTS_ENDPOINT}"

      requests = body_params.get('requests')

      if requests:
        del body_params['requests']

      proxies = {}

      return self.post(url, headers=self.default_headers, data=body_params, files={ 'requests': requests }, proxies=proxies)

  def index(self, **query_params: RequestsIndexQueryParams):
    url = f"{self.service_url}{self.REQUESTS_ENDPOINT}"

    Logger.instance().debug(f"{self.LOG_ID}.request_response:{url}?{urllib.parse.urlencode(query_params)}")

    return self.get(url, headers=self.default_headers, params=query_params)

  def response(self, **query_params):
    url = f"{self.service_url}{self.REQUESTS_ENDPOINT}/response"

    Logger.instance().debug(f"{self.LOG_ID}.request_response:{url}?{urllib.parse.urlencode(query_params)}")

    return self.get(
        url,
        allow_redirects=False,
        headers=self.default_headers,
        params=query_params,
        stream=True
    )

  def show(self, request_id, **query_params: RequestShowQueryParams):
      url = f"{self.service_url}{self.REQUESTS_ENDPOINT}/{request_id}"

      Logger.instance().debug(f"{self.LOG_ID}.request_response:{url}?{urllib.parse.urlencode(query_params)}")

      return self.get(url, headers=self.default_headers, params=query_params)