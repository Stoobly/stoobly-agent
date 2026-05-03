import pytest

from mitmproxy.http import Headers, Request as MitmproxyRequest

from stoobly_agent.app.proxy.intercept_settings import InterceptSettings
from stoobly_agent.app.proxy.utils.request_transformation_log_cache import (
    RequestTransformationLogCache,
    append_log_from_request,
)
from stoobly_agent.app.proxy.utils.request_transformation_entry_logger import RequestTransformationEntryLogger
from stoobly_agent.app.settings import Settings
from stoobly_agent.app.settings.constants import request_component
from stoobly_agent.config.constants import custom_headers
from stoobly_agent.config.constants import mode as agent_mode
from stoobly_agent.lib.cache import Cache


@pytest.fixture(autouse=True)
def reset_singletons():
    Cache._instance = None
    RequestTransformationLogCache._instance = None
    RequestTransformationEntryLogger._pending.clear()
    yield
    Cache._instance = None
    RequestTransformationLogCache._instance = None
    RequestTransformationEntryLogger._pending.clear()


def _mitm_request(**header_items):
    h = Headers()
    for k, v in header_items.items():
        h.add(k, v)
    return MitmproxyRequest(
        'example.com',
        443,
        b'GET',
        b'https',
        b'example.com:443',
        b'/test',
        b'HTTP/1.1',
        h,
        b'',
        Headers(),
        0,
        0,
    )


class TestRequestTransformationLogCache:
    def test_singleton_returns_same_instance(self):
        a = RequestTransformationLogCache.instance()
        b = RequestTransformationLogCache.instance()
        assert a is b

    def test_direct_init_raises(self):
        RequestTransformationLogCache.instance()
        with pytest.raises(RuntimeError, match='instance'):
            RequestTransformationLogCache()

    def test_append_read_order_and_delete(self):
        cache = RequestTransformationLogCache.instance()
        uid = '550e8400-e29b-41d4-a716-446655440000'
        e1 = {
            'action': 'rewrite',
            'lifecycle': 'request',
            'target': 'url',
            'mode': agent_mode.MOCK,
            'details': 'rewriting URL a => b',
        }
        e2 = {
            'action': 'filter',
            'lifecycle': 'request',
            'target': 'url',
            'mode': agent_mode.RECORD,
            'details': 'filtering (exclude) request https://x',
        }
        cache.append(uid, e1)
        cache.append(uid, e2)
        rows = cache.read(uid)
        assert len(rows) == 2
        assert rows[0]['details'] == e1['details']
        assert rows[1]['details'] == e2['details']
        assert rows[0] is not e1
        cache.delete(uid)
        assert cache.read(uid) == []

    def test_append_many_extends_existing(self):
        cache = RequestTransformationLogCache.instance()
        uid = 'aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee'
        cache.append(uid, {
            'action': 'rewrite',
            'lifecycle': 'request',
            'target': 'url',
            'mode': agent_mode.MOCK,
            'details': 'first',
        })
        cache.append_many(uid, [
            {
                'action': 'filter',
                'lifecycle': 'request',
                'target': 'url',
                'mode': agent_mode.RECORD,
                'details': 'second',
            },
            {
                'action': 'filter',
                'lifecycle': 'request',
                'target': 'url',
                'mode': agent_mode.RECORD,
                'details': 'third',
            },
        ])
        rows = cache.read(uid)
        assert [r['details'] for r in rows] == ['first', 'second', 'third']

    def test_read_missing_returns_empty_list(self):
        cache = RequestTransformationLogCache.instance()
        assert cache.read('nonexistent-uuid') == []

    def test_append_log_from_request_skips_without_proxy_uuid_header(self):
        req = _mitm_request()
        append_log_from_request(req, {
            'action': 'rewrite',
            'lifecycle': 'request',
            'target': 'url',
            'mode': agent_mode.NONE,
            'details': 'x',
        })
        cache = RequestTransformationLogCache.instance()
        assert cache.read('00000000-0000-0000-0000-000000000099') == []

    def test_append_log_from_request_with_header(self):
        uid = '6ba7b810-9dad-11d1-80b4-00c04fd430c8'
        req = _mitm_request(**{custom_headers.PROXY_REQUEST_UUID: uid})
        append_log_from_request(req, {
            'action': 'rewrite',
            'lifecycle': 'response',
            'target': request_component.RESPONSE_HEADER,
            'mode': agent_mode.TEST,
            'details': 'rewriting header x => y',
        })
        cache = RequestTransformationLogCache.instance()
        rows = cache.read(uid)
        assert len(rows) == 1
        assert rows[0]['action'] == 'rewrite'
        assert rows[0]['lifecycle'] == 'response'
        assert rows[0]['target'] == request_component.RESPONSE_HEADER
        assert rows[0]['mode'] == agent_mode.TEST


