from time import time
from urllib.parse import urlparse

import pytest
import requests
from mitmproxy.http import Headers, Request as MitmproxyRequest, Response as MitmproxyResponse

from stoobly_agent.app.models.factories.resource.local_db.helpers.request_builder import RequestBuilder
from stoobly_agent.app.models.factories.resource.local_db.request_adapter import LocalDBRequestAdapter
from stoobly_agent.app.models.request_model import RequestModel
from stoobly_agent.app.proxy.handle_record_service import handle_sse_record
from stoobly_agent.app.proxy.intercept_settings import InterceptSettings
from stoobly_agent.app.proxy.mitmproxy.flow_mock import MitmproxyFlowMock
from stoobly_agent.app.proxy.record.context import RecordContext
from stoobly_agent.app.proxy.record.sse_record_service import (
  SSE_RESPONSE_ID_KEY,
  finalize_sse_record,
  is_sse_flow,
  sse_body_from_chunks,
  start_sse_record,
)
from stoobly_agent.app.proxy.replay.body_parser_service import is_event_stream
from stoobly_agent.config.constants import custom_headers, mode, record_policy, stream_status
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.lib.orm.response import Response
from stoobly_agent.lib.orm.response_chunk import ResponseChunk
from stoobly_agent.test.sse_server import DEFAULT_EVENTS, SseServer
from stoobly_agent.test.test_helper import reset


def _mitmproxy_request_for_url(url: str, extra_headers: dict | None = None) -> MitmproxyRequest:
  parsed = urlparse(url)
  host = parsed.hostname or '127.0.0.1'
  port = parsed.port or (443 if parsed.scheme == 'https' else 80)
  path = parsed.path or '/'
  if parsed.query:
    path = f'{path}?{parsed.query}'
  authority = f'{host}:{port}'.encode()
  headers = Headers(**(extra_headers or {}))
  now = time()
  return MitmproxyRequest(
    host,
    port,
    b'GET',
    parsed.scheme.encode(),
    authority,
    path.encode(),
    b'HTTP/1.1',
    headers,
    b'',
    Headers(),
    now,
    now,
  )


def _sse_headers_response(content_type: str = 'text/event-stream') -> MitmproxyResponse:
  return MitmproxyResponse.make(
    200,
    b'',
    {
      'Content-Type': content_type,
      'Cache-Control': 'no-cache',
    },
  )


def _stream_server_into_tee(url: str, tee) -> bytes:
  """Read the live SSE upstream and feed each chunk through mitmproxy's stream tee."""
  received = b''
  with requests.get(url, stream=True, timeout=5) as res:
    assert res.status_code == 200
    assert is_event_stream(res.headers.get('Content-Type'))
    for chunk in res.iter_content(chunk_size=None):
      if not chunk:
        continue
      received += chunk
      out = tee(chunk)
      assert out == [chunk]
  tee(b'')
  return received


class TestIsEventStream:
  def test_matches_text_event_stream(self):
    assert is_event_stream('text/event-stream')
    assert is_event_stream('text/event-stream; charset=utf-8')

  def test_rejects_other_types(self):
    assert not is_event_stream('application/json')
    assert not is_event_stream('')
    assert not is_event_stream(None)


class TestSseServer:
  def test_serves_default_events(self):
    with SseServer(interval=0.0) as server:
      with requests.get(server.url, stream=True, timeout=5) as res:
        assert res.status_code == 200
        assert 'text/event-stream' in res.headers['Content-Type']
        body = b''.join(res.iter_content(chunk_size=None))

    assert body == b''.join(DEFAULT_EVENTS)

  def test_serves_custom_events(self):
    events = (b'data: a\n\n', b'data: b\n\n')
    with SseServer(events=events, interval=0.0) as server:
      body = requests.get(server.url, timeout=5).content
    assert body == b''.join(events)


class TestResponseChunksMock:
  @pytest.fixture(autouse=True, scope='class')
  @classmethod
  def settings(cls):
    return reset()

  @pytest.fixture
  def sse_request(self, settings):
    status = RequestBuilder(
      method='GET',
      request_body='',
      request_headers={},
      response_body='',
      response_headers={'Content-Type': 'text/event-stream'},
      status_code=200,
      url='https://example.com/events',
    ).with_settings(settings).build()[1]
    assert status == 200
    request = Request.last()
    response = request.response
    response.update(stream_status=stream_status.COMPLETE)
    ResponseChunk.create(response_id=response.id, sequence=0, payload=b'data: one\n\n')
    ResponseChunk.create(response_id=response.id, sequence=1, payload=b'data: two\n\n')
    yield request
    request.delete()

  def test_sse_body_from_chunks_concatenates_in_order(self, sse_request: Request):
    body = sse_body_from_chunks(sse_request.response)
    assert body == b'data: one\n\ndata: two\n\n'

  def test_raw_stays_without_chunk_payloads(self, sse_request: Request):
    raw = sse_request.response.raw or b''
    assert b'data: one' not in raw
    assert b'data: two' not in raw

  def test_mock_serves_chunks_as_body(self, sse_request: Request):
    adapter = LocalDBRequestAdapter(request_orm=Request, response_orm=Response)
    response = adapter.response(request_id=sse_request.id)
    assert response.status_code == 200
    assert response.content == b'data: one\n\ndata: two\n\n'
    assert 'event-stream' in (response.headers.get('Content-Type') or '').lower()
    assert response.headers.get(custom_headers.MOCK_REQUEST_ID) == str(sse_request.id)


