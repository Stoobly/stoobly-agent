import requests
import urllib
import pdb

from stoobly_agent.app.models.types import ParamNameCreateParams

from ..logger import Logger
from .endpoints_resource import EndpointsResource

class BodyParamNamesResource(EndpointsResource):
  BODY_PARAM_NAMES_ENDPOINT = 'body_param_names'

  def create(self, endpoint_id: int, params: ParamNameCreateParams = {}):
    url = f"{self.service_url}/{self.ENDPOINTS_ENDPOINT}/{endpoint_id}/{self.BODY_PARAM_NAMES_ENDPOINT}"
    return self.post(url, headers=self.default_headers, json=params)

  def index(self, endpoint_id: int, query_params = {}) -> requests.Response:
    url = f"{self.service_url}/{self.ENDPOINTS_ENDPOINT}/{endpoint_id}/{self.BODY_PARAM_NAMES_ENDPOINT}"

    Logger.instance().debug(f"{self.LOG_ID}.request_response:{url}?{urllib.parse.urlencode(query_params)}")

    return self.get(url, headers=self.default_headers, params=query_params)

  def show(self, endpoint_id: int, body_param_name_id: int, query_params = {}) -> requests.Response:
    url = f"{self.service_url}/{self.ENDPOINTS_ENDPOINT}/{endpoint_id}/{self.BODY_PARAM_NAMES_ENDPOINT}/{body_param_name_id}"

    Logger.instance().debug(f"{self.LOG_ID}.request_response:{url}?{urllib.parse.urlencode(query_params)}")

    return self.get(url, headers=self.default_headers, params=query_params)
  
  def destroy(self, endpoint_id, body_param_name_id: int, query_params = {}) -> requests.Response:
    url = f"{self.service_url}/{self.ENDPOINTS_ENDPOINT}/{endpoint_id}/{self.BODY_PARAM_NAMES_ENDPOINT}/{body_param_name_id}"

    Logger.instance().debug(f"{self.LOG_ID}.request_response:{url}?{urllib.parse.urlencode(query_params)}")

    return self.delete(url, headers=self.default_headers, params=query_params)