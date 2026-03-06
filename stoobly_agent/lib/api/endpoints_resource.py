import urllib
import pdb

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from requests import Response

from ..logger import Logger
from .interfaces import EndpointsIndexQueryParams
from .stoobly_api import StooblyApi

LOG_ID = 'EndpointsResource'

class EndpointsResource(StooblyApi):
  ENDPOINTS_ENDPOINT = 'endpoints'

  def create(self, **params):
    url = f"{self.service_url}/{self.ENDPOINTS_ENDPOINT}"
    return self.post(url, headers=self.default_headers, json=params)

  def index(self, **query_params: EndpointsIndexQueryParams) -> 'Response':
    url = f"{self.service_url}/{self.ENDPOINTS_ENDPOINT}"

    Logger.instance(LOG_ID).debug(f"{url}?{urllib.parse.urlencode(query_params)}")

    return self.get(url, headers=self.default_headers, params=query_params)

  def show(self, endpoint_id: int, **query_params) -> 'Response':
    url = f"{self.service_url}/{self.ENDPOINTS_ENDPOINT}/{endpoint_id}"

    Logger.instance(LOG_ID).debug(f"{url}?{urllib.parse.urlencode(query_params)}")

    return self.get(url, headers=self.default_headers, params=query_params)

  def destroy(self, endpoint_id: int, **query_params) -> 'Response':
    url = f"{self.service_url}/{self.ENDPOINTS_ENDPOINT}/{endpoint_id}"

    Logger.instance(LOG_ID).debug(f"{url}?{urllib.parse.urlencode(query_params)}")

    return self.delete(url, headers=self.default_headers, params=query_params)