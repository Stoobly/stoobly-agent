import os

import pytest

from stoobly_agent.app.models.factories.resource.local_db.helpers.request_snapshot import (
  MalformedRequestSnapshotError,
  RequestSnapshot,
  RequestSnapshotV1,
  RequestSnapshotV2,
)
from stoobly_agent.app.models.factories.resource.local_db.helpers.snapshot_format import FORMAT_V1, FORMAT_V2
from stoobly_agent.app.proxy.record.joined_request import REQUEST_DELIMITTER
from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.test.test_helper import reset


@pytest.fixture(autouse=True)
def settings():
  return reset()


UUID = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'
UUID_B = 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb'


def _joined(marker: bytes = b'x', uuid: str = UUID) -> bytes:
  request = b'GET /api HTTP/1.1\r\nHost: example.com\r\n\r\n' + marker
  response = b'HTTP/1.1 200\r\nContent-Length: 0\r\n\r\n'
  return REQUEST_DELIMITTER.join([
    f'1 {uuid} 1\r\n'.encode() + request,
    f'2 {uuid} 1 1\r\n'.encode() + response,
  ])


def _write_v2_file(snapshot: RequestSnapshotV2, payload: bytes = None):
  """Write a valid v2 YAML request snapshot (or raw bytes for malformed-path tests)."""
  path = snapshot.path
  snapshot._ensure_parent(path)
  if payload is None:
    snapshot.write_raw(_joined(b'', uuid=snapshot.uuid))
    return path
  with open(path, 'wb') as fp:
    fp.write(payload)
  return path


class TestRequestSnapshotParseRef:
  def test_slug_uuid(self):
    parsed_uuid, parsed_slug = RequestSnapshot._parse_request_ref(f'GET-api/{UUID}')
    assert parsed_uuid == UUID
    assert parsed_slug == 'GET-api'

  def test_slug_uuid_with_http_suffix(self):
    parsed_uuid, parsed_slug = RequestSnapshot._parse_request_ref(f'GET-api/{UUID}.yaml')
    assert parsed_uuid == UUID
    assert parsed_slug == 'GET-api'

  def test_bare_uuid(self):
    parsed_uuid, parsed_slug = RequestSnapshot._parse_request_ref(UUID)
    assert parsed_uuid == UUID
    assert parsed_slug is None


class TestRequestSnapshotCreateAndFromPath:
  def test_create_with_slug_is_v2(self):
    snapshot = RequestSnapshot.create(UUID, slug='GET-api')
    assert isinstance(snapshot, RequestSnapshotV2)
    assert snapshot.format == FORMAT_V2
    assert snapshot.slug == 'GET-api'

  def test_create_detects_v1_shard(self):
    data_dir = DataDir.instance()
    v1 = RequestSnapshotV1(UUID, data_dir)
    v1.write_raw(b'v1-bytes')

    snapshot = RequestSnapshot.create(UUID, data_dir)
    assert isinstance(snapshot, RequestSnapshotV1)
    assert snapshot.request == b'v1-bytes'

  def test_create_detects_v2_http(self):
    data_dir = DataDir.instance()
    v2 = RequestSnapshotV2(UUID, data_dir, slug='GET-api')
    # Empty bodies so externalize/reconstitute is a pure round-trip
    original = _joined(b'')
    v2.write_raw(original)

    snapshot = RequestSnapshot.create(UUID, data_dir)
    assert isinstance(snapshot, RequestSnapshotV2)
    assert snapshot.format == FORMAT_V2
    assert snapshot.path.endswith(f'GET-api/{UUID}.yaml')
    assert snapshot.request == original

  def test_from_path_v2(self):
    data_dir = DataDir.instance()
    v2 = RequestSnapshotV2(UUID, data_dir, slug='GET-api')
    _write_v2_file(v2)

    snapshot = RequestSnapshot.from_path(v2.path, data_dir)
    assert isinstance(snapshot, RequestSnapshotV2)
    assert snapshot.uuid == UUID
    assert snapshot.slug == 'GET-api'

  def test_from_path_v1(self):
    data_dir = DataDir.instance()
    v1 = RequestSnapshotV1(UUID, data_dir)
    v1.write_raw(b'v1-bytes')

    snapshot = RequestSnapshot.from_path(v1.path, data_dir)
    assert isinstance(snapshot, RequestSnapshotV1)
    assert snapshot.uuid == UUID

  def test_from_path_outside_requests_dir(self):
    data_dir = DataDir.instance()
    outside = os.path.join(data_dir.path, 'outside.yaml')
    with open(outside, 'wb') as fp:
      fp.write(b'x')
    assert RequestSnapshot.from_path(outside, data_dir) is None


