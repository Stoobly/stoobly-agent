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
    line = LogEvent.serialize(REQUEST_RESOURCE, 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', PUT_ACTION)
    event = LogEvent.create(line)
    assert isinstance(event, LogEventV1)
    assert event.format == FORMAT_V1
    assert event.resource_id == 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'
    assert event.resource_slug is None

  def test_slug_uuid_request_is_v2(self):
    line = LogEvent.serialize(
      REQUEST_RESOURCE,
      'GET-api-users/aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
      PUT_ACTION,
    )
    event = LogEvent.create(line)
    assert isinstance(event, LogEventV2)
    assert event.format == FORMAT_V2
    assert event.resource_id == 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'
    assert event.resource_slug == 'GET-api-users'

  def test_scenario_name_only_is_v2(self):
    line = LogEvent.serialize(SCENARIO_RESOURCE, 'checkout-flow', PUT_ACTION)
    event = LogEvent.create(line)
    assert isinstance(event, LogEventV2)
    assert event.resource_id == 'checkout-flow'
    assert event.resource_slug == 'checkout-flow'

  def test_scenario_bare_uuid_is_v1(self):
    line = LogEvent.serialize(
      SCENARIO_RESOURCE,
      'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb',
      PUT_ACTION,
    )
    event = LogEvent.create(line)
    assert isinstance(event, LogEventV1)
    assert event.resource_id == 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb'

  def test_legacy_scenario_name_uuid_is_v2(self):
    line = LogEvent.serialize(
      SCENARIO_RESOURCE,
      'checkout-flow/bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb',
      PUT_ACTION,
    )
    event = LogEvent.create(line)
    assert isinstance(event, LogEventV2)
    # Collapse identity prefers the name when present
    assert event.resource_id == 'checkout-flow'
    assert event.resource_slug == 'checkout-flow'


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
    put_line = LogEvent.serialize(SCENARIO_RESOURCE, 'checkout-flow', PUT_ACTION)
    delete_line = LogEvent.serialize(SCENARIO_RESOURCE, 'checkout-flow', DELETE_ACTION)
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

    assert seen['put'] == 'checkout-flow'
    assert seen['delete'] == 'checkout-flow'


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
