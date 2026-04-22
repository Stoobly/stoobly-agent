import json
import pytest

from mitmproxy.http import Request as MitmproxyRequest

from stoobly_agent.app.proxy.mitmproxy.request_body_facade import MitmproxyRequestBodyFacade


@pytest.fixture
def json_request():
    return MitmproxyRequest.make(
        method='POST',
        url='https://example.com/api',
        content=json.dumps({'key': 'value', 'count': 42}).encode(),
        headers={'content-type': 'application/json'},
    )


@pytest.fixture
def raw_request():
    return MitmproxyRequest.make(
        method='GET',
        url='https://example.com/api',
        content=b'raw bytes',
        headers={},
    )


class TestMitmproxyRequestBodyFacade:

    class TestGet:

        def test_json_content_type_returns_dict(self, json_request):
            facade = MitmproxyRequestBodyFacade(json_request)
            result = facade.get('application/json')
            assert result == {'key': 'value', 'count': 42}

        def test_no_content_type_returns_raw_bytes(self, raw_request):
            facade = MitmproxyRequestBodyFacade(raw_request)
            result = facade.get(None)
            assert result == b'raw bytes'

        def test_form_urlencoded_returns_parsed(self):
            request = MitmproxyRequest.make(
                method='POST',
                url='https://example.com/form',
                content=b'name=Alice&age=20',
                headers={'content-type': 'application/x-www-form-urlencoded'},
            )
            facade = MitmproxyRequestBodyFacade(request)
            result = facade.get('application/x-www-form-urlencoded')
            assert result == {b'name': [b'Alice'], b'age': [b'20']}

    class TestSet:

        def test_json_content_type_encodes_dict(self, json_request):
            facade = MitmproxyRequestBodyFacade(json_request)
            facade.set({'updated': True}, 'application/json')
            assert json_request.content == b'{"updated": true}'

        def test_roundtrip_json(self, json_request):
            payload = {'x': 1, 'y': 2}
            facade = MitmproxyRequestBodyFacade(json_request)
            facade.set(payload, 'application/json')
            assert facade.get('application/json') == payload

        def test_set_updates_request_content(self, json_request):
            facade = MitmproxyRequestBodyFacade(json_request)
            facade.set({'new': 'body'}, 'application/json')
            assert isinstance(json_request.content, bytes)
