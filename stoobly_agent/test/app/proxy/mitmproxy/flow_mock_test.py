import pytest
import requests

from time import time
from unittest.mock import MagicMock

from mitmproxy.http import Headers, Request as MitmproxyRequest, Response as MitmproxyResponse

from stoobly_agent.app.proxy.mitmproxy.flow_mock import MitmproxyFlowMock


@pytest.fixture
def mitmproxy_request():
    now = time()
    return MitmproxyRequest(
        'example.com',
        443,
        b'GET',
        b'https',
        b'example.com:443',
        b'/api',
        b'HTTP/1.1',
        Headers(),
        b'',
        Headers(),
        now,
        now + 1,
    )


@pytest.fixture
def mitmproxy_response():
    return MitmproxyResponse.make(200, b'hello', {})


def make_requests_response(status_code=200, content=b''):
    resp = requests.Response()
    resp.status_code = status_code
    resp._content = content
    resp.raw = MagicMock()
    resp.raw.version = 11
    resp.raw._body = content
    return resp


class TestMitmproxyFlowMock:

    class TestRequestSetter:

        def test_accepts_mitmproxy_request(self, mitmproxy_request):
            flow = MitmproxyFlowMock()
            flow.request = mitmproxy_request
            assert flow.request is mitmproxy_request

        def test_converts_requests_Request(self):
            flow = MitmproxyFlowMock()
            req = requests.Request(method='GET', url='https://example.com/api', headers={}, data=b'')
            flow.request = req
            assert isinstance(flow.request, MitmproxyRequest)
            assert flow.request.method == 'GET'

    class TestResponseSetter:

        def test_accepts_mitmproxy_response(self, mitmproxy_response):
            flow = MitmproxyFlowMock()
            flow.response = mitmproxy_response
            assert flow.response is mitmproxy_response

        def test_converts_requests_Response(self):
            flow = MitmproxyFlowMock()
            resp = make_requests_response(status_code=201)
            flow.response = resp
            assert isinstance(flow.response, MitmproxyResponse)
            assert flow.response.status_code == 201

    class TestCopy:

        def test_copy_returns_new_instance(self, mitmproxy_request, mitmproxy_response):
            flow = MitmproxyFlowMock()
            flow.request = mitmproxy_request
            flow.response = mitmproxy_response
            copy = flow.copy()
            assert copy is not flow

        def test_copy_request_is_independent(self, mitmproxy_request, mitmproxy_response):
            flow = MitmproxyFlowMock()
            flow.request = mitmproxy_request
            flow.response = mitmproxy_response
            copy = flow.copy()
            copy.request.host = 'other.com'
            assert flow.request.host == 'example.com'

        def test_copy_response_is_independent(self, mitmproxy_request, mitmproxy_response):
            flow = MitmproxyFlowMock()
            flow.request = mitmproxy_request
            flow.response = mitmproxy_response
            copy = flow.copy()
            copy.response.status_code = 500
            assert flow.response.status_code == 200
