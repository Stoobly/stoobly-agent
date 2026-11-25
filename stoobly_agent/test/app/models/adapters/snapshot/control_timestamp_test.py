from datetime import datetime, timezone

import pytest

from stoobly_agent.app.models.adapters.snapshot.control_timestamp import (
  coerce_legacy_us_to_ns,
  format_control_timestamp,
  parse_control_timestamp,
)

REQ_TS_NS = 1795066190943834368
RES_TS_US_LEGACY = 1795066190944042
RES_TS_NS = 1795066190944042000


class TestControlTimestampCodec:
  def test_ns_round_trip(self):
    iso = format_control_timestamp(REQ_TS_NS)
    assert iso == '2026-11-19T05:29:50.943834368Z'
    assert parse_control_timestamp(iso) == REQ_TS_NS

  def test_zero_formats_as_epoch(self):
    assert format_control_timestamp(0) == '1970-01-01T00:00:00Z'
    assert parse_control_timestamp('1970-01-01T00:00:00Z') == 0

  def test_legacy_int_and_digit_string(self):
    assert parse_control_timestamp(123) == 123
    assert parse_control_timestamp('456') == 456

  def test_datetime_from_yaml_loader(self):
    dt = datetime(2026, 11, 19, 5, 29, 50, 944042, tzinfo=timezone.utc)
    assert parse_control_timestamp(dt) == RES_TS_NS

  def test_coerce_legacy_us(self):
    assert coerce_legacy_us_to_ns(RES_TS_US_LEGACY) == RES_TS_NS
    assert coerce_legacy_us_to_ns(RES_TS_NS) == RES_TS_NS
    assert coerce_legacy_us_to_ns(0) == 0
    assert coerce_legacy_us_to_ns(1) == 1
    assert coerce_legacy_us_to_ns(None) == 0

  def test_none_and_empty(self):
    assert format_control_timestamp(None) is None
    assert parse_control_timestamp(None) == 0
    assert parse_control_timestamp('') == 0

  def test_invalid_raises(self):
    with pytest.raises(ValueError, match='invalid timestamp'):
      parse_control_timestamp('not-a-time')
    with pytest.raises(ValueError, match='invalid timestamp'):
      parse_control_timestamp(True)