class TestSseRecordFromServer:
  @pytest.fixture(autouse=True)
  def settings(self):
    return reset('stoobly-agent-sse-record-test')

  @pytest.fixture
  def sse_server(self):
    with SseServer(interval=0.0) as server:
      yield server

  def test_is_sse_flow_detects_server_headers(self, sse_server: SseServer):
    flow = MitmproxyFlowMock()
    flow.request = _mitmproxy_request_for_url(sse_server.url)
    flow.response = _sse_headers_response()
    assert is_sse_flow(flow)

  def test_start_sse_record_tees_live_server_chunks(self, settings, sse_server: SseServer):
    flow = MitmproxyFlowMock()
    flow.request = _mitmproxy_request_for_url(
      sse_server.url,
      {
        custom_headers.PROXY_MODE: mode.RECORD,
        custom_headers.RECORD_POLICY: record_policy.ALL,
      },
    )
    flow.response = _sse_headers_response()

    intercept_settings = InterceptSettings(settings, flow.request)
    request_model = RequestModel(settings)

    response_record = start_sse_record(flow, request_model, intercept_settings)
    assert response_record is not None
    assert flow.metadata.get(SSE_RESPONSE_ID_KEY) == response_record.id
    assert callable(flow.response.stream)

    expected = b''.join(DEFAULT_EVENTS)
    received = _stream_server_into_tee(sse_server.url, flow.response.stream)
    assert received == expected

    response_record = Response.find(response_record.id)
    assert response_record.stream_status == stream_status.COMPLETE
    chunks = ResponseChunk.where('response_id', response_record.id).order_by('sequence', 'asc').get()
    # Network/read boundaries may coalesce events; content must match, not chunk count.
    assert len(chunks) >= 1
    assert b''.join(c.payload or b'' for c in chunks) == expected
    assert b'data: hello' not in (response_record.raw or b'')
    assert sse_body_from_chunks(response_record) == expected

  def test_handle_sse_record_starts_tee(self, settings, sse_server: SseServer):
    flow = MitmproxyFlowMock()
    flow.request = _mitmproxy_request_for_url(
      sse_server.url,
      {
        custom_headers.PROXY_MODE: mode.RECORD,
        custom_headers.RECORD_POLICY: record_policy.ALL,
      },
    )
    flow.response = _sse_headers_response()

    intercept_settings = InterceptSettings(settings, flow.request)
    handle_sse_record(RecordContext(flow, intercept_settings))

    assert flow.metadata.get(SSE_RESPONSE_ID_KEY)
    assert callable(flow.response.stream)

    expected = b''.join(DEFAULT_EVENTS)
    received = _stream_server_into_tee(sse_server.url, flow.response.stream)
    assert received == expected
    finalize_sse_record(flow)

    response = Response.find(flow.metadata[SSE_RESPONSE_ID_KEY])
    assert response.stream_status == stream_status.COMPLETE
    chunks = ResponseChunk.where('response_id', response.id).order_by('sequence', 'asc').get()
    assert len(chunks) >= 1
    assert b''.join(c.payload or b'' for c in chunks) == expected

  def test_handle_sse_record_passthrough_when_policy_none(
    self, settings, sse_server: SseServer
  ):
    flow = MitmproxyFlowMock()
    flow.request = _mitmproxy_request_for_url(
      sse_server.url,
      {
        custom_headers.PROXY_MODE: mode.RECORD,
        custom_headers.RECORD_POLICY: record_policy.NONE,
      },
    )
    flow.response = _sse_headers_response()

    intercept_settings = InterceptSettings(settings, flow.request)
    handle_sse_record(RecordContext(flow, intercept_settings))

    # No tee; passthrough is owned by intercept_handler.responseheaders.
    assert flow.metadata.get(SSE_RESPONSE_ID_KEY) is None
    assert not callable(getattr(flow.response, 'stream', None))

  def test_start_sse_record_skips_remote_request_model(self, settings, sse_server: SseServer):
    flow = MitmproxyFlowMock()
    flow.request = _mitmproxy_request_for_url(
      sse_server.url,
      {
        custom_headers.PROXY_MODE: mode.RECORD,
        custom_headers.RECORD_POLICY: record_policy.ALL,
      },
    )
    flow.response = _sse_headers_response()
    flow.response.stream = True

    intercept_settings = InterceptSettings(settings, flow.request)
    request_model = RequestModel(settings)
    request_model.is_local = False

    assert start_sse_record(flow, request_model, intercept_settings) is None
    assert flow.metadata.get(SSE_RESPONSE_ID_KEY) is None
    assert flow.response.stream is True
