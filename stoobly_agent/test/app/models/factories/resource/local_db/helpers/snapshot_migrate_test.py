import json
import os

import pytest
import yaml

from stoobly_agent.app.models.factories.resource.local_db.helpers.log import Log
from stoobly_agent.app.models.factories.resource.local_db.helpers.log_event import (
  LogEventV1,
  LogEventV2,
  PUT_ACTION,
  REQUEST_RESOURCE,
  SCENARIO_RESOURCE,
)
from stoobly_agent.app.models.factories.resource.local_db.helpers.request_snapshot import (
  RequestSnapshot,
  RequestSnapshotV1,
  RequestSnapshotV2,
)
from stoobly_agent.app.models.factories.resource.local_db.helpers.scenario_snapshot import ScenarioSnapshot
from stoobly_agent.app.models.factories.resource.local_db.helpers.snapshot_format import (
  FORMAT_V1,
  FORMAT_V2,
  detect_snapshot_format,
  has_v1_snapshots,
  has_v2_snapshots,
)
from stoobly_agent.app.models.factories.resource.local_db.helpers.snapshot_migrate import (
  _backfill_v1_scenario_locators,
  _backfill_v2_request_locators,
  _backfill_v2_scenario_locators,
  migrate_snapshots,
  migrate_snapshots_to_v1,
  migrate_snapshots_to_v2,
)
from stoobly_agent.app.proxy.record.joined_request import REQUEST_DELIMITTER
from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.test.test_helper import reset


@pytest.fixture(autouse=True)
def settings():
  return reset()


UUID_A = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'
UUID_B = 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb'
UUID_C = 'cccccccc-cccc-cccc-cccc-cccccccccccc'
SCENARIO_A = 'dddddddd-dddd-dddd-dddd-dddddddddddd'
SCENARIO_B = 'eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee'


def _joined(path: str = '/api', marker: bytes = b'') -> bytes:
  request = f'GET {path} HTTP/1.1\r\nHost: example.com\r\n\r\n'.encode() + marker
  response = b'HTTP/1.1 200 OK\r\nContent-Length: 0\r\n\r\n'
  return REQUEST_DELIMITTER.join([b'1 id 1\r\n' + request, b'2 id 1 1\r\n' + response])


def _write_v1_request(uuid: str, joined: bytes = None) -> str:
  snap = RequestSnapshotV1(uuid, DataDir.instance())
  snap.write_raw(joined if joined is not None else _joined())
  return snap.path


def _write_v2_request(uuid: str, slug: str = 'GET-api', joined: bytes = None) -> str:
  snap = RequestSnapshotV2(uuid, DataDir.instance(), slug=slug)
  snap.write_raw(joined if joined is not None else _joined())
  return snap.path


def _write_v1_scenario(uuid: str, name: str, request_uuids: list = None) -> str:
  data_dir = DataDir.instance()
  scenarios_dir = data_dir.snapshots_scenarios_dir_path
  os.makedirs(scenarios_dir, exist_ok=True)
  meta_path = os.path.join(scenarios_dir, uuid)
  with open(meta_path, 'w') as fp:
    json.dump({'name': name, 'description': ''}, fp)

  index_dir = data_dir.snapshots_scenario_requests_dir_path
  os.makedirs(index_dir, exist_ok=True)
  with open(os.path.join(index_dir, uuid), 'w') as fp:
    fp.write('\n'.join(request_uuids or []))
  return meta_path


def _write_v2_scenario(uuid: str, name: str, requests: list = None) -> str:
  data_dir = DataDir.instance()
  scenarios_dir = data_dir.snapshots_scenarios_dir_path
  os.makedirs(scenarios_dir, exist_ok=True)
  yaml_path = os.path.join(scenarios_dir, f'{name}.yaml')
  with open(yaml_path, 'w') as fp:
    yaml.safe_dump({
      'uuid': uuid,
      'description': '',
      'requests': requests or [],
    }, fp, sort_keys=False)
  return yaml_path


def _append_history(resource: str, locator: str, format: int = FORMAT_V1):
  line = (
    LogEventV2.serialize(resource, locator, PUT_ACTION)
    if format == FORMAT_V2
    else LogEventV1.serialize(resource, locator, PUT_ACTION)
  )
  Log().append(line)
  return line


