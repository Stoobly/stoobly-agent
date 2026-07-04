from unittest.mock import patch
from urllib.parse import urlparse

import pytest

from stoobly_agent.test.test_helper import (
  DETERMINISTIC_GET_REQUEST_URL,
  make_deterministic_get_request_response,
)


def _uses_proxy(session, prepared_request, kwargs):
  proxies = kwargs['proxies'] if 'proxies' in kwargs else session.proxies
  if not proxies:
    return False
  scheme = urlparse(prepared_request.url).scheme
  return bool(proxies.get(scheme) or proxies.get('all'))


@pytest.fixture(autouse=True, scope='module')
def stub_deterministic_get_request(request):
  if 'DETERMINISTIC_GET_REQUEST_URL' not in getattr(request.module, '__dict__', {}):
    yield
    return

  import requests

  original_send = requests.Session.send

  def stub_send(self, prepared_request, **kwargs):
    if prepared_request.url == DETERMINISTIC_GET_REQUEST_URL and not _uses_proxy(self, prepared_request, kwargs):
      return make_deterministic_get_request_response()
    return original_send(self, prepared_request, **kwargs)

  with patch.object(requests.Session, 'send', stub_send):
    yield
