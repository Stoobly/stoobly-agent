import pdb
import requests

from stoobly_agent.app.models.adapters.python.response import PythonResponseAdapterFactory
from stoobly_agent.app.models.adapters.raw_http_response_adapter import RawHttpResponseAdapter
from stoobly_agent.app.proxy.mitmproxy.response_facade import MitmproxyResponseFacade
from stoobly_agent.app.proxy.record.response_string import ResponseString

class TestRequestString():
    
    def test_www_google_com(self):
        url='https://www.google.com'
        response = requests.get(url, stream=True)

        response_string = self.__to_response_string(response)
        raw_response_string = response_string.get()
        _response = RawHttpResponseAdapter(raw_response_string).to_response()

        self.__test_equivalence(_response, response)

    def __test_equivalence(self, response: requests.Response, _response: requests.Response):
        assert _response.raw.data == response.raw.data

        for key, val in _response.headers.items():
            assert val == response.headers.get(key)

    def __to_response_string(self, response: requests.Response):
        mitmproxy_response = PythonResponseAdapterFactory(response).mitmproxy_response()
        mitmproxy_response_facade = MitmproxyResponseFacade(mitmproxy_response)
        return ResponseString(mitmproxy_response_facade, None)