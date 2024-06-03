import requests
import urllib
import pdb

from stoobly_agent.app.models.types import ParamNameCreateParams

from ..logger import Logger
from .endpoints_resource import EndpointsResource

LOG_ID = 'QueryParamNamesResource'

class QueryParamNamesResource(EndpointsResource):
  QUERY_PARAM_NAMES_ENDPOINT = 'query_param_names'

  def create(self, endpoint_id: int, params: ParamNameCreateParams = {}):
    url = f"{self.service_url}/{self.ENDPOINTS_ENDPOINT}/{endpoint_id}/{self.QUERY_PARAM_NAMES_ENDPOINT}"
    return self.post(url, headers=self.default_headers, json=params)

  def index(self, endpoint_id: int, query_params = {}) -> requests.Response:
    url = f"{self.service_url}/{self.ENDPOINTS_ENDPOINT}/{endpoint_id}/{self.QUERY_PARAM_NAMES_ENDPOINT}"

    Logger.instance(LOG_ID).debug(f"{url}?{urllib.parse.urlencode(query_params)}")

    return self.get(url, headers=self.default_headers, params=query_params)

  def show(self, endpoint_id: int, query_param_name_id: int, query_params = {}) -> requests.Response:
    url = f"{self.service_url}/{self.ENDPOINTS_ENDPOINT}/{endpoint_id}/{self.QUERY_PARAM_NAMES_ENDPOINT}/{query_param_name_id}"

    Logger.instance(LOG_ID).debug(f"{url}?{urllib.parse.urlencode(query_params)}")

    return self.get(url, headers=self.default_headers, params=query_params)
  
  def destroy(self, endpoint_id: int, query_param_name_id: int, query_params = {}) -> requests.Response:
    url = f"{self.service_url}/{self.ENDPOINTS_ENDPOINT}/{endpoint_id}/{self.QUERY_PARAM_NAMES_ENDPOINT}/{query_param_name_id}"

    Logger.instance(LOG_ID).debug(f"{url}?{urllib.parse.urlencode(query_params)}")

    return self.delete(url, headers=self.default_headers, params=query_params)