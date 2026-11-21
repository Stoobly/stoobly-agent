import os
import tempfile

from stoobly_agent.app.models.adapters.joined_request_adapter import JoinedRequestAdapter
from stoobly_agent.app.models.factories.resource.local_db.helpers.body_ref import (
  BODY_REF_HEADER,
  externalize_joined_request,
  reconstitute_joined_request,
)
from stoobly_agent.app.proxy.record.joined_request import REQUEST_DELIMITTER


def _joined_with_bodies(request_body: bytes, response_body: bytes) -> bytes:
  request = (
    b'GET /api/test HTTP/1.1\r\n'
    b'Host: example.com\r\n'
    b'Content-Length: ' + str(len(request_body)).encode() + b'\r\n'
    b'\r\n' + request_body
  )
  response = (
    b'HTTP/1.1 200 OK\r\n'
    b'Content-Length: ' + str(len(response_body)).encode() + b'\r\n'
    b'\r\n' + response_body
  )
  control_req = b'1 id 1'
  control_res = b'2 id 1 1'
  return REQUEST_DELIMITTER.join([
    control_req + b'\r\n' + request,
    control_res + b'\r\n' + response,
  ])


class TestBodyRef:
  def test_externalize_and_reconstitute_round_trip(self):
    joined = _joined_with_bodies(b'hello', b'world!!!')
    with tempfile.TemporaryDirectory() as slug_dir:
      externalized = externalize_joined_request(joined, slug_dir)

      assert BODY_REF_HEADER.encode() in externalized
      assert b'hello' not in externalized
      assert b'world!!!' not in externalized

      bodies = os.path.join(slug_dir, 'bodies')
      assert os.path.isdir(bodies)
      assert len(os.listdir(bodies)) == 2

      restored = reconstitute_joined_request(externalized, slug_dir)
      assert restored == joined

  def test_empty_bodies_unchanged(self):
    joined = _joined_with_bodies(b'', b'')
    with tempfile.TemporaryDirectory() as slug_dir:
      externalized = externalize_joined_request(joined, slug_dir)
      # Empty request/response bodies should not add body refs
      assert BODY_REF_HEADER.encode() not in externalized
      restored = reconstitute_joined_request(externalized, slug_dir)
      assert restored == joined

  def test_body_ref_is_last_header(self):
    joined = _joined_with_bodies(b'x', b'y')
    with tempfile.TemporaryDirectory() as slug_dir:
      externalized = externalize_joined_request(joined, slug_dir)
      adapter = JoinedRequestAdapter(externalized)
      response_raw = adapter.build_response_string().get(control=False)
      head, _ = response_raw.split(b'\r\n\r\n', 1)
      header_lines = head.split(b'\r\n')[1:]
      assert header_lines[-1].lower().startswith(BODY_REF_HEADER.lower().encode())
