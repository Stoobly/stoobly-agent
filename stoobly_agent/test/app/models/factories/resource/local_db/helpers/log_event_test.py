import pytest

from stoobly_agent.app.models.factories.resource.local_db.helpers.log_event import (
  DELETE_ACTION,
  LogEvent,
  LogEventV1,
  LogEventV2,
  PUT_ACTION,
  REQUEST_RESOURCE,
  SCENARIO_RESOURCE,
)
from stoobly_agent.app.models.factories.resource.local_db.helpers.snapshot_format import FORMAT_V1, FORMAT_V2
from stoobly_agent.test.test_helper import reset


@pytest.fixture(autouse=True)
def settings():
  return reset()


class TestLogEventCreate:
  def test_bare_uuid_request_is_v1(self):
    line = LogEventV1.serialize(REQUEST_RESOURCE, 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', PUT_ACTION)
    event = LogEvent.create(line)
    assert isinstance(event, LogEventV1)
    assert event.format == FORMAT_V1
    assert event.resource_id == 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'
    assert event.resource_slug is None

  def test_slug_uuid_request_is_v2(self):
    line = LogEventV2.serialize(
      REQUEST_RESOURCE,
      'GET-api-users/aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
      PUT_ACTION,
    )
    event = LogEvent.create(line)
    assert isinstance(event, LogEventV2)
    assert event.format == FORMAT_V2
    assert event.resource_id == 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'
    assert event.resource_slug == 'GET-api-users'
    # uuid ISO-8601 action resource resource_id
    toks = line.split(' ')
    assert toks[1].endswith('Z')
    assert 'T' in toks[1]
    assert toks[2] == PUT_ACTION
    assert toks[3] == REQUEST_RESOURCE
    assert isinstance(event.created_at, int)

  def test_scenario_name_with_spaces_is_v2(self):
    locator = 'My Scenario/bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb'
    line = LogEventV2.serialize(SCENARIO_RESOURCE, locator, PUT_ACTION)
    event = LogEvent.create(line)
    assert isinstance(event, LogEventV2)
    assert event.resource_uuid == locator
    assert event.resource_id == 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb'
    assert event.resource_slug == 'My Scenario'

  def test_legacy_v2_line_order_still_parses(self):
    # Pre-rewrite field order with name/uuid locator
    line = (
      '11111111-1111-1111-1111-111111111111 scenario '
      'My-Scenario/bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb PUT 1700000000000'
    )
    event = LogEvent.create(line)
    assert isinstance(event, LogEventV2)
    assert event.resource_uuid == 'My-Scenario/bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb'
    assert event.resource_id == 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb'
    assert event.created_at == 1700000000000

  def test_v2_iso_timestamp_parses(self):
    line = (
      '11111111-1111-1111-1111-111111111111 2023-11-14T22:13:20.000Z PUT request '
      'GET-api/aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'
    )
    event = LogEvent.create(line)
    assert isinstance(event, LogEventV2)
    assert event.created_at == 1700000000000
    assert str(event).split(' ')[1] == '2023-11-14T22:13:20Z'

  def test_v2_legacy_integer_timestamp_still_parses(self):
    line = (
      '11111111-1111-1111-1111-111111111111 1700000000000 PUT request '
      'GET-api/aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'
    )
    event = LogEvent.create(line)
    assert isinstance(event, LogEventV2)
    assert event.created_at == 1700000000000
    # Rewriting upgrades to ISO
    assert str(event).split(' ')[1] == '2023-11-14T22:13:20Z'

  def test_scenario_bare_uuid_is_v1(self):
    line = LogEventV1.serialize(
      SCENARIO_RESOURCE,
      'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb',
      PUT_ACTION,
    )
    event = LogEvent.create(line)
    assert isinstance(event, LogEventV1)
    assert event.resource_id == 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb'

  def test_legacy_scenario_name_uuid_is_v2(self):
    # Legacy field order with name/uuid locator
    line = LogEventV1.format_line(
      '11111111-1111-1111-1111-111111111111',
      1700000000000,
      PUT_ACTION,
      SCENARIO_RESOURCE,
      'checkout-flow/bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb',
    )
    event = LogEvent.create(line)
    assert isinstance(event, LogEventV2)
    # Collapse identity prefers UUID when present (same as requests)
    assert event.resource_id == 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb'
    assert event.resource_slug == 'checkout-flow'

  def test_scenario_name_uuid_locator_is_v2(self):
    line = LogEventV2.serialize(
      SCENARIO_RESOURCE,
      'checkout-flow/bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb',
      PUT_ACTION,
    )
    event = LogEvent.create(line)
    assert isinstance(event, LogEventV2)
    assert event.resource_id == 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb'
    assert event.resource_slug == 'checkout-flow'
    assert event.resource_uuid == 'checkout-flow/bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb'


class TestLogEventApply:
  def test_request_put_passes_full_locator(self):
    line = LogEvent.serialize(
      REQUEST_RESOURCE,
      'GET-api/aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
      PUT_ACTION,
    )
    event = LogEvent.create(line)
    seen = {}

    event.apply(
      handle_request_put=lambda ref: seen.setdefault('put', ref),
      handle_request_delete=lambda ref: seen.setdefault('delete', ref),
      handle_scenario_put=lambda ref: None,
      handle_scenario_delete=lambda ref: None,
    )

    assert seen['put'] == 'GET-api/aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'

  def test_request_delete_passes_resource_id(self):
    line = LogEvent.serialize(
      REQUEST_RESOURCE,
      'GET-api/aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
      DELETE_ACTION,
    )
    event = LogEvent.create(line)
    seen = {}

    event.apply(
      handle_request_put=lambda ref: None,
      handle_request_delete=lambda ref: seen.setdefault('delete', ref),
      handle_scenario_put=lambda ref: None,
      handle_scenario_delete=lambda ref: None,
    )

    assert seen['delete'] == 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'

  def test_scenario_put_and_delete_pass_locator(self):
    locator = 'checkout-flow/bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb'
    put_line = LogEvent.serialize(SCENARIO_RESOURCE, locator, PUT_ACTION)
    delete_line = LogEvent.serialize(SCENARIO_RESOURCE, locator, DELETE_ACTION)
    put_event = LogEvent.create(put_line)
    delete_event = LogEvent.create(delete_line)
    seen = {}

    put_event.apply(
      handle_request_put=lambda ref: None,
      handle_request_delete=lambda ref: None,
      handle_scenario_put=lambda ref: seen.setdefault('put', ref),
      handle_scenario_delete=lambda ref: None,
    )
    delete_event.apply(
      handle_request_put=lambda ref: None,
      handle_request_delete=lambda ref: None,
      handle_scenario_put=lambda ref: None,
      handle_scenario_delete=lambda ref: seen.setdefault('delete', ref),
    )

    # PUT gets full locator for O(1) path resolve; DELETE gets UUID identity
    assert seen['put'] == locator
    assert seen['delete'] == 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb'


class TestLogEventDuplicate:
  def test_duplicate_refreshes_uuid_and_timestamp(self):
    line = LogEvent.serialize(REQUEST_RESOURCE, 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', PUT_ACTION)
    event = LogEvent.create(line)
    dup = event.duplicate()

    assert dup.uuid != event.uuid
    assert dup.resource_uuid == event.resource_uuid
    assert dup.action == PUT_ACTION
    assert isinstance(dup, type(event))

  def test_duplicate_as_delete_and_put(self):
    line = LogEvent.serialize(REQUEST_RESOURCE, 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', PUT_ACTION)
    event = LogEvent.create(line)

    assert event.duplicate_as_delete().action == DELETE_ACTION
    assert event.duplicate_as_put().action == PUT_ACTION


class TestLogEventKeyAndMissingCreatedAt:
  def test_key_uses_resource_id(self):
    line = LogEvent.serialize(
      REQUEST_RESOURCE,
      'GET-api/aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
      PUT_ACTION,
    )
    event = LogEvent.create(line)
    assert event.key == 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa.request'

  def test_missing_created_at_is_none(self):
    event = LogEvent.create(
      '11111111-1111-1111-1111-111111111111 request aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa PUT'
    )
    assert event.created_at is None


class TestMalformedLogEvent:
  def test_too_few_fields_raises(self):
    from stoobly_agent.app.models.factories.resource.local_db.helpers.log_event import MalformedLogEventError

    with pytest.raises(MalformedLogEventError, match='expected at least 4') as exc:
      LogEvent.create('uuid request locator')

    assert 'uuid request locator' in str(exc.value)

  def test_non_integer_created_at_raises(self):
    from stoobly_agent.app.models.factories.resource.local_db.helpers.log_event import MalformedLogEventError

    with pytest.raises(MalformedLogEventError, match='created_at must be an integer'):
      LogEvent.create(
        '11111111-1111-1111-1111-111111111111 request aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa PUT not-a-number'
      )

  def test_v2_invalid_timestamp_raises(self):
    from stoobly_agent.app.models.factories.resource.local_db.helpers.log_event import MalformedLogEventError

    with pytest.raises(MalformedLogEventError, match='ISO-8601 or integer timestamp'):
      LogEvent.create(
        '11111111-1111-1111-1111-111111111111 not-a-time PUT request '
        'GET-api/aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'
      )
