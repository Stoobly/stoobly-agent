import os
import pdb
import requests

from stoobly_agent.app.models.adapters.python.request import PythonRequestAdapterFactory
from stoobly_agent.app.proxy.mitmproxy.request_facade import MitmproxyRequestFacade
from stoobly_agent.app.proxy.record.proxy_request import ProxyRequest
from stoobly_agent.app.proxy.record.request_string import RequestString
from stoobly_agent.app.models.adapters.raw_http_request_adapter import RawHttpRequestAdapter

class TestRequestString():
    
    def test_www_google_com(self):
        request = requests.Request(
            data=b'',
            headers={
                'Content-Length': '0'
            },
            method='GET',
            url='https://www.google.com',
        )

        request_string = self.__to_request_string(request)
        raw_request_string = request_string.get()
        _request = RawHttpRequestAdapter(raw_request_string).to_request()

        self.__test_equivalence(_request, request)

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

        request_string = self.__to_request_string(request)
        raw_request_string = request_string.get()
        _request = RawHttpRequestAdapter(raw_request_string).to_request()

        self.__test_equivalence(_request, request)

    def __test_equivalence(self, request: requests.Request, _request: requests.Request):
        assert _request.method == request.method

        # MitmproxyRequest adds a trailing /
        assert _request.url.rstrip('/') == request.url.rstrip('/')

        assert _request.data == request.data

        for key, val in _request.headers.items():
            assert val == request.headers.get(key)

    def __to_request_string(self, request: requests.Request):
        mitmproxy_request = PythonRequestAdapterFactory(request).mitmproxy_request()
        mitmproxy_request_facade = MitmproxyRequestFacade(mitmproxy_request)
        proxy_request = ProxyRequest(mitmproxy_request_facade)
        return RequestString(proxy_request)