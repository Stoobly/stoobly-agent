import pytest
import requests

from time import time

from mitmproxy.http import Headers, Request as MitmproxyRequest

from stoobly_agent.app.models.adapters.mitmproxy.request.python_adapter import PythonRequestAdapter


@pytest.fixture
def mitmproxy_get_request():
    now = time()
    return MitmproxyRequest(
        'example.com',
        443,
        b'GET',
        b'https',
        b'example.com:443',
        b'/api/v1/users?page=1',
        b'HTTP/1.1',
        Headers(**{'authorization': b'Bearer token123', 'content-type': b'application/json'}),
        b'',
        Headers(),
        now,
        now + 1,
    )


@pytest.fixture
def mitmproxy_post_request():
    now = time()
    return MitmproxyRequest(
        'example.com',
        443,
        b'POST',
        b'https',
        b'example.com:443',
        b'/api/v1/users',
        b'HTTP/1.1',
        Headers(**{'content-type': b'application/json'}),
        b'{"name": "Alice"}',
        Headers(),
        now,
        now + 1,
    )


class TestPythonRequestAdapter:

    class TestAdapt:

        def test_returns_requests_Request_instance(self, mitmproxy_get_request):
            result = PythonRequestAdapter(mitmproxy_get_request).adapt()
            assert isinstance(result, requests.Request)

        def test_method_preserved(self, mitmproxy_get_request):
            result = PythonRequestAdapter(mitmproxy_get_request).adapt()
            assert result.method == 'GET'

        def test_url_preserved(self, mitmproxy_get_request):
            result = PythonRequestAdapter(mitmproxy_get_request).adapt()
            assert result.url == mitmproxy_get_request.url

        def test_headers_preserved(self, mitmproxy_get_request):
            result = PythonRequestAdapter(mitmproxy_get_request).adapt()
            assert result.headers['authorization'] == 'Bearer token123'
            assert result.headers['content-type'] == 'application/json'

        def test_content_as_data(self, mitmproxy_post_request):
            result = PythonRequestAdapter(mitmproxy_post_request).adapt()
            assert result.data == b'{"name": "Alice"}'
