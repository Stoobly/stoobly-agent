import urllib

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from requests import Response

from ..logger import Logger
from .tests_resource import TestsResource

LOG_ID = 'TestResponsesResource'

class TestResponsesResource(TestsResource):
  RESPONSES_ENDPOINT = 'responses'

  def mock(self, test_id: int, **query_params) -> 'Response':
    url = f"{self.service_url}/{self.TESTS_ENDPOINT}/{test_id}/{self.RESPONSES_ENDPOINT}/mock"

    Logger.instance(LOG_ID).debug(f"{url}?{urllib.parse.urlencode(query_params)}")

    return self.get(url, headers=self.default_headers, params=query_params) 