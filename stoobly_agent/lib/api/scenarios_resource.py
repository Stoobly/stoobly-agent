import requests
import urllib

from stoobly_agent.app.models.types import ScenarioCreateParams

from ..logger import Logger
from .interfaces.pagination_query_params import PaginationQueryParams
from .stoobly_api import StooblyApi

LOG_ID = 'ScenariosResource'

class ScenariosResource(StooblyApi):
  SCENARIOS_ENDPOINT = 'scenarios'

  def create(self, **params: ScenarioCreateParams):
    url = f"{self.service_url}/{self.SCENARIOS_ENDPOINT}"
    return self.post(url, headers=self.default_headers, data=params)

  def index(self, **query_params: PaginationQueryParams) -> requests.Response:
    url = f"{self.service_url}/{self.SCENARIOS_ENDPOINT}"

    Logger.instance(LOG_ID).debug(f"{url}?{urllib.parse.urlencode(query_params)}")

    return self.get(url, headers=self.default_headers, params=query_params)

  def show(self, scenario_id: int, **query_params) -> requests.Response:
    url = f"{self.service_url}/{self.SCENARIOS_ENDPOINT}/{scenario_id}"

    Logger.instance(LOG_ID).debug(f"{url}?{urllib.parse.urlencode(query_params)}")

    return self.get(url, headers=self.default_headers, params=query_params)

  def update(self, scenario_id: int, **params):
    url = f"{self.service_url}/{self.SCENARIOS_ENDPOINT}/{scenario_id}"

    Logger.instance(LOG_ID).debug(f"{url}")

    return self.put(url, headers=self.default_headers, json=params)