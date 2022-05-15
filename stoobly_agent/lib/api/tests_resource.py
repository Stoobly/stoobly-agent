import requests
import urllib

from stoobly_agent.lib.api.interfaces.tests import TestCreateParams

from ..logger import Logger
from .stoobly_api import StooblyApi

class TestsResource(StooblyApi):
  TESTS_ENDPOINT = 'tests'

  def create(self, project_id: str, raw_request, params: TestCreateParams = {}):
    url = f"{self.service_url}/{self.TESTS_ENDPOINT}"

    body = {
        'project_id': project_id,
        **params,
    }

    return self.post(url, headers=self.default_headers, data=body, files={ 'request': raw_request })

  def show(self, test_id: int, **query_params) -> requests.Response:
    url = f"{self.service_url}/{self.TESTS_ENDPOINT}/{test_id}"

    Logger.instance().debug(f"{self.LOG_ID}.request_response:{url}?{urllib.parse.urlencode(query_params)}")

    return self.get(url, headers=self.default_headers, params=query_params)