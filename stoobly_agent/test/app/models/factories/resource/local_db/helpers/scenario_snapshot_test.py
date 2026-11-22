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
  def test_non_uuid_without_slash_is_not_a_locator(self):
    parsed_uuid, parsed_name = ScenarioSnapshot._parse_scenario_ref('checkout-flow')
    assert parsed_uuid == 'checkout-flow'
    assert parsed_name is None

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
    assert ScenarioSnapshotV2.sanitize_scenario_filename('///') == 'scenario'

  def test_strips_leading_trailing_safe_punct(self):
    assert ScenarioSnapshotV2.sanitize_scenario_filename('-._name_.-') == 'name'

  def test_preserves_spaces_and_punctuation(self):
    assert ScenarioSnapshotV2.sanitize_scenario_filename('My Scenario') == 'My Scenario'
    assert ScenarioSnapshotV2.sanitize_scenario_filename('My-Scenario') == 'My-Scenario'
    assert ScenarioSnapshotV2.sanitize_scenario_filename('My Scenario!') == 'My Scenario!'

  def test_replaces_path_separators(self):
    assert ScenarioSnapshotV2.sanitize_scenario_filename('a/b\\c') == 'a-b-c'


class TestScenarioSnapshotV2NameCollision:
  UUID_A = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'
  UUID_B = 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb'

  def test_space_and_hyphen_names_stay_distinct(self):
    data_dir = DataDir.instance()
    scenarios_dir = data_dir.snapshots_scenarios_dir_path
    os.makedirs(scenarios_dir, exist_ok=True)

    first = ScenarioSnapshotV2.allocate_yaml_path(scenarios_dir, 'My Scenario', uuid=self.UUID_A)
    assert os.path.basename(first) == 'My Scenario.yaml'
    with open(first, 'w') as fp:
      yaml.safe_dump({'uuid': self.UUID_A, 'description': '', 'requests': []}, fp)

    second = ScenarioSnapshotV2.allocate_yaml_path(scenarios_dir, 'My-Scenario', uuid=self.UUID_B)
    assert os.path.basename(second) == 'My-Scenario.yaml'

    again = ScenarioSnapshotV2.allocate_yaml_path(scenarios_dir, 'My Scenario', uuid=self.UUID_A)
    assert again == first

  def test_allocate_yaml_path_disambiguates_true_collisions(self):
    data_dir = DataDir.instance()
    scenarios_dir = data_dir.snapshots_scenarios_dir_path
    os.makedirs(scenarios_dir, exist_ok=True)

    first = ScenarioSnapshotV2.allocate_yaml_path(scenarios_dir, 'dup-name', uuid=self.UUID_A)
    with open(first, 'w') as fp:
      yaml.safe_dump({'uuid': self.UUID_A, 'description': '', 'requests': []}, fp)

    second = ScenarioSnapshotV2.allocate_yaml_path(scenarios_dir, 'dup-name', uuid=self.UUID_B)
    assert os.path.basename(second) == 'dup-name-2.yaml'

  def test_writes_keep_space_and_hyphen_names_distinct(self):
    from stoobly_agent.app.models.factories.resource.local_db.helpers.log import Log
    from stoobly_agent.app.models.factories.resource.local_db.helpers.log_event import LogEventV2
    from stoobly_agent.app.models.factories.resource.local_db.helpers.snapshot_service import snapshot_scenario
    from stoobly_agent.app.models.factories.resource.local_db.helpers.snapshot_types import PUT_ACTION
    from stoobly_agent.lib.orm.scenario import Scenario

    a = Scenario.create(name='My Scenario', description='')
    b = Scenario.create(name='My-Scenario', description='')

    path_a = snapshot_scenario(a, action=PUT_ACTION)
    path_b = snapshot_scenario(b, action=PUT_ACTION)

    assert os.path.basename(path_a) == 'My Scenario.yaml'
    assert os.path.basename(path_b) == 'My-Scenario.yaml'
    assert os.path.isfile(path_a) and os.path.isfile(path_b)

    assert ScenarioSnapshotV2._uuid_from_v2_yaml(path_a) == a.uuid
    assert ScenarioSnapshotV2._uuid_from_v2_yaml(path_b) == b.uuid

    events = [e for e in Log().events if e.is_scenario()]
    assert all(isinstance(e, LogEventV2) for e in events)
    locators = {e.resource_uuid for e in events}
    assert locators == {f'My Scenario/{a.uuid}', f'My-Scenario/{b.uuid}'}

    targets = [e for e in Log().target_events if e.is_scenario()]
    assert {e.resource_id for e in targets} == {a.uuid, b.uuid}

  def test_rename_relocates_yaml_and_collapses_history_by_uuid(self):
    from stoobly_agent.app.models.factories.resource.local_db.helpers.log import Log
    from stoobly_agent.app.models.factories.resource.local_db.helpers.snapshot_service import snapshot_scenario
    from stoobly_agent.app.models.factories.resource.local_db.helpers.snapshot_types import PUT_ACTION
    from stoobly_agent.lib.orm.scenario import Scenario

    scenario = Scenario.create(name='old-name', description='')
    first_path = snapshot_scenario(scenario, action=PUT_ACTION)
    assert os.path.basename(first_path) == 'old-name.yaml'

    scenario.update({'name': 'new-name'})
    scenario = Scenario.find(scenario.id)
    second_path = snapshot_scenario(scenario, action=PUT_ACTION)

    assert os.path.basename(second_path) == 'new-name.yaml'
    assert os.path.isfile(second_path)
    assert not os.path.exists(first_path)
    assert ScenarioSnapshotV2._uuid_from_v2_yaml(second_path) == scenario.uuid

    snap = ScenarioSnapshot.create(scenario.uuid)
    assert snap.metadata_path == second_path
    assert snap.metadata['name'] == 'new-name'

    events = [e for e in Log().events if e.is_scenario()]
    assert len(events) >= 2
    assert all(e.resource_id == scenario.uuid for e in events)
    assert events[-1].resource_uuid == f'new-name/{scenario.uuid}'

    targets = [e for e in Log().target_events if e.is_scenario()]
    assert len(targets) == 1
    assert targets[0].resource_id == scenario.uuid
    assert targets[0].resource_uuid == f'new-name/{scenario.uuid}'


