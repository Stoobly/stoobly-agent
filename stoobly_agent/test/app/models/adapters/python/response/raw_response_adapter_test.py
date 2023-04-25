import pdb
import requests

from stoobly_agent.test.test_helper import DETERMINISTIC_GET_REQUEST_URL, NON_DETERMINISTIC_GET_REQUEST_URL

from stoobly_agent.app.models.adapters.python import PythonResponseAdapterFactory
from stoobly_agent.app.models.adapters.raw_http_response_adapter import RawHttpResponseAdapter

class TestRawResponseAdapter():

  def test_deterministic_request(self):
    res = requests.get(DETERMINISTIC_GET_REQUEST_URL, stream=True) 

    raw_response = PythonResponseAdapterFactory(res).raw_response()
    self.__test_equivalence(raw_response, res)

  def test_non_deterministic_request(self):
    res = requests.get(NON_DETERMINISTIC_GET_REQUEST_URL, stream=True) 

    raw_response = PythonResponseAdapterFactory(res).raw_response()
    self.__test_equivalence(raw_response, res)

  def __test_equivalence(self, raw_response: str, response: requests.Response):
    _response = RawHttpResponseAdapter(raw_response).to_response()
    
    assert _response.request == None
    assert _response.raw.data == response.raw.data
    assert _response.status_code == response.status_code

    for key, val in response.headers.items():
      assert val == _response.headers.get(key)


