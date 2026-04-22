import json
import pytest

from mitmproxy.http import Response as MitmproxyResponse

from stoobly_agent.app.proxy.mitmproxy.response_body_facade import MitmproxyResponseBodyFacade


@pytest.fixture
def json_response():
    return MitmproxyResponse.make(
        200,
        json.dumps({'status': 'ok', 'count': 3}).encode(),
        {'content-type': 'application/json'},
    )


@pytest.fixture
def raw_response():
    return MitmproxyResponse.make(
        200,
        b'raw bytes',
        {},
    )


class TestMitmproxyResponseBodyFacade:

    class TestGet:

        def test_json_content_type_returns_dict(self, json_response):
            facade = MitmproxyResponseBodyFacade(json_response)
            result = facade.get('application/json')
            assert result == {'status': 'ok', 'count': 3}

        def test_no_content_type_returns_raw_bytes(self, raw_response):
            facade = MitmproxyResponseBodyFacade(raw_response)
            result = facade.get(None)
            assert result == b'raw bytes'

    class TestSet:

        def test_json_content_type_encodes_dict(self, json_response):
            facade = MitmproxyResponseBodyFacade(json_response)
            facade.set({'updated': True}, 'application/json')
            assert json_response.content == b'{"updated": true}'

        def test_roundtrip_json(self, json_response):
            payload = {'a': 1, 'b': 2}
            facade = MitmproxyResponseBodyFacade(json_response)
            facade.set(payload, 'application/json')
            assert facade.get('application/json') == payload

        def test_set_updates_response_content(self, json_response):
            facade = MitmproxyResponseBodyFacade(json_response)
            facade.set({'new': 'body'}, 'application/json')
            assert isinstance(json_response.content, bytes)
