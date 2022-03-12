import urllib

from ..logger import Logger
from .interfaces.pagination_query_params import PaginationQueryParams
from .interfaces.scenarios_index_response import ScenariosIndexResponse
from .stoobly_api import StooblyApi

class ScenariosResource(StooblyApi):
  SCENARIOS_ENDPOINT = 'scenarios'

  def create(self, project_id: str, params, raw_requests = ''):
    url = f"{self.service_url}/{self.SCENARIOS_ENDPOINT}"

    body = {
        'project_id': project_id,
        **params,
    }

    files = {}
    if len(raw_requests) > 0:
      files = { 'file': raw_requests }

    return self.post(url, headers=self.default_headers, data=body, files=files)

  def index(self, project_id: int, query_params: PaginationQueryParams) -> ScenariosIndexResponse:
    url = f"{self.service_url}/{self.SCENARIOS_ENDPOINT}"

    params = {
      'project_id': project_id,
      **query_params,
    }

    Logger.instance().debug(f"{self.LOG_ID}.request_response:{url}?{urllib.parse.urlencode(params)}")

    return self.get(url, headers=self.default_headers, params=params)

