import os
import tempfile

import pytest

from stoobly_agent.app.models.adapters.joined_request_adapter import JoinedRequestAdapter
from stoobly_agent.app.models.factories.resource.local_db.helpers.body_ref import (
  BODY_REF_HEADER,
  bodies_dir_path,
  content_hash,
  full_content_hash,
  normalize_body_ref,
  read_body,
  relative_body_ref,
  resolve_body_path,
  write_body,
)
from stoobly_agent.config.data_dir import DATA_DIR_NAME
from stoobly_agent.app.models.factories.resource.local_db.helpers.joined_request_ref import (
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
      body_names = os.listdir(bodies)
      assert len(body_names) == 2
      assert all(len(name) == 16 for name in body_names)

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

  def test_write_body_dedupes_identical_content(self):
    with tempfile.TemporaryDirectory() as slug_dir:
      h1 = write_body(slug_dir, b'same')
      h2 = write_body(slug_dir, b'same')
      assert h1 == h2
      assert len(h1) == 16
      assert len(os.listdir(bodies_dir_path(slug_dir))) == 1

  def test_write_body_truncated_collision_falls_back_to_full_digest(self):
    with tempfile.TemporaryDirectory() as root:
      slug_dir = os.path.join(root, 'GET-api')
      os.makedirs(slug_dir)
      body = b'unique-body-payload'
      short = content_hash(body)
      bodies = bodies_dir_path(slug_dir)
      os.makedirs(bodies)
      with open(os.path.join(bodies, short), 'wb') as fp:
        fp.write(b'planted-different-bytes')

      hash_value = write_body(slug_dir, body)
      assert hash_value == full_content_hash(body)
      assert len(hash_value) == 64
      assert read_body(slug_dir, relative_body_ref('GET-api', hash_value)) == body
      # Original short-hash file left untouched
      with open(os.path.join(bodies, short), 'rb') as fp:
        assert fp.read() == b'planted-different-bytes'

  def test_relative_body_ref_is_context_relative(self):
    assert relative_body_ref('GET-api', 'abc') == (
      f'{DATA_DIR_NAME}/snapshots/requests/GET-api/bodies/abc'
    )

  def test_normalize_accepts_context_relative_form(self):
    long_ref = f'{DATA_DIR_NAME}/snapshots/requests/GET-api/bodies/abc'
    assert normalize_body_ref(long_ref) == long_ref
    assert normalize_body_ref(long_ref, slug='GET-api') == long_ref

  def test_normalize_rejects_traversal_and_absolute(self):
    for bad in (
      '/etc/passwd',
      'bodies/abc',
      'bodies/../secret',
      '../bodies/abc',
      'etc/passwd',
      '',
      f'{DATA_DIR_NAME}/snapshots/requests/GET-api/../bodies/abc',
      f'{DATA_DIR_NAME}/snapshots/requests/other/bodies/abc',
    ):
      with pytest.raises(ValueError, match='Invalid body ref'):
        normalize_body_ref(bad, slug='GET-api')

  def test_resolve_stays_under_slug_dir(self):
    with tempfile.TemporaryDirectory() as root:
      slug_dir = os.path.join(root, 'GET-api')
      os.makedirs(slug_dir)
      long_ref = relative_body_ref('GET-api', 'deadbeef')
      path = resolve_body_path(slug_dir, long_ref)
      assert path.startswith(slug_dir)
      assert path.endswith(os.path.join('bodies', 'deadbeef'))

  def test_resolve_rejects_slug_mismatch(self):
    with tempfile.TemporaryDirectory() as root:
      slug_dir = os.path.join(root, 'GET-api')
      os.makedirs(slug_dir)
      with pytest.raises(ValueError, match='Invalid body ref'):
        resolve_body_path(
          slug_dir, relative_body_ref('POST-other', 'deadbeef')
        )

  def test_resolve_rejects_symlink_escape(self):
    with tempfile.TemporaryDirectory() as root:
      slug_dir = os.path.join(root, 'GET-api')
      bodies = os.path.join(slug_dir, 'bodies')
      os.makedirs(bodies)
      target = os.path.join(slug_dir, 'outside-secret')
      with open(target, 'wb') as fp:
        fp.write(b'secret')
      link = os.path.join(bodies, 'deadbeef')
      os.symlink(target, link)

      with pytest.raises(ValueError, match='Invalid body ref'):
        resolve_body_path(slug_dir, relative_body_ref('GET-api', 'deadbeef'))

  def test_resolve_rejects_bodies_dir_symlink_escape(self):
    with tempfile.TemporaryDirectory() as root:
      slug_dir = os.path.join(root, 'slug')
      os.makedirs(slug_dir)
      outside = os.path.join(root, 'outside')
      os.makedirs(outside)
      os.symlink(outside, os.path.join(slug_dir, 'bodies'))

      with pytest.raises(ValueError, match='Invalid body ref'):
        resolve_body_path(slug_dir, relative_body_ref('slug', 'deadbeef'))

  def test_externalize_writes_context_relative_refs(self):
    joined = _joined_with_bodies(b'hello', b'world')
    with tempfile.TemporaryDirectory() as root:
      slug_dir = os.path.join(root, 'GET-api-test')
      os.makedirs(slug_dir)
      externalized = externalize_joined_request(joined, slug_dir)
      prefix = f'{DATA_DIR_NAME}/snapshots/requests/GET-api-test/bodies/'.encode()
      assert prefix in externalized
