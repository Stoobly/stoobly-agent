import tempfile
from datetime import datetime, timezone

import pytest
import yaml

from stoobly_agent.app.models.factories.resource.local_db.helpers.yaml_adapter import (
  _coerce_legacy_us_to_ns,
  _format_control_timestamp,
  _parse_control_timestamp,
  entry_to_joined,
  joined_to_entry,
)
from stoobly_agent.app.proxy.record.joined_request import REQUEST_DELIMITTER

REQ_TS_NS = 1795066190943834368
RES_TS_US_LEGACY = 1795066190944042
RES_TS_NS = 1795066190944042000


def _joined(req_ts: int, res_ts: int) -> bytes:
  request = b'GET https://example.com/api HTTP/1.1\r\nHost: example.com\r\n\r\n'
  response = b'HTTP/1.1 200\r\nContent-Length: 0\r\n\r\n'
  return REQUEST_DELIMITTER.join([
    f'1 req-id {req_ts}'.encode() + b'\r\n' + request,
    f'2 req-id {res_ts} 42'.encode() + b'\r\n' + response,
  ])


class TestControlTimestampCodec:
  def test_ns_round_trip(self):
    iso = _format_control_timestamp(REQ_TS_NS)
    assert iso == '2026-11-19T05:29:50.943834368Z'
    assert _parse_control_timestamp(iso) == REQ_TS_NS

  def test_zero_formats_as_epoch(self):
    assert _format_control_timestamp(0) == '1970-01-01T00:00:00Z'
    assert _parse_control_timestamp('1970-01-01T00:00:00Z') == 0

  def test_legacy_int_and_digit_string(self):
    assert _parse_control_timestamp(123) == 123
    assert _parse_control_timestamp('456') == 456

  def test_datetime_from_yaml_loader(self):
    dt = datetime(2026, 11, 19, 5, 29, 50, 944042, tzinfo=timezone.utc)
    assert _parse_control_timestamp(dt) == RES_TS_NS

  def test_coerce_legacy_us(self):
    assert _coerce_legacy_us_to_ns(RES_TS_US_LEGACY) == RES_TS_NS
    assert _coerce_legacy_us_to_ns(RES_TS_NS) == RES_TS_NS
    assert _coerce_legacy_us_to_ns(0) == 0
    assert _coerce_legacy_us_to_ns(1) == 1
    assert _coerce_legacy_us_to_ns(None) == 0

  def test_none_and_empty(self):
    assert _format_control_timestamp(None) is None
    assert _parse_control_timestamp(None) == 0
    assert _parse_control_timestamp('') == 0

  def test_invalid_raises(self):
    with pytest.raises(ValueError, match='invalid timestamp'):
      _parse_control_timestamp('not-a-time')
    with pytest.raises(ValueError, match='invalid timestamp'):
      _parse_control_timestamp(True)


class TestJoinedEntryTimestamps:
  def test_joined_to_entry_writes_iso(self):
    with tempfile.TemporaryDirectory() as slug_dir:
      entry = joined_to_entry(_joined(REQ_TS_NS, RES_TS_NS), slug_dir, uuid='req-id')
      assert entry['timestamp'] == '2026-11-19T05:29:50.943834368Z'
      assert entry['response']['timestamp'] == '2026-11-19T05:29:50.944042Z'

  def test_legacy_us_response_formats_as_same_iso(self):
    with tempfile.TemporaryDirectory() as slug_dir:
      entry = joined_to_entry(
        _joined(REQ_TS_NS, RES_TS_US_LEGACY), slug_dir, uuid='req-id'
      )
      assert entry['response']['timestamp'] == '2026-11-19T05:29:50.944042Z'

  def test_entry_to_joined_round_trip(self):
    with tempfile.TemporaryDirectory() as slug_dir:
      entry = joined_to_entry(_joined(REQ_TS_NS, RES_TS_NS), slug_dir, uuid='req-id')
      restored = entry_to_joined(entry, slug_dir, uuid='req-id')
      assert restored == _joined(REQ_TS_NS, RES_TS_NS)

  def test_legacy_us_response_upgrades_to_ns_on_rewrite(self):
    with tempfile.TemporaryDirectory() as slug_dir:
      entry = joined_to_entry(
        _joined(REQ_TS_NS, RES_TS_US_LEGACY), slug_dir, uuid='req-id'
      )
      restored = entry_to_joined(entry, slug_dir, uuid='req-id')
      assert restored == _joined(REQ_TS_NS, RES_TS_NS)

  def test_legacy_int_timestamps_still_load(self):
    entry = {
      'method': 'GET',
      'url': 'https://example.com/api',
      'http_version': '1.1',
      'timestamp': REQ_TS_NS,
      'headers': {'Host': 'example.com'},
      'response': {
        'status': 200,
        'latency': 42,
        'http_version': '1.1',
        'timestamp': RES_TS_US_LEGACY,
        'headers': {},
      },
    }
    with tempfile.TemporaryDirectory() as slug_dir:
      restored = entry_to_joined(entry, slug_dir, uuid='req-id')
      assert restored.startswith(f'1 req-id {REQ_TS_NS}\r\n'.encode())
      assert f'2 req-id {RES_TS_NS} 42\r\n'.encode() in restored

  def test_yaml_dump_load_preserves_timestamps(self):
    with tempfile.TemporaryDirectory() as slug_dir:
      entry = joined_to_entry(_joined(REQ_TS_NS, RES_TS_NS), slug_dir, uuid='req-id')
      dumped = yaml.safe_dump(entry, sort_keys=False)
      loaded = yaml.safe_load(dumped)
      restored = entry_to_joined(loaded, slug_dir, uuid='req-id')
      assert restored == _joined(REQ_TS_NS, RES_TS_NS)
