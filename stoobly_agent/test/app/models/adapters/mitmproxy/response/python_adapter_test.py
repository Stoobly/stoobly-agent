import pytest
import requests

from mitmproxy.http import Response as MitmproxyResponse

from stoobly_agent.app.models.adapters.mitmproxy.response.python_adapter import PythonResponseAdapter


@pytest.fixture
def mitmproxy_json_response():
    return MitmproxyResponse.make(
        200,
        b'{"status": "ok"}',
        {'content-type': 'application/json', 'x-request-id': 'abc123'},
    )


@pytest.fixture
def mitmproxy_error_response():
    return MitmproxyResponse.make(
        404,
        b'Not Found',
        {'content-type': 'text/plain'},
    )


class TestPythonResponseAdapter:

    class TestAdapt:

        def test_returns_requests_Response_instance(self, mitmproxy_json_response):
            result = PythonResponseAdapter(mitmproxy_json_response).adapt()
            assert isinstance(result, requests.Response)

        def test_status_code_preserved(self, mitmproxy_json_response):
            result = PythonResponseAdapter(mitmproxy_json_response).adapt()
            assert result.status_code == 200

        def test_error_status_code_preserved(self, mitmproxy_error_response):
            result = PythonResponseAdapter(mitmproxy_error_response).adapt()
            assert result.status_code == 404

        def test_headers_preserved(self, mitmproxy_json_response):
            result = PythonResponseAdapter(mitmproxy_json_response).adapt()
            assert result.headers['content-type'] == 'application/json'
            assert result.headers['x-request-id'] == 'abc123'

        def test_raw_content_readable(self, mitmproxy_json_response):
            result = PythonResponseAdapter(mitmproxy_json_response).adapt()
            assert result.raw.read() == b'{"status": "ok"}'