class TestRequestTransformationEntryLoggerApi:
    def test_log_filter_exclude_writes_cache_after_flush(self):
        uid = '11111111-1111-1111-1111-111111111111'
        req = _mitm_request(**{custom_headers.PROXY_REQUEST_UUID: uid})
        isettings = InterceptSettings(Settings.instance(), req)
        RequestTransformationEntryLogger.log_filter_exclude(
            req, isettings, agent_mode.MOCK, str(req.url)
        )
        cache = RequestTransformationLogCache.instance()
        assert cache.read(uid) == []
        RequestTransformationEntryLogger.flush(req)
        rows = cache.read(uid)
        assert len(rows) == 1
        assert rows[0]['action'] == 'filter'
        assert rows[0]['lifecycle'] == 'request'
        assert rows[0]['target'] == 'url'
        assert rows[0]['details'].startswith('filtering (exclude) request ')
        assert rows[0]['mode'] == agent_mode.MOCK

    def test_log_filter_exclude_lifecycle_response_when_for_response(self):
        uid = 'aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee'
        req = _mitm_request(**{custom_headers.PROXY_REQUEST_UUID: uid})
        isettings = InterceptSettings(Settings.instance(), req)
        isettings.for_response()
        RequestTransformationEntryLogger.log_filter_exclude(
            req, isettings, agent_mode.MOCK, str(req.url)
        )
        RequestTransformationEntryLogger.flush(req)
        rows = RequestTransformationLogCache.instance().read(uid)
        assert len(rows) == 1
        assert rows[0]['lifecycle'] == 'response'
        assert rows[0]['details'].startswith('filtering (exclude) response ')

    def test_flush_emits_all_records_single_cache_write(self):
        uid = '22222222-2222-2222-2222-222222222222'
        req = _mitm_request(**{custom_headers.PROXY_REQUEST_UUID: uid})
        isettings = InterceptSettings(Settings.instance(), req)
        RequestTransformationEntryLogger.log_filter_exclude(
            req, isettings, agent_mode.MOCK, 'https://a'
        )
        RequestTransformationEntryLogger.log_filter_include_pattern_miss(
            req, isettings, agent_mode.RECORD, 'https://b'
        )
        cache = RequestTransformationLogCache.instance()
        assert cache.read(uid) == []
        RequestTransformationEntryLogger.flush(req)
        rows = cache.read(uid)
        assert len(rows) == 2
        assert 'filtering (exclude)' in rows[0]['details']
        assert 'filtering (not include)' in rows[1]['details']
        RequestTransformationEntryLogger.flush(req)
        assert len(cache.read(uid)) == 2

    def test_log_mocked_response_after_flush(self):
        uid = '33333333-3333-3333-3333-333333333333'
        req = _mitm_request(**{custom_headers.PROXY_REQUEST_UUID: uid})
        RequestTransformationEntryLogger.log_mocked_response(req, 'https://ex/a', 'req-key-1')
        cache = RequestTransformationLogCache.instance()
        RequestTransformationEntryLogger.flush(req)
        rows = cache.read(uid)
        assert len(rows) == 1
        assert rows[0]['action'] == 'rewrite'
        assert rows[0]['lifecycle'] == 'response'
        assert rows[0]['target'] == 'url'
        assert rows[0]['mode'] == agent_mode.MOCK
        assert 'mocked' in rows[0]['details']

    def test_log_testing_response_after_flush(self):
        uid = '44444444-4444-4444-4444-444444444444'
        req = _mitm_request(**{custom_headers.PROXY_REQUEST_UUID: uid})
        RequestTransformationEntryLogger.log_testing_response(req, 'rk', 'cli')
        cache = RequestTransformationLogCache.instance()
        RequestTransformationEntryLogger.flush(req)
        rows = cache.read(uid)
        assert len(rows) == 1
        assert rows[0]['action'] == 'noop'
        assert rows[0]['lifecycle'] == 'response'
        assert rows[0]['target'] == 'url'
        assert rows[0]['mode'] == agent_mode.TEST
        assert 'testing' in rows[0]['details']

    def test_log_recording_after_flush(self):
        uid = '55555555-5555-5555-5555-555555555555'
        req = _mitm_request(**{custom_headers.PROXY_REQUEST_UUID: uid})
        RequestTransformationEntryLogger.log_recording(req, str(req.url))
        cache = RequestTransformationLogCache.instance()
        RequestTransformationEntryLogger.flush(req)
        rows = cache.read(uid)
        assert len(rows) == 1
        assert rows[0]['action'] == 'noop'
        assert rows[0]['lifecycle'] == 'response'
        assert rows[0]['target'] == 'url'
        assert rows[0]['mode'] == agent_mode.RECORD
        assert 'recording' in rows[0]['details']
