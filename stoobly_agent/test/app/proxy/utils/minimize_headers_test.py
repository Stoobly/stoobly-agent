import copy
import time

from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow
from mitmproxy.http import Request, Response, Headers
from stoobly_agent.app.proxy.utils.minimize_headers import (
    minimize_headers, 
    minimize_request_headers,
)


class TestMinimizeHeaders():

    def test_minimize_request_headers(self):
        headers_stub = [
            # Essential headers (should be preserved)
            (b"Host", b"api.example.com"),
            (b"User-Agent", b"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"),
            (b"Accept", b"application/json, text/plain, */*"),
            (b"Accept-Language", b"en-US,en;q=0.9"),
            (b"Accept-Encoding", b"gzip, deflate, br"),
            (b"Content-Type", b"application/json"),
            (b"Content-Length", b"42"),
            (b"Origin", b"https://example.com"),
            (b"Referer", b"https://example.com/page"),
            
            # Headers that should be removed
            (b"Cookie", b"session=abc123; user=john"),
            (b"Authorization", b"Bearer token123"),
            (b"X-Request-ID", b"req-uuid-123"),
            (b"X-Forwarded-For", b"192.168.1.1"),
            (b"X-Custom-Header", b"custom-value"),
            (b"Sec-Fetch-Mode", b"cors"),
            (b"Sec-Fetch-Dest", b"empty"),
            (b"DNT", b"1"),
        ]
        headers = Headers(headers_stub)

        flow_stub = MitmproxyHTTPFlow(client_conn=None, server_conn=None)
        flow_stub.request = Request(
            host="api.example.com",
            port=443,
            method="POST",
            scheme="https",
            authority="api.example.com",
            path="/api/v1/data",
            http_version="HTTP/1.1",
            headers=headers,
            content=b'{"data": "test"}',
            trailers=None,
            timestamp_start=time.time(),
            timestamp_end=time.time() + 1,
        )

        old_headers = copy.deepcopy(flow_stub.request.headers)

        minimize_request_headers(flow_stub)

        new_headers = flow_stub.request.headers

        # Non-essential headers should be removed
        assert old_headers != new_headers
        assert "Cookie" in old_headers
        assert "Cookie" not in new_headers
        assert "Authorization" not in new_headers
        assert "X-Request-ID" not in new_headers
        assert "X-Forwarded-For" not in new_headers
        assert "X-Custom-Header" not in new_headers
        assert "Sec-Fetch-Mode" not in new_headers
        assert "Sec-Fetch-Dest" not in new_headers
        assert "DNT" not in new_headers

        # Essential headers should remain
        assert "Host" in new_headers
        assert "User-Agent" in new_headers
        assert "Accept" in new_headers
        assert "Accept-Language" in new_headers
        assert "Accept-Encoding" in new_headers
        assert "Content-Type" in new_headers
        assert "Content-Length" in new_headers
        assert "Origin" in new_headers
        assert "Referer" in new_headers

    def test_minimize_headers(self):
        req_headers = Headers([
            (b"Host", b"example.com"),
            (b"X-Remove-Me", b"bye")
        ])
        res_headers = Headers([
            (b"Content-Type", b"text/html"),
            (b"X-Remove-Me", b"bye"),
            (b"Set-Cookie", b"session=new"),
        ])
        flow_stub = MitmproxyHTTPFlow(client_conn=None, server_conn=None)
        flow_stub.request = Request(
            host="example.com",
            port=80,
            method="GET",
            scheme="http",
            authority="example.com",
            path="/",
            http_version="HTTP/1.1",
            headers=req_headers,
            content=None,
            trailers=None,
            timestamp_start=time.time(),
            timestamp_end=time.time() + 1,
        )
        flow_stub.response = Response(
            http_version="HTTP/1.1",
            status_code=200,
            reason="OK",
            headers=res_headers,
            content=b"<html></html>",
            trailers=None,
            timestamp_start=time.time(),
            timestamp_end=time.time() + 1,
        )
        old_req_headers = copy.deepcopy(flow_stub.request.headers)
        old_res_headers = copy.deepcopy(flow_stub.response.headers)
        
        minimize_headers(flow_stub)
        
        # Request headers are minimized
        assert old_req_headers != flow_stub.request.headers
        assert "X-Remove-Me" not in flow_stub.request.headers
        assert "Host" in flow_stub.request.headers
        assert len(flow_stub.request.headers) == 1

        # Response headers are preserved
        assert old_res_headers == flow_stub.response.headers
        assert "X-Remove-Me" in flow_stub.response.headers
        assert "Set-Cookie" in flow_stub.response.headers
        assert "Content-Type" in flow_stub.response.headers
        assert len(flow_stub.response.headers) == 3

    def test_empty_headers(self):
        """Test minimize functions with empty headers"""
        flow_stub = MitmproxyHTTPFlow(client_conn=None, server_conn=None)
        flow_stub.request = Request(
            host="example.com",
            port=80,
            method="GET",
            scheme="http",
            authority="example.com",
            path="/",
            http_version="HTTP/1.1",
            headers=Headers(),
            content=None,
            trailers=None,
            timestamp_start=time.time(),
            timestamp_end=time.time() + 1,
        )
        flow_stub.response = Response(
            http_version="HTTP/1.1",
            status_code=200,
            reason="OK",
            headers=Headers(),
            content=b"",
            trailers=None,
            timestamp_start=time.time(),
            timestamp_end=time.time() + 1,
        )
        
        # Should not raise any errors
        minimize_headers(flow_stub)
        assert len(flow_stub.request.headers) == 0
        assert len(flow_stub.response.headers) == 0

    def test_case_sensitivity(self):
        """Test that header matching is case-insensitive"""
        headers_stub = [
            (b"host", b"example.com"),  # lowercase
            (b"USER-AGENT", b"test-agent"),  # uppercase
            (b"Content-Type", b"application/json"),  # mixed case
            (b"x-remove-me", b"bye"),  # should be removed
        ]
        headers = Headers(headers_stub)
        
        flow_stub = MitmproxyHTTPFlow(client_conn=None, server_conn=None)
        flow_stub.request = Request(
            host="example.com",
            port=80,
            method="POST",
            scheme="http",
            authority="example.com",
            path="/",
            http_version="HTTP/1.1",
            headers=headers,
            content=b'{"test": "data"}',
            trailers=None,
            timestamp_start=time.time(),
            timestamp_end=time.time() + 1,
        )
        
        minimize_request_headers(flow_stub)
        
        # Case-insensitive matching should preserve these headers
        assert "host" in flow_stub.request.headers
        assert "USER-AGENT" in flow_stub.request.headers
        assert "Content-Type" in flow_stub.request.headers
        
        # Non-allowed header should be removed regardless of case
        assert "x-remove-me" not in flow_stub.request.headers

    def test_minimize_headers_no_response(self):
        """Test minimize_headers when response is None"""
        flow_stub = MitmproxyHTTPFlow(client_conn=None, server_conn=None)
        flow_stub.request = Request(
            host="example.com",
            port=80,
            method="GET",
            scheme="http",
            authority="example.com",
            path="/",
            http_version="HTTP/1.1",
            headers=Headers([(b"Host", b"example.com"), (b"X-Remove", b"me")]),
            content=None,
            trailers=None,
            timestamp_start=time.time(),
            timestamp_end=time.time() + 1,
        )
        flow_stub.response = None
        
        # Should not raise an error when response is None
        minimize_headers(flow_stub)
        assert "Host" in flow_stub.request.headers
        assert "X-Remove" not in flow_stub.request.headers

    def test_header_ordering_preserved(self):
        """Test that header ordering is preserved after minimization"""
        headers_stub = [
            (b"Host", b"example.com"),
            (b"User-Agent", b"test-agent"),
            (b"Accept", b"application/json"),
            (b"X-Remove-1", b"bye"),
            (b"Content-Type", b"application/json"),
            (b"X-Remove-2", b"bye"),
        ]
        headers = Headers(headers_stub)
        
        flow_stub = MitmproxyHTTPFlow(client_conn=None, server_conn=None)
        flow_stub.request = Request(
            host="example.com",
            port=80,
            method="POST",
            scheme="http",
            authority="example.com",
            path="/",
            http_version="HTTP/1.1",
            headers=headers,
            content=b'{"test": "data"}',
            trailers=None,
            timestamp_start=time.time(),
            timestamp_end=time.time() + 1,
        )
        
        minimize_request_headers(flow_stub)
        
        # Check that remaining headers maintain relative order
        remaining_headers = list(flow_stub.request.headers.keys())
        expected_order = ["Host", "User-Agent", "Accept", "Content-Type"]
        assert remaining_headers == expected_order
