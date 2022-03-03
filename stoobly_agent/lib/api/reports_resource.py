import urllib

from ..logger import Logger
from .interfaces.requests_index_query_params import RequestsIndexQueryParams
from .stoobly_api import StooblyApi

class ReportsResource(StooblyApi):

  def create(self, project_id: str, params = {}):
    url = f"{self.service_url}{self.REPORTS_ENDPOINT}"

    body = {
        'project_id': project_id,
        **params,
    }

    return self.post(url, headers=self.default_headers, json=body)

  def index(self, project_id: str, query_params = {}):
    url = f"{self.service_url}{self.REPORTS_ENDPOINT}"

    return self.get(url, headers=self.default_headers, params={
        'project_id': project_id,
        **query_params,
    })