class TestRequestSnapshotV2PathAndWrite:
  def test_path_without_slug_is_none_until_written(self):
    snapshot = RequestSnapshotV2(UUID)
    assert snapshot.path is None

  def test_write_raw_without_path_raises(self):
    snapshot = RequestSnapshotV2(UUID)
    with pytest.raises(ValueError, match='missing path'):
      snapshot.write_raw(b'x')

  def test_backup_and_rollback(self):
    snapshot = RequestSnapshotV2(UUID, slug='GET-api')
    _write_v2_file(snapshot, b'original')
    snapshot.backup()

    _write_v2_file(snapshot, b'changed')
    with open(snapshot.path, 'rb') as fp:
      assert fp.read() == b'changed'

    snapshot.rollback()
    with open(snapshot.path, 'rb') as fp:
      assert fp.read() == b'original'

  def test_find_v2_path_with_slug_missing_does_not_glob(self):
    old = RequestSnapshotV2(UUID, slug='GET-api')
    old_path = _write_v2_file(old)

    snap = RequestSnapshotV2(UUID, slug='POST-api')
    assert snap._find_v2_path() is None
    assert snap.path.endswith(f'POST-api/{UUID}.yaml')
    assert snap.path != old_path

  def test_find_v2_path_without_slug_still_globs(self):
    old = RequestSnapshotV2(UUID, slug='GET-api')
    old_path = _write_v2_file(old)

    snap = RequestSnapshotV2(UUID)
    assert snap._find_v2_path() == old_path

  def test_write_after_slug_change_uses_new_path_and_removes_orphan(self):
    old = RequestSnapshotV2(UUID, slug='GET-api')
    old_path = _write_v2_file(old, b'old')
    old_slug_dir = os.path.dirname(old_path)

    # Simulate write(): new method/path slug, clear resolved path
    snap = RequestSnapshotV2(UUID, slug='GET-api')
    snap._slug = RequestSnapshotV2.build_request_slug('POST', '/api')
    snap._resolved_path = None
    snap.write_raw(_joined(b''))

    new_path = snap.path
    assert new_path.endswith(f'POST-api/{UUID}.yaml')
    assert os.path.exists(new_path)
    assert not os.path.exists(old_path)
    assert not os.path.isdir(old_slug_dir)


class TestRequestSnapshotV2SlugTraversal:
  def test_constructor_slug_with_dotdot_stays_under_requests(self):
    data_dir = DataDir.instance()
    requests_dir = data_dir.snapshots_requests_dir_path
    snapshot = RequestSnapshotV2(UUID, data_dir, slug='../outside')

    path = snapshot.path
    assert path is not None
    assert os.path.commonpath([requests_dir, os.path.normpath(path)]) == os.path.normpath(requests_dir)
    assert snapshot.slug == RequestSnapshotV2.sanitize_request_slug('../outside')
    assert '..' not in path.split(os.sep)

  def test_history_style_ref_with_traversal_stays_under_requests(self):
    data_dir = DataDir.instance()
    requests_dir = data_dir.snapshots_requests_dir_path
    snapshot = RequestSnapshot.create(f'../../tmp/{UUID}.yaml', data_dir)

    assert isinstance(snapshot, RequestSnapshotV2)
    path = snapshot.path
    assert os.path.commonpath([requests_dir, os.path.normpath(path)]) == os.path.normpath(requests_dir)

  def test_remove_with_traversal_slug_does_not_delete_outside(self):
    data_dir = DataDir.instance()
    requests_dir = data_dir.snapshots_requests_dir_path
    # Unsanitized join(requests, '..', uuid.yaml) would land here
    outside = os.path.normpath(os.path.join(requests_dir, '..', f'{UUID}.yaml'))
    with open(outside, 'wb') as fp:
      fp.write(b'secret')

    snapshot = RequestSnapshotV2(UUID, data_dir, slug='..')
    assert snapshot.slug == 'GET'  # sanitized away from '..'
    snapshot.remove()
    assert os.path.isfile(outside)

  def test_wildcard_uuid_does_not_glob_other_snapshots(self):
    data_dir = DataDir.instance()
    victim = RequestSnapshotV2(UUID, data_dir, slug='GET-api')
    victim_path = _write_v2_file(victim, b'keep-me')

    # Bare '*' would expand glob .../requests/*/*.yaml to the victim
    wildcard = RequestSnapshotV2('*', data_dir)
    assert wildcard._find_v2_path() is None
    assert wildcard.path is None
    wildcard.remove()
    assert os.path.isfile(victim_path)

  def test_history_style_wildcard_ref_does_not_remove_other_snapshots(self):
    data_dir = DataDir.instance()
    victim = RequestSnapshotV2(UUID, data_dir, slug='GET-api')
    victim_path = _write_v2_file(victim, b'keep-me')

    # slug/*.yaml parses to uuid='*'; must not glob-match victim
    snapshot = RequestSnapshot.create('slug/*.yaml', data_dir)
    assert isinstance(snapshot, RequestSnapshotV2)
    assert snapshot.uuid == '*'
    snapshot.remove()
    assert os.path.isfile(victim_path)

