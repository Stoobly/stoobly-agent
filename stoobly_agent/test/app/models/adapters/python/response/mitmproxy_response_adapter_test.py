import pdb
import requests

from mitmproxy.http import Response as MitmproxyResponse

from stoobly_agent.test.test_helper import DETERMINISTIC_GET_REQUEST_URL, NON_DETERMINISTIC_GET_REQUEST_URL

from stoobly_agent.app.models.adapters.python import PythonResponseAdapterFactory

class TestMitmproxyResponseAdapter():

  def test_deterministic_request(self):
    res = requests.get(DETERMINISTIC_GET_REQUEST_URL) 

    mitmproxy_response = PythonResponseAdapterFactory(res).mitmproxy_response()
    self.__test_equivalence(mitmproxy_response, res)

  def test_non_deterministic_request(self):
    res = requests.get(NON_DETERMINISTIC_GET_REQUEST_URL) 

    mitmproxy_response = PythonResponseAdapterFactory(res).mitmproxy_response()
    self.__test_equivalence(mitmproxy_response, res)

  def __test_equivalence(self, mitmproxy_response: MitmproxyResponse, response: requests.Response):
    assert mitmproxy_response.raw_content == response.raw.data
    assert mitmproxy_response.content == response.content
    assert mitmproxy_response.status_code == response.status_code

    for key, val in response.headers.items():
      assert val == mitmproxy_response.headers.get(key)

