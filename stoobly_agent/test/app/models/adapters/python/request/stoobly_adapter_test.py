import requests

from stoobly_agent.lib.api.interfaces import RequestShowResponse
from stoobly_agent.app.models.adapters.python import PythonRequestAdapterFactory

class TestStooblyAdapter():

  def test_www_google_com(self):
    request = requests.Request(
      data=b'',
      headers={
        'Content-Length': '0'
      },
      method='GET',
      url='https://www.google.com',
    )

    mitmproxy_request = PythonRequestAdapterFactory(request).stoobly_request()
    self.__test_equivalence(mitmproxy_request, request)

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

    mitmproxy_request = PythonRequestAdapterFactory(request).stoobly_request()

    self.__test_equivalence(mitmproxy_request, request)

  def __test_equivalence(self, stoobly_request: RequestShowResponse, request: requests.Request):
    assert stoobly_request['method'] == request.method
    assert stoobly_request['url'] == request.url
    assert stoobly_request['body'] == request.data

    stoobly_request_headers = {}
    for header in stoobly_request['headers']:
      stoobly_request_headers[header['name']] = header['value']
      
    for name, value in request.headers.items():
      assert value == stoobly_request_headers.get(name)