class TestMigrateSnapshotsGate:
  def test_noop_when_empty(self):
    result = migrate_snapshots(DataDir.instance(), format=FORMAT_V2)
    assert result == {'requests': 0, 'scenarios': 0, 'noop': True}

    result = migrate_snapshots(DataDir.instance(), format=FORMAT_V1)
    assert result == {'requests': 0, 'scenarios': 0, 'noop': True}

  def test_noop_when_already_pure_v2(self):
    _write_v2_request(UUID_A)
    result = migrate_snapshots(DataDir.instance(), format=FORMAT_V2)
    assert result['noop'] is True
    assert result['requests'] == 0

  def test_noop_when_already_pure_v1(self):
    _write_v1_request(UUID_A)
    result = migrate_snapshots(DataDir.instance(), format=FORMAT_V1)
    assert result['noop'] is True
    assert result['requests'] == 0

  def test_rejects_unsupported_format(self):
    with pytest.raises(ValueError, match='Unsupported snapshot format'):
      migrate_snapshots(DataDir.instance(), format=99)

  def test_migrates_v1_to_v2(self):
    _write_v1_request(UUID_A)
    _append_history(REQUEST_RESOURCE, UUID_A, format=FORMAT_V1)

    result = migrate_snapshots(DataDir.instance(), format=FORMAT_V2)
    assert result['noop'] is False
    assert result['requests'] == 1
    assert detect_snapshot_format(DataDir.instance()) == FORMAT_V2
    assert RequestSnapshot.create(UUID_A).format == FORMAT_V2

    event = next(e for e in Log().events if e.is_request())
    assert '/' in event.resource_uuid
    assert event.resource_id == UUID_A

  def test_migrates_v2_to_v1(self):
    _write_v2_request(UUID_A)
    _append_history(REQUEST_RESOURCE, f'GET-api/{UUID_A}', format=FORMAT_V2)

    result = migrate_snapshots(DataDir.instance(), format=FORMAT_V1)
    assert result['noop'] is False
    assert result['requests'] == 1
    assert detect_snapshot_format(DataDir.instance()) == FORMAT_V1
    assert RequestSnapshot.create(UUID_A).format == FORMAT_V1

    event = next(e for e in Log().events if e.is_request())
    assert event.resource_uuid == UUID_A

  def test_mixed_tree_finishes_pending_v1_when_targeting_v2(self):
    _write_v2_request(UUID_A)
    _write_v1_request(UUID_B, _joined('/other'))

    assert detect_snapshot_format(DataDir.instance()) == FORMAT_V2
    assert has_v1_snapshots(DataDir.instance())
    assert has_v2_snapshots(DataDir.instance())

    result = migrate_snapshots(DataDir.instance(), format=FORMAT_V2)
    assert result['noop'] is False
    assert result['requests'] == 1
    assert not has_v1_snapshots(DataDir.instance())
    assert RequestSnapshot.create(UUID_A).format == FORMAT_V2
    assert RequestSnapshot.create(UUID_B).format == FORMAT_V2

  def test_mixed_tree_finishes_pending_v2_when_targeting_v1(self):
    _write_v1_request(UUID_A)
    _write_v2_request(UUID_B, slug='GET-other', joined=_joined('/other'))

    assert detect_snapshot_format(DataDir.instance()) == FORMAT_V2
    assert has_v1_snapshots(DataDir.instance())

    result = migrate_snapshots(DataDir.instance(), format=FORMAT_V1)
    assert result['noop'] is False
    assert result['requests'] == 1
    assert not has_v2_snapshots(DataDir.instance())
    assert RequestSnapshot.create(UUID_A).format == FORMAT_V1
    assert RequestSnapshot.create(UUID_B).format == FORMAT_V1


