import json
import os

import pytest
import yaml

from stoobly_agent.app.models.factories.resource.local_db.helpers.request_snapshot import RequestSnapshotV2
from stoobly_agent.app.models.factories.resource.local_db.helpers.scenario_snapshot import (
  ScenarioSnapshot,
  ScenarioSnapshotV1,
  ScenarioSnapshotV2,
)
from stoobly_agent.app.models.factories.resource.local_db.helpers.snapshot_format import FORMAT_V1, FORMAT_V2
from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.test.test_helper import reset


@pytest.fixture(autouse=True)
def settings():
  return reset()


UUID = 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb'
REQUEST_UUID = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'


class TestScenarioSnapshotParseRef:
  def test_name_only(self):
    parsed_uuid, parsed_name = ScenarioSnapshot._parse_scenario_ref('checkout-flow')
    assert parsed_uuid is None
    assert parsed_name == 'checkout-flow'

  def test_name_uuid(self):
    parsed_uuid, parsed_name = ScenarioSnapshot._parse_scenario_ref(f'checkout-flow/{UUID}')
    assert parsed_uuid == UUID
    assert parsed_name == 'checkout-flow'

  def test_name_uuid_yaml_suffix(self):
    parsed_uuid, parsed_name = ScenarioSnapshot._parse_scenario_ref(f'checkout-flow/{UUID}.yaml')
    assert parsed_uuid == UUID
    assert parsed_name == 'checkout-flow'

  def test_bare_uuid(self):
    parsed_uuid, parsed_name = ScenarioSnapshot._parse_scenario_ref(UUID)
    assert parsed_uuid == UUID
    assert parsed_name is None


class TestScenarioSnapshotSanitize:
  def test_empty_becomes_scenario(self):
    assert ScenarioSnapshotV2.sanitize_scenario_filename('') == 'scenario'
    assert ScenarioSnapshotV2.sanitize_scenario_filename('!!!') == 'scenario'

  def test_strips_leading_trailing_safe_punct(self):
    assert ScenarioSnapshotV2.sanitize_scenario_filename('-._name_.-') == 'name'


class TestScenarioSnapshotCreateAndFromPath:
  def test_create_name_only_is_v2_and_hydrates_uuid(self):
    data_dir = DataDir.instance()
    path = os.path.join(data_dir.snapshots_scenarios_dir_path, 'checkout-flow.yaml')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as fp:
      yaml.safe_dump({'uuid': UUID, 'description': '', 'requests': []}, fp)

    snapshot = ScenarioSnapshot.create('checkout-flow', data_dir)
    assert isinstance(snapshot, ScenarioSnapshotV2)
    assert snapshot.format == FORMAT_V2
    assert snapshot.uuid == UUID

  def test_create_detects_v1(self):
    data_dir = DataDir.instance()
    v1 = ScenarioSnapshotV1(UUID, data_dir)
    with open(v1.metadata_path, 'w') as fp:
      json.dump({'name': 'legacy', 'description': ''}, fp)
    os.makedirs(os.path.dirname(v1.requests_path), exist_ok=True)
    with open(v1.requests_path, 'w') as fp:
      fp.write('')

    snapshot = ScenarioSnapshot.create(UUID, data_dir)
    assert isinstance(snapshot, ScenarioSnapshotV1)
    assert snapshot.metadata['name'] == 'legacy'

  def test_from_path_yaml_without_uuid_returns_none(self):
    data_dir = DataDir.instance()
    path = os.path.join(data_dir.snapshots_scenarios_dir_path, 'broken.yaml')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as fp:
      yaml.safe_dump({'description': 'no uuid'}, fp)

    assert ScenarioSnapshot.from_path(path, data_dir) is None

  def test_from_path_yaml_with_uuid(self):
    data_dir = DataDir.instance()
    path = os.path.join(data_dir.snapshots_scenarios_dir_path, 'ok-flow.yaml')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as fp:
      yaml.safe_dump({'uuid': UUID, 'description': 'x', 'requests': []}, fp)

    snapshot = ScenarioSnapshot.from_path(path, data_dir)
    assert isinstance(snapshot, ScenarioSnapshotV2)
    assert snapshot.uuid == UUID

  def test_from_path_outside_scenarios_dir(self):
    data_dir = DataDir.instance()
    outside = os.path.join(data_dir.path, 'outside.yaml')
    with open(outside, 'w') as fp:
      fp.write('uuid: x\n')
    assert ScenarioSnapshot.from_path(outside, data_dir) is None


class TestScenarioSnapshotV2Metadata:
  def test_corrupt_yaml_returns_empty_metadata(self):
    data_dir = DataDir.instance()
    path = os.path.join(data_dir.snapshots_scenarios_dir_path, 'corrupt.yaml')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as fp:
      fp.write('junk: [')

    snapshot = ScenarioSnapshotV2('', data_dir, name='corrupt')
    assert snapshot.metadata == {}
    assert snapshot._load_metadata_data() == {}

  def test_missing_uuid_in_yaml_returns_empty(self):
    data_dir = DataDir.instance()
    path = os.path.join(data_dir.snapshots_scenarios_dir_path, 'no-uuid.yaml')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as fp:
      yaml.safe_dump({'description': 'x', 'requests': []}, fp)

    snapshot = ScenarioSnapshotV2('', data_dir, name='no-uuid')
    assert snapshot._load_metadata_data() == {}

  def test_iter_skips_invalid_relative_paths(self):
    data_dir = DataDir.instance()
    path = os.path.join(data_dir.snapshots_scenarios_dir_path, 'skip-bad.yaml')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as fp:
      yaml.safe_dump({
        'uuid': UUID,
        'description': '',
        'requests': [
          'not-a-valid-relative',
          RequestSnapshotV2.request_relative_path('GET-api', REQUEST_UUID),
        ],
      }, fp)

    request_snap = RequestSnapshotV2(REQUEST_UUID, data_dir, slug='GET-api')
    request_snap._ensure_parent(request_snap.path)
    with open(request_snap.path, 'wb') as fp:
      fp.write(b'req')

    snapshot = ScenarioSnapshot.create('skip-bad', data_dir)
    snaps = snapshot.request_snapshots
    assert len(snaps) == 1
    assert snaps[0].uuid == REQUEST_UUID


class TestScenarioSnapshotV1CorruptMetadata:
  def test_invalid_json_falls_back_to_name_uuid(self):
    data_dir = DataDir.instance()
    v1 = ScenarioSnapshotV1(UUID, data_dir)
    with open(v1.metadata_path, 'w') as fp:
      fp.write('not-json')

    assert v1._load_metadata_data() == {'name': UUID}
    assert v1.metadata['name'] == UUID
