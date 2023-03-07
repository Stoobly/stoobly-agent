import pdb
import requests

from mitmproxy.http import Request as MitmproxyRequest

from stoobly_agent.app.models.adapters.python import PythonRequestAdapterFactory

class TestMitmproxyAdapter():

  def test_www_google_com(self):
    request = requests.Request(
      data=b'',
      headers={
        'Content-Length': '0'
      },
      method='GET',
      url='https://www.google.com',
    )

    mitmproxy_request = PythonRequestAdapterFactory(request).mitmproxy_request()
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

    mitmproxy_request = PythonRequestAdapterFactory(request).mitmproxy_request()

    self.__test_equivalence(mitmproxy_request, request)

  def __test_equivalence(self, mitmproxy_request: MitmproxyRequest, request: requests.Request):
    assert mitmproxy_request.method == request.method
    assert mitmproxy_request.url.rstrip('/') == request.url
    assert mitmproxy_request.content == request.data

    for key, val in request.headers.items():
      assert val == mitmproxy_request.headers.get(key)