class TestRequestSnapshotV2NamingEdges:
  def test_parse_relative_path_invalid(self):
    assert RequestSnapshotV2.parse_request_relative_path('only-one-part') is None
    assert RequestSnapshotV2.parse_request_relative_path('slug/uuid.txt') is None
    assert RequestSnapshotV2.parse_request_relative_path('/uuid.yaml') is None
    assert RequestSnapshotV2.parse_request_relative_path('slug/.yaml') is None

  def test_cleanup_empty_slug_dir_after_remove(self):
    snapshot = RequestSnapshotV2(UUID, slug='GET-cleanup')
    _write_v2_file(snapshot)
    slug_dir = os.path.dirname(snapshot.path)
    assert os.path.isdir(slug_dir)

    snapshot.remove()
    assert not os.path.isdir(slug_dir)

  def test_cleanup_keeps_slug_dir_when_other_http_remains(self):
    first = RequestSnapshotV2(UUID, slug='GET-shared')
    second = RequestSnapshotV2(UUID_B, slug='GET-shared')
    _write_v2_file(first, b'one')
    _write_v2_file(second, b'two')
    slug_dir = os.path.dirname(first.path)

    first.remove()
    assert os.path.isdir(slug_dir)
    assert os.path.isfile(second.path)

  def test_malformed_contents_raise(self):
    snapshot = RequestSnapshotV2(UUID, slug='GET-bad')
    _write_v2_file(snapshot, b'junk')

    with pytest.raises(MalformedRequestSnapshotError, match='Malformed request snapshot') as exc:
      _ = snapshot.request

    assert snapshot.path in str(exc.value)

  def test_copy_refs_skips_unsafe_refs(self, tmp_path):
    import yaml

    from stoobly_agent.config.constants.custom_headers import BODY_REF, HEADER_REF

    snapshot = RequestSnapshotV2(UUID, slug='GET-copy')
    path = snapshot.path
    snapshot._ensure_parent(path)
    slug_dir = os.path.dirname(path)
    bodies_dir = os.path.join(slug_dir, 'bodies')
    headers_dir = os.path.join(slug_dir, 'headers')
    os.makedirs(bodies_dir, exist_ok=True)
    os.makedirs(headers_dir, exist_ok=True)

    safe_body_hash = 'a' * 16
    safe_header_hash = 'b' * 16
    with open(os.path.join(bodies_dir, safe_body_hash), 'wb') as fp:
      fp.write(b'safe-body')
    with open(os.path.join(headers_dir, safe_header_hash), 'wb') as fp:
      fp.write(b'User-Agent: ua')

    entry = {
      'method': 'GET',
      'url': 'https://example.com/',
      'http_version': '1.1',
      'timestamp': 1,
      'headers': {
        HEADER_REF: f'.stoobly/snapshots/requests/GET-copy/headers/{safe_header_hash}',
        'X-Bad-Header-Ref': '../outside-header',
        BODY_REF: f'.stoobly/snapshots/requests/GET-copy/bodies/{safe_body_hash}',
      },
      'response': {
        'status': 200,
        'latency': 0,
        'http_version': '1.1',
        'timestamp': 1,
        'headers': {
          BODY_REF: '../outside-secret',
          'X-Bad-Body': '/etc/passwd',
        },
      },
    }
    # Include unsafe refs under the real BODY_REF/HEADER_REF keys as alternate entries
    entry['response']['headers'][BODY_REF] = '../outside-secret'
    with open(path, 'w') as fp:
      yaml.safe_dump(entry, fp)
    snapshot._entry = entry
    snapshot._resolved_path = path

    dest = tmp_path / 'dest'
    dest.mkdir()
    snapshot.copy(str(dest))

    # Safe refs copied; absolute/traversal refs skipped
    copied_bodies = list(dest.rglob(safe_body_hash))
    assert len(copied_bodies) == 1
    assert copied_bodies[0].read_bytes() == b'safe-body'
    copied_headers = list(dest.rglob(safe_header_hash))
    assert len(copied_headers) == 1
    assert copied_headers[0].read_bytes() == b'User-Agent: ua'
    assert not list(dest.rglob('outside-secret'))
    assert not list(dest.rglob('outside-header'))
    assert not list(dest.rglob('passwd'))
