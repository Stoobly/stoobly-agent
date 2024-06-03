import requests
import urllib
import pdb

from stoobly_agent.app.models.types import HeaderNameCreateParams

from ..logger import Logger
from .endpoints_resource import EndpointsResource

LOG_ID = 'ResponseHeaderNamesResource'

class ResponseHeaderNamesResource(EndpointsResource):
  RESPONSE_HEADER_NAME_ENDPOINT = 'response_header_names'

  def create(self, endpoint_id: int, params: HeaderNameCreateParams = {}):
    url = f"{self.service_url}/{self.ENDPOINTS_ENDPOINT}/{endpoint_id}/{self.RESPONSE_HEADER_NAME_ENDPOINT}"
    return self.post(url, headers=self.default_headers, json=params)

  def index(self, endpoint_id: int, query_params = {}) -> requests.Response:
    url = f"{self.service_url}/{self.ENDPOINTS_ENDPOINT}/{endpoint_id}/{self.RESPONSE_HEADER_NAME_ENDPOINT}"

    Logger.instance(LOG_ID).debug(f"{url}?{urllib.parse.urlencode(query_params)}")

    return self.get(url, headers=self.default_headers, params=query_params)

  def show(self, endpoint_id: int, response_header_name_id: int, query_params = {}) -> requests.Response:
    url = f"{self.service_url}/{self.ENDPOINTS_ENDPOINT}/{endpoint_id}/{self.RESPONSE_HEADER_NAME_ENDPOINT}/{response_header_name_id}"

    Logger.instance(LOG_ID).debug(f"{url}?{urllib.parse.urlencode(query_params)}")

    return self.get(url, headers=self.default_headers, params=query_params)
  
  def destroy(self, endpoint_id: int, response_header_name_id: int, query_params = {}) -> requests.Response:
    url = f"{self.service_url}/{self.ENDPOINTS_ENDPOINT}/{endpoint_id}/{self.RESPONSE_HEADER_NAME_ENDPOINT}/{response_header_name_id}"

    Logger.instance(LOG_ID).debug(f"{url}?{urllib.parse.urlencode(query_params)}")

    return self.delete(url, headers=self.default_headers, params=query_params)