import pdb
import requests

from stoobly_agent.app.models.adapters.python import PythonRequestAdapterFactory
from stoobly_agent.app.models.adapters.raw_http_request_adapter import RawHttpRequestAdapter

class TestRawAdapter():

  def test_www_google_com(self):
    request = requests.Request(
      data=b'',
      headers={
        'Content-Length': '0'
      },
      method='GET',
      url='https://www.google.com?a=1&a=2',
    )
    raw_request = PythonRequestAdapterFactory(request).raw_request()

    self.__test_equivalence(raw_request, request)

  def test_stoobly_com(self):
    data = b'{"name": "test", "description": "test"}'
    request = requests.Request(
      data=data,
      headers={
        'Content-Length': str(len(data)),
        'Content-Type': 'application/json',
      },
      method='POST',
      url='https://stoobly.com/scenarios',
    )
    raw_request = PythonRequestAdapterFactory(request).raw_request()

    self.__test_equivalence(raw_request, request)

  def __test_equivalence(self, raw_request: str, request: requests.Request):
    _request = RawHttpRequestAdapter(raw_request).to_request()

    assert _request.method == request.method
    assert _request.url == request.url
    assert _request.data == request.data

    for key, val in request.headers.items():
      assert val == _request.headers.get(key)

