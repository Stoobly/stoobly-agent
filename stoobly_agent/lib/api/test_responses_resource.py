import requests
import urllib

from ..logger import Logger
from .tests_resource import TestsResource

class TestResponsesResource(TestsResource):
  RESPONSES_ENDPOINT = 'responses'

  def mock(self, test_id: int, **query_params) -> requests.Response:
    url = f"{self.service_url}/{self.TESTS_ENDPOINT}/{test_id}/{self.RESPONSES_ENDPOINT}/mock"

    Logger.instance().debug(f"{self.LOG_ID}.test_response_response:{url}?{urllib.parse.urlencode(query_params)}")

    return self.get(url, headers=self.default_headers, params=query_params) 