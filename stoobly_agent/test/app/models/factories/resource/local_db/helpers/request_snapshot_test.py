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


def _joined(marker: bytes = b'x') -> bytes:
  request = b'GET /api HTTP/1.1\r\nHost: example.com\r\n\r\n' + marker
  response = b'HTTP/1.1 200 OK\r\nContent-Length: 0\r\n\r\n'
  return REQUEST_DELIMITTER.join([b'1 id 1\r\n' + request, b'2 id 1 1\r\n' + response])


def _write_v2_file(snapshot: RequestSnapshotV2, payload: bytes = b'raw-on-disk'):
  path = snapshot.path
  snapshot._ensure_parent(path)
  with open(path, 'wb') as fp:
    fp.write(payload)
  return path


class TestRequestSnapshotParseRef:
  def test_slug_uuid(self):
    parsed_uuid, parsed_slug = RequestSnapshot._parse_request_ref(f'GET-api/{UUID}')
    assert parsed_uuid == UUID
    assert parsed_slug == 'GET-api'

  def test_slug_uuid_with_http_suffix(self):
    parsed_uuid, parsed_slug = RequestSnapshot._parse_request_ref(f'GET-api/{UUID}.http')
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
    assert snapshot.path.endswith(f'GET-api/{UUID}.http')
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
    outside = os.path.join(data_dir.path, 'outside.http')
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


class TestRequestSnapshotV2NamingEdges:
  def test_parse_relative_path_invalid(self):
    assert RequestSnapshotV2.parse_request_relative_path('only-one-part') is None
    assert RequestSnapshotV2.parse_request_relative_path('slug/uuid.txt') is None
    assert RequestSnapshotV2.parse_request_relative_path('/uuid.http') is None
    assert RequestSnapshotV2.parse_request_relative_path('slug/.http') is None

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
