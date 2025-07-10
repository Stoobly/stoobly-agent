import copy
import time
import pdb

from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow
from mitmproxy.http import Request, Response, Headers
from stoobly_agent.app.proxy.utils.minimize_headers import minimize_headers, minimize_request_headers, minimize_response_headers


class TestRewrite():

    def test_minimize_request_headers(self):
        headers_stub = [
            (b"Host", b"example-custom-container-service.com"),
            (b"Connection", b"close"),
            (b"X-Real-Ip", b"172.18.0.1"),
            (b"X-Forwarded-For", b"172.18.0.1"),
            (b"X-Forwarded-Host", b"example-custom-container-service.com"),
            (b"X-Forwarded-Proto", b"http"),
            (b"X-Forwarded-Ssl", b"off"),
            (b"X-Forwarded-Port", b"80"),
            (b"X-Original-Uri", b"/get"),
            (b"User-Agent", b"curl/7.68.0"),
            (b"Accept", b"*/*"),
            (b"Cache-Control", b"no-cache, no-store, must-revalidate"),
            (b"Expires", b"0"),
            (b"Pragma", b"no-cache"),
            (b"Sec-Fetch-Site", b"same-origin"),
        ]
        headers = Headers(headers_stub)

        flow_stub = MitmproxyHTTPFlow(client_conn=None, server_conn=None)
        flow_stub.request = Request(
            host="example-custom-container-service.com",
            port=80,
            method="GET",
            scheme="http",
            authority="example-custom-container-service.com",
            path="/",
            http_version="HTTP/1.1",
            headers=headers,
            content=None,
            trailers=None,
            timestamp_start=time.time(),
            timestamp_end=time.time() + 1,
        )

        old_headers = copy.deepcopy(flow_stub.request.headers)

        minimize_request_headers(flow_stub)

        new_headers = flow_stub.request.headers

        # Non-essential headers should be removed
        assert old_headers != new_headers
        assert "Pragma" in old_headers
        assert "Pragma" not in new_headers
        assert "pragma" in old_headers
        assert "pragma" not in new_headers

        # Essential headers should remain
        assert "Host" in new_headers
        assert "User-Agent" in new_headers