class TestMigrateSnapshotsToV2:
  def test_converts_request_and_scenario(self):
    _write_v1_request(UUID_A)
    _write_v1_scenario(SCENARIO_A, 'checkout', [UUID_A])
    _append_history(REQUEST_RESOURCE, UUID_A, format=FORMAT_V1)
    _append_history(SCENARIO_RESOURCE, SCENARIO_A, format=FORMAT_V1)

    result = migrate_snapshots_to_v2(DataDir.instance())
    assert result == {'requests': 1, 'scenarios': 1}

    assert RequestSnapshot.create(UUID_A).format == FORMAT_V2
    scenario = ScenarioSnapshot.create(SCENARIO_A)
    assert scenario.format == FORMAT_V2
    assert scenario.exists

    request_event = next(e for e in Log().events if e.is_request())
    scenario_event = next(e for e in Log().events if e.is_scenario())
    assert request_event.resource_uuid.startswith('GET-api/')
    assert scenario_event.resource_uuid == f'checkout/{SCENARIO_A}'
    assert scenario_event.resource_id == SCENARIO_A

  def test_skips_corrupt_v1_request(self):
    _write_v1_request(UUID_A)
    shard = os.path.join(DataDir.instance().snapshots_requests_dir_path, UUID_C[0:2])
    os.makedirs(shard, exist_ok=True)
    corrupt = os.path.join(shard, UUID_C)
    with open(corrupt, 'wb') as fp:
      fp.write(b'not-a-joined-request')

    result = migrate_snapshots_to_v2(DataDir.instance())
    assert result['requests'] == 1
    assert os.path.isfile(corrupt)
    assert RequestSnapshot.create(UUID_A).format == FORMAT_V2


class TestMigrateSnapshotsToV1:
  def test_converts_request_and_scenario(self):
    _write_v2_request(UUID_A)
    relative = RequestSnapshotV2.request_relative_path('GET-api', UUID_A)
    _write_v2_scenario(SCENARIO_A, 'checkout', [relative])
    _append_history(REQUEST_RESOURCE, f'GET-api/{UUID_A}', format=FORMAT_V2)
    _append_history(SCENARIO_RESOURCE, f'checkout/{SCENARIO_A}', format=FORMAT_V2)

    result = migrate_snapshots_to_v1(DataDir.instance())
    assert result == {'requests': 1, 'scenarios': 1}

    assert RequestSnapshot.create(UUID_A).format == FORMAT_V1
    assert ScenarioSnapshot.create(SCENARIO_A).format == FORMAT_V1

    request_event = next(e for e in Log().events if e.is_request())
    scenario_event = next(e for e in Log().events if e.is_scenario())
    assert request_event.resource_uuid == UUID_A
    assert scenario_event.resource_uuid == SCENARIO_A