class TestScenarioSnapshotCreateAndFromPath:
  def test_create_by_yaml_stem_is_v2_and_hydrates_uuid(self):
    data_dir = DataDir.instance()
    path = os.path.join(data_dir.snapshots_scenarios_dir_path, 'checkout-flow.yaml')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as fp:
      yaml.safe_dump({'uuid': UUID, 'description': '', 'requests': []}, fp)

    snapshot = ScenarioSnapshot.create('', data_dir, name='checkout-flow')
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


class TestScenarioSnapshotPathEscape:
  def test_history_locator_with_dotdot_stays_under_scenarios_dir(self):
    data_dir = DataDir.instance()
    scenarios_dir = data_dir.snapshots_scenarios_dir_path
    os.makedirs(scenarios_dir, exist_ok=True)

    # Plant a file outside scenarios/ that an unsanitized join would hit
    outside_dir = os.path.join(data_dir.path, 'tmp', 'x')
    os.makedirs(outside_dir, exist_ok=True)
    outside_yaml = os.path.join(outside_dir, 'evil.yaml')
    with open(outside_yaml, 'w') as fp:
      yaml.safe_dump({'uuid': UUID, 'description': 'outside', 'requests': []}, fp)

    # Legacy-style locator: name is ../../tmp/x relative to scenarios/
    rel_escape = os.path.relpath(outside_dir, scenarios_dir)
    locator = f'{rel_escape}/{UUID}'
    assert '..' in locator

    snap = ScenarioSnapshot.create(locator, data_dir)
    assert isinstance(snap, ScenarioSnapshotV2)

    meta = snap.metadata_path
    abs_meta = os.path.abspath(meta)
    abs_scenarios = os.path.abspath(scenarios_dir)
    assert os.path.commonpath([abs_meta, abs_scenarios]) == abs_scenarios
    assert abs_meta != os.path.abspath(outside_yaml)

    # Name lookup must not treat the outside file as the scenario snapshot
    found = snap._find_v2_metadata_path()
    if found:
      assert os.path.commonpath(
        [os.path.abspath(found), abs_scenarios]
      ) == abs_scenarios

  def test_safe_scenario_yaml_path_rejects_escape(self):
    data_dir = DataDir.instance()
    scenarios_dir = data_dir.snapshots_scenarios_dir_path
    path = ScenarioSnapshot._safe_scenario_yaml_path(scenarios_dir, '../../tmp/x')
    assert path is not None
    # Separators become '-', leading .-_ stripped → single basename under scenarios/
    assert os.path.basename(path) == 'tmp-x.yaml'
    assert '/' not in os.path.basename(path)
    assert os.path.dirname(os.path.abspath(path)) == os.path.abspath(scenarios_dir)
    assert os.path.commonpath(
      [os.path.abspath(path), os.path.abspath(scenarios_dir)]
    ) == os.path.abspath(scenarios_dir)


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
