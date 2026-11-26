import os

import pytest

from stoobly_agent.app.models.factories.resource.local_db.helpers.request_builder import RequestBuilder
from stoobly_agent.app.models.factories.resource.local_db.helpers.request_snapshot import RequestSnapshot
from stoobly_agent.app.models.helpers.apply import Apply
from stoobly_agent.config.constants import stream_status
from stoobly_agent.config.constants.custom_headers import CHUNK_REF
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.lib.orm.response_chunk import ResponseChunk
from stoobly_agent.test.test_helper import reset


class TestSseSnapshotChunks:
  @pytest.fixture(autouse=True)
  def settings(self):
    return reset()

  @pytest.fixture
  def sse_request(self, settings):
    status = RequestBuilder(
      method='GET',
      request_body='',
      request_headers={},
      response_body='',
      response_headers={'Content-Type': 'text/event-stream', 'Cache-Control': 'no-cache'},
      status_code=200,
      url='https://example.com/sse',
    ).with_settings(settings).build()[1]
    assert status == 200
    request = Request.last()
    response = request.response
    response.update(stream_status=stream_status.COMPLETE)
    ResponseChunk.create(response_id=response.id, sequence=0, payload=b'data: hello\n\n')
    ResponseChunk.create(response_id=response.id, sequence=1, payload=b'data: world\n\n')
    yield request
    request.delete()

  def test_snapshot_write_emits_chunk_ref_and_files(self, sse_request: Request):
    from stoobly_agent.app.models.factories.resource.local_db.helpers.chunk_ref import (
      content_hash,
    )

    snapshot = RequestSnapshot.create(sse_request.uuid)
    snapshot.write(sse_request)

    entry = snapshot.entry
    assert entry is not None
    headers = (entry.get('response') or {}).get('headers') or ''
    assert CHUNK_REF in headers
    # One Chunk-Ref header per chunk; Content-Type may be under Header-Ref.
    chunk_lines = [
      line for line in headers.splitlines()
      if line.lower().startswith(CHUNK_REF.lower() + ':')
    ]
    assert len(chunk_lines) == 2

    slug_dir = snapshot.slug_dir
    chunks_dir = os.path.join(slug_dir, 'chunks')
    assert os.path.isdir(chunks_dir)
    expected = sorted([content_hash(b'data: hello\n\n'), content_hash(b'data: world\n\n')])
    assert sorted(os.listdir(chunks_dir)) == expected

    with open(os.path.join(chunks_dir, content_hash(b'data: hello\n\n')), 'rb') as fp:
      assert fp.read() == b'data: hello\n\n'

    # Envelope raw in ORM must not contain chunk payloads
    assert b'data: hello' not in (sse_request.response.raw or b'')

  def test_apply_recreates_response_chunks(self, sse_request: Request, settings):
    snapshot = RequestSnapshot.create(sse_request.uuid)
    snapshot.write(sse_request)
    uuid = sse_request.uuid
    response_id = sse_request.response.id

    # Delete ORM request so apply recreates from snapshot
    sse_request.delete()
    assert Request.find_by(uuid=uuid) is None

    result = Apply().request(uuid)
    assert result is not False

    restored = Request.find_by(uuid=uuid)
    assert restored is not None
    response = restored.response
    assert response.stream_status == stream_status.COMPLETE
    chunks = ResponseChunk.where('response_id', response.id).order_by('sequence', 'asc').get()
    assert len(chunks) == 2
    assert chunks[0].payload == b'data: hello\n\n'
    assert chunks[1].payload == b'data: world\n\n'
    assert b'data: hello' not in (response.raw or b'')

    restored.delete()
