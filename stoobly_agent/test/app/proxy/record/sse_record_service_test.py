import pytest

from stoobly_agent.app.models.factories.resource.local_db.helpers.request_builder import RequestBuilder
from stoobly_agent.app.models.factories.resource.local_db.request_adapter import LocalDBRequestAdapter
from stoobly_agent.app.proxy.record.sse_record_service import sse_body_from_chunks
from stoobly_agent.app.proxy.replay.body_parser_service import is_event_stream
from stoobly_agent.config.constants import custom_headers, stream_status
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.lib.orm.response import Response
from stoobly_agent.lib.orm.response_chunk import ResponseChunk
from stoobly_agent.test.test_helper import reset


class TestIsEventStream:
  def test_matches_text_event_stream(self):
    assert is_event_stream('text/event-stream')
    assert is_event_stream('text/event-stream; charset=utf-8')

  def test_rejects_other_types(self):
    assert not is_event_stream('application/json')
    assert not is_event_stream('')
    assert not is_event_stream(None)


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
