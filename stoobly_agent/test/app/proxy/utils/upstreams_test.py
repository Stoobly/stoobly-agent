from time import time

import pytest
from mitmproxy.http import Headers, Request as MitmproxyRequest, Response as MitmproxyResponse

from stoobly_agent.app.cli.helpers.options import normalize_proxy_regular_upstream
from stoobly_agent.app.proxy.mitmproxy.flow_mock import MitmproxyFlowMock
from stoobly_agent.app.proxy.utils.upstreams import (
    apply_upstreams,
    parse_proxy_regular_upstreams,
    restore_upstreams,
)


@pytest.fixture
def mitmproxy_request():
    now = time()
    return MitmproxyRequest(
        'local.api.stoobly',
        3001,
        b'GET',
        b'http',
        b'local.api.stoobly:3001',
        b'/api',
        b'HTTP/1.1',
        Headers(),
        b'',
        Headers(),
        now,
        now + 1,
    )


@pytest.fixture
def flow(mitmproxy_request):
    flow = MitmproxyFlowMock()
    flow.request = mitmproxy_request
    return flow


class TestNormalizeProxyRegularUpstream:

    def test_joins_multiple_values(self):
        assert normalize_proxy_regular_upstream([
            'a:1=b:2',
            'c:3=d:4',
        ]) == 'a:1=b:2,c:3=d:4'

    def test_passes_through_string(self):
        assert normalize_proxy_regular_upstream('a:1=b:2') == 'a:1=b:2'


class TestParseProxyRegularUpstreams:

    def test_parses_single_mapping_with_explicit_port(self):
        assert parse_proxy_regular_upstreams(
            'local.api.stoobly:3001=http://host.docker.internal:3002'
        ) == {
            'local.api.stoobly:3001': 'http://host.docker.internal:3002',
        }

    def test_parses_mapping_without_port(self):
        assert parse_proxy_regular_upstreams(
            'api.example.com:443=https://backend'
        ) == {
            'api.example.com:443': 'https://backend',
        }

    def test_parses_multiple_mappings(self):
        assert parse_proxy_regular_upstreams(
            'a:1=http://b:2,c:3=https://d:4'
        ) == {
            'a:1': 'http://b:2',
            'c:3': 'https://d:4',
        }

    def test_parses_mixed_port_specifications(self):
        assert parse_proxy_regular_upstreams(
            'api.example.com:443=https://backend:8443,other:80=http://internal'
        ) == {
            'api.example.com:443': 'https://backend:8443',
            'other:80': 'http://internal',
        }

    def test_ignores_invalid_entries(self):
        assert parse_proxy_regular_upstreams('a:1=http://b:2,invalid,=missing') == {
            'a:1': 'http://b:2',
        }

    def test_empty_returns_empty_dict(self):
        assert parse_proxy_regular_upstreams(None) == {}
        assert parse_proxy_regular_upstreams('') == {}


class TestApplyUpstreams:

    def test_remaps_with_explicit_scheme_and_port(self, flow):
        upstreams = {
            'local.api.stoobly:3001': 'http://host.docker.internal:3002',
        }

        assert apply_upstreams(flow, upstreams) is True
        assert flow.request.host == 'host.docker.internal'
        assert flow.request.port == 3002
        assert flow.request.scheme == 'http'

    def test_remaps_with_https_and_explicit_port(self, flow):
        upstreams = {
            'local.api.stoobly:3001': 'https://host.docker.internal:3002',
        }

        assert apply_upstreams(flow, upstreams) is True
        assert flow.request.host == 'host.docker.internal'
        assert flow.request.port == 3002
        assert flow.request.scheme == 'https'

    def test_remaps_with_https_no_port(self, flow):
        upstreams = {
            'local.api.stoobly:3001': 'https://backend',
        }

        assert apply_upstreams(flow, upstreams) is True
        assert flow.request.host == 'backend'
        assert flow.request.port == 443  # Default HTTPS port
        assert flow.request.scheme == 'https'

    def test_remaps_with_http_no_port(self, flow):
        upstreams = {
            'local.api.stoobly:3001': 'http://backend',
        }

        assert apply_upstreams(flow, upstreams) is True
        assert flow.request.host == 'backend'
        assert flow.request.port == 80  # Default HTTP port
        assert flow.request.scheme == 'http'

    def test_miss_leaves_host_unchanged(self, flow):
        upstreams = {
            'other.host:80': 'upstream:80',
        }

        assert apply_upstreams(flow, upstreams) is False
        assert flow.request.host == 'local.api.stoobly'
        assert flow.request.port == 3001

    def test_skips_when_response_already_set(self, flow):
        flow.response = MitmproxyResponse.make(200, b'ok', {})
        upstreams = {
            'local.api.stoobly:3001': 'host.docker.internal:3002',
        }

        assert apply_upstreams(flow, upstreams) is False
        assert flow.request.host == 'local.api.stoobly'
        assert flow.request.port == 3001

    def test_empty_upstreams_is_noop(self, flow):
        assert apply_upstreams(flow, {}) is False
        assert apply_upstreams(flow, None) is False


class TestRestoreUpstreams:

    def test_restores_host_port_after_apply(self, flow):
        upstreams = {
            'local.api.stoobly:3001': 'host.docker.internal:3002',
        }

        apply_upstreams(flow, upstreams)
        assert flow.request.host == 'host.docker.internal'

        assert restore_upstreams(flow) is True
        assert flow.request.host == 'local.api.stoobly'
        assert flow.request.port == 3001

    def test_restore_without_apply_is_noop(self, flow):
        assert restore_upstreams(flow) is False
        assert flow.request.host == 'local.api.stoobly'
        assert flow.request.port == 3001

    def test_restores_post_rewrite_host_not_pre_rewrite(self, flow):
        flow.request.host = 'rewritten.example'
        flow.request.port = 4000

        upstreams = {
            'rewritten.example:4000': 'host.docker.internal:3002',
        }

        apply_upstreams(flow, upstreams)
        assert flow.request.host == 'host.docker.internal'
        assert flow.request.port == 3002

        restore_upstreams(flow)
        assert flow.request.host == 'rewritten.example'
        assert flow.request.port == 4000