class TestRemigrateHistoryBackfill:
  def test_remigrate_rewrites_history_for_already_converted_request(self):
    # Already-v2 request from a prior partial migrate; history still bare uuid
    _write_v2_request(UUID_A)
    _append_history(REQUEST_RESOURCE, UUID_A, format=FORMAT_V1)

    # Leftover v1 file so migrate_snapshots_to_v2 actually runs
    _write_v1_request(UUID_B, _joined('/other'))
    _append_history(REQUEST_RESOURCE, UUID_B, format=FORMAT_V1)

    migrate_snapshots_to_v2(DataDir.instance())

    request_events = [e for e in Log().events if e.is_request()]
    by_id = {e.resource_id: e for e in request_events}
    assert by_id[UUID_A].resource_uuid == f'GET-api/{UUID_A}'
    assert by_id[UUID_B].resource_uuid.startswith('GET-other/')

  def test_remigrate_rewrites_history_for_already_converted_scenario(self):
    _write_v2_scenario(SCENARIO_A, 'already-done')
    _append_history(SCENARIO_RESOURCE, SCENARIO_A, format=FORMAT_V1)

    _write_v1_scenario(SCENARIO_B, 'pending')
    _append_history(SCENARIO_RESOURCE, SCENARIO_B, format=FORMAT_V1)

    migrate_snapshots_to_v2(DataDir.instance())

    scenario_events = [e for e in Log().events if e.is_scenario()]
    locators = {e.resource_uuid for e in scenario_events}
    assert locators == {f'already-done/{SCENARIO_A}', f'pending/{SCENARIO_B}'}

  def test_remigrate_to_v1_rewrites_history_for_already_converted_scenario(self):
    # Already-v1 scenario meta; history still uses name/uuid from partial v2→v1
    _write_v1_scenario(SCENARIO_A, 'already-done')
    _append_history(SCENARIO_RESOURCE, f'already-done/{SCENARIO_A}', format=FORMAT_V2)

    _write_v2_scenario(SCENARIO_B, 'pending')
    _append_history(SCENARIO_RESOURCE, f'pending/{SCENARIO_B}', format=FORMAT_V2)

    migrate_snapshots_to_v1(DataDir.instance())

    scenario_events = [e for e in Log().events if e.is_scenario()]
    by_id = {e.resource_id: e for e in scenario_events}
    assert by_id[SCENARIO_A].resource_uuid == SCENARIO_A
    assert by_id[SCENARIO_B].resource_uuid == SCENARIO_B

  def test_gate_rewrites_history_when_last_v1_already_gone(self):
    # Interrupt after last v1 remove, before history rewrite: pure v2 + bare uuids
    _write_v2_request(UUID_A)
    _write_v2_scenario(SCENARIO_A, 'checkout')
    _append_history(REQUEST_RESOURCE, UUID_A, format=FORMAT_V1)
    _append_history(SCENARIO_RESOURCE, SCENARIO_A, format=FORMAT_V1)

    assert not has_v1_snapshots(DataDir.instance())
    assert has_v2_snapshots(DataDir.instance())

    result = migrate_snapshots(DataDir.instance(), format=FORMAT_V2)
    assert result['noop'] is False
    assert result['requests'] == 0
    assert result['scenarios'] == 0

    request_event = next(e for e in Log().events if e.is_request())
    scenario_event = next(e for e in Log().events if e.is_scenario())
    assert request_event.resource_uuid == f'GET-api/{UUID_A}'
    assert scenario_event.resource_uuid == f'checkout/{SCENARIO_A}'

    noop = migrate_snapshots(DataDir.instance(), format=FORMAT_V2)
    assert noop['noop'] is True

  def test_gate_rewrites_history_when_last_v2_already_gone(self):
    # Interrupt after last v2 remove, before history rewrite: pure v1 + v2 locators
    _write_v1_request(UUID_A)
    _write_v1_scenario(SCENARIO_A, 'checkout')
    _append_history(REQUEST_RESOURCE, f'GET-api/{UUID_A}', format=FORMAT_V2)
    _append_history(SCENARIO_RESOURCE, f'checkout/{SCENARIO_A}', format=FORMAT_V2)

    assert not has_v2_snapshots(DataDir.instance())
    assert has_v1_snapshots(DataDir.instance())

    result = migrate_snapshots(DataDir.instance(), format=FORMAT_V1)
    assert result['noop'] is False
    assert result['requests'] == 0
    assert result['scenarios'] == 0

    request_event = next(e for e in Log().events if e.is_request())
    scenario_event = next(e for e in Log().events if e.is_scenario())
    assert request_event.resource_uuid == UUID_A
    assert scenario_event.resource_uuid == SCENARIO_A

    noop = migrate_snapshots(DataDir.instance(), format=FORMAT_V1)
    assert noop['noop'] is True


class TestBackfillHelpers:
  def test_backfill_v2_request_locators(self):
    _write_v2_request(UUID_A, slug='GET-api')
    locators = {}
    _backfill_v2_request_locators(DataDir.instance().snapshots_requests_dir_path, locators)
    assert locators == {UUID_A: f'GET-api/{UUID_A}'}

  def test_backfill_v2_request_locators_preserves_existing(self):
    _write_v2_request(UUID_A, slug='GET-api')
    locators = {UUID_A: 'custom/locator'}
    _backfill_v2_request_locators(DataDir.instance().snapshots_requests_dir_path, locators)
    assert locators[UUID_A] == 'custom/locator'

  def test_backfill_v2_scenario_locators(self):
    _write_v2_scenario(SCENARIO_A, 'flow')
    locators = {}
    _backfill_v2_scenario_locators(DataDir.instance().snapshots_scenarios_dir_path, locators)
    assert locators == {SCENARIO_A: f'flow/{SCENARIO_A}'}

  def test_backfill_v1_scenario_locators(self):
    _write_v1_scenario(SCENARIO_A, 'flow')
    locators = {}
    _backfill_v1_scenario_locators(DataDir.instance().snapshots_scenarios_dir_path, locators)
    assert locators == {'flow': SCENARIO_A}
