import tempfile

import yaml

from stoobly_agent.app.models.adapters.raw_joined import (
  RawJoinedRequestAdapterFactory,
  RawJoinedResponseAdapterFactory,
  SnapshotEntryAdapter,
)
from stoobly_agent.app.models.adapters.snapshot import SnapshotAdapterFactory
from stoobly_agent.app.proxy.record.joined_request import REQUEST_DELIMITTER

REQ_TS_NS = 1795066190943834368
RES_TS_NS = 1795066190944042000
RES_TS_US_LEGACY = 1795066190944042


def _joined(req_ts: int, res_ts: int) -> bytes:
  request = b'GET https://example.com/api HTTP/1.1\r\nHost: example.com\r\n\r\n'
  response = b'HTTP/1.1 200\r\nContent-Length: 0\r\n\r\n'
  return REQUEST_DELIMITTER.join([
    f'1 req-id {req_ts}'.encode() + b'\r\n' + request,
    f'2 req-id {res_ts} 42'.encode() + b'\r\n' + response,
  ])


class TestSnapshotEntryAdapter:
  def test_adapt_writes_iso_timestamps(self):
    entry = SnapshotEntryAdapter(_joined(REQ_TS_NS, RES_TS_NS)).adapt()
    assert entry['method'] == 'GET'
    assert entry['url'] == 'https://example.com/api'
    assert entry['http_version'] == '1.1'
    assert entry['timestamp'] == '2026-11-19T05:29:50.943834368Z'
    assert entry['headers'] == 'Host: example.com'
    assert entry['response']['status'] == 200
    assert entry['response']['latency'] == 42
    assert entry['response']['timestamp'] == '2026-11-19T05:29:50.944042Z'

  def test_legacy_us_response_formats_as_same_iso(self):
    entry = SnapshotEntryAdapter(_joined(REQ_TS_NS, RES_TS_US_LEGACY)).adapt()
    assert entry['response']['timestamp'] == '2026-11-19T05:29:50.944042Z'

  def test_round_trip_with_snapshot_adapter_factory(self):
    original = _joined(REQ_TS_NS, RES_TS_NS)
    entry = SnapshotEntryAdapter(original).adapt()
    restored = SnapshotAdapterFactory(entry, uuid='req-id').joined_request()
    assert restored == original

  def test_from_joined_with_slug_dir_round_trip(self):
    with tempfile.TemporaryDirectory() as slug_dir:
      entry = SnapshotEntryAdapter.from_joined(
        _joined(REQ_TS_NS, RES_TS_NS), slug_dir
      ).adapt()
      restored = SnapshotAdapterFactory(entry, uuid='req-id').joined_request(slug_dir)
      assert restored == _joined(REQ_TS_NS, RES_TS_NS)

  def test_legacy_us_response_upgrades_to_ns_on_rewrite(self):
    with tempfile.TemporaryDirectory() as slug_dir:
      entry = SnapshotEntryAdapter.from_joined(
        _joined(REQ_TS_NS, RES_TS_US_LEGACY), slug_dir
      ).adapt()
      restored = SnapshotAdapterFactory(entry, uuid='req-id').joined_request(slug_dir)
      assert restored == _joined(REQ_TS_NS, RES_TS_NS)

  def test_legacy_int_timestamps_still_load(self):
    entry = {
      'method': 'GET',
      'url': 'https://example.com/api',
      'http_version': '1.1',
      'timestamp': REQ_TS_NS,
      'headers': 'Host: example.com',
      'response': {
        'status': 200,
        'latency': 42,
        'http_version': '1.1',
        'timestamp': RES_TS_US_LEGACY,
        'headers': {},
      },
    }
    with tempfile.TemporaryDirectory() as slug_dir:
      restored = SnapshotAdapterFactory(entry, uuid='req-id').joined_request(slug_dir)
      assert restored.startswith(f'1 req-id {REQ_TS_NS}\r\n'.encode())
      assert f'2 req-id {RES_TS_NS} 42\r\n'.encode() in restored

  def test_yaml_dump_load_preserves_timestamps(self):
    with tempfile.TemporaryDirectory() as slug_dir:
      entry = SnapshotEntryAdapter.from_joined(
        _joined(REQ_TS_NS, RES_TS_NS), slug_dir
      ).adapt()
      dumped = yaml.safe_dump(entry, sort_keys=False)
      loaded = yaml.safe_load(dumped)
      restored = SnapshotAdapterFactory(loaded, uuid='req-id').joined_request(slug_dir)
      assert restored == _joined(REQ_TS_NS, RES_TS_NS)

  def test_request_and_response_factories(self):
    joined = _joined(REQ_TS_NS, RES_TS_NS)
    request = RawJoinedRequestAdapterFactory(joined).snapshot_request()
    response = RawJoinedResponseAdapterFactory(joined).snapshot_response()
    assert request['method'] == 'GET'
    assert 'response' not in request
    assert response['status'] == 200

  def test_snapshot_entry_factory_with_slug_dir(self):
    with tempfile.TemporaryDirectory() as slug_dir:
      joined = _joined(REQ_TS_NS, RES_TS_NS)
      entry = RawJoinedRequestAdapterFactory(joined).snapshot_entry(slug_dir)
      assert entry['timestamp'] == '2026-11-19T05:29:50.943834368Z'

  def test_multiple_set_cookie_round_trip(self):
    request = b'GET https://example.com/api HTTP/1.1\r\nHost: example.com\r\n\r\n'
    response = (
      b'HTTP/1.1 200\r\n'
      b'Set-Cookie: session=abc; Path=/\r\n'
      b'Set-Cookie: user=john; HttpOnly\r\n'
      b'Content-Length: 0\r\n\r\n'
    )
    joined = REQUEST_DELIMITTER.join([
      f'1 req-id {REQ_TS_NS}'.encode() + b'\r\n' + request,
      f'2 req-id {RES_TS_NS} 42'.encode() + b'\r\n' + response,
    ])
    with tempfile.TemporaryDirectory() as slug_dir:
      entry = SnapshotEntryAdapter.from_joined(joined, slug_dir).adapt()
      assert entry['response']['headers']['Set-Cookie'] == [
        'session=abc; Path=/',
        'user=john; HttpOnly',
      ]
      dumped = yaml.safe_dump(entry, sort_keys=False)
      loaded = yaml.safe_load(dumped)
      restored = SnapshotAdapterFactory(loaded, uuid='req-id').joined_request(slug_dir)
      assert restored == joined
