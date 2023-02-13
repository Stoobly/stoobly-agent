import requests
import urllib

from stoobly_agent.app.models.adapters.types.scenario_create_params import ScenarioCreateParams

from ..logger import Logger
from .interfaces.pagination_query_params import PaginationQueryParams
from .stoobly_api import StooblyApi

class ScenariosResource(StooblyApi):
  SCENARIOS_ENDPOINT = 'scenarios'

  def create(self, **params: ScenarioCreateParams):
    url = f"{self.service_url}/{self.SCENARIOS_ENDPOINT}"
    return self.post(url, headers=self.default_headers, data=params)

  def index(self, **query_params: PaginationQueryParams) -> requests.Response:
    url = f"{self.service_url}/{self.SCENARIOS_ENDPOINT}"

    Logger.instance().debug(f"{self.LOG_ID}.request_response:{url}?{urllib.parse.urlencode(query_params)}")

    return self.get(url, headers=self.default_headers, params=query_params)

  def show(self, scenario_id: int, **query_params) -> requests.Response:
    url = f"{self.service_url}/{self.SCENARIOS_ENDPOINT}/{scenario_id}"

    Logger.instance().debug(f"{self.LOG_ID}.request_response:{url}?{urllib.parse.urlencode(query_params)}")

    return self.get(url, headers=self.default_headers, params=query_params)