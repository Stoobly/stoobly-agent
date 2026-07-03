from unittest.mock import patch

import pytest
import requests

from stoobly_agent.test.test_helper import (
  DETERMINISTIC_GET_REQUEST_URL,
  make_deterministic_get_request_response,
)


@pytest.fixture(autouse=True, scope='module')
def stub_deterministic_get_request(request):
  if 'DETERMINISTIC_GET_REQUEST_URL' not in getattr(request.module, '__dict__', {}):
    yield
    return

  original_send = requests.Session.send

  def stub_send(self, prepared_request, **kwargs):
    if prepared_request.url == DETERMINISTIC_GET_REQUEST_URL:
      return make_deterministic_get_request_response()
    return original_send(self, prepared_request, **kwargs)

  with patch.object(requests.Session, 'send', stub_send):
    yield
