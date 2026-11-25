import json
import os
import tempfile
from unittest.mock import patch

import pytest
import yaml

from stoobly_agent.app.models.factories.resource.local_db.helpers.request_snapshot import RequestSnapshotV2
from stoobly_agent.app.models.factories.resource.local_db.helpers.scenario_snapshot import (
  ScenarioSnapshot,
  ScenarioSnapshotV1,
  ScenarioSnapshotV2,
)
from stoobly_agent.app.models.factories.resource.local_db.helpers.snapshot_format import FORMAT_V1, FORMAT_V2
from stoobly_agent.config.constants.custom_headers import BODY_REF, HEADER_REF
from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.test.test_helper import reset


@pytest.fixture(autouse=True)
def settings():
  return reset()


UUID = 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb'
UUID_C = 'cccccccc-cccc-cccc-cccc-cccccccccccc'
UUID_D = 'dddddddd-dddd-dddd-dddd-dddddddddddd'
REQUEST_UUID = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'
REQUEST_UUID_B = 'eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee'


def _minimal_entry(url: str, slug: str, body_hash: str = None, header_hash: str = None) -> dict:
  headers = {}
  if body_hash:
    headers[BODY_REF] = f'.stoobly/snapshots/requests/{slug}/bodies/{body_hash}'
  if header_hash:
    headers[HEADER_REF] = f'.stoobly/snapshots/requests/{slug}/headers/{header_hash}'
  return {
    'method': 'GET',
    'url': url,
    'http_version': '1.1',
    'timestamp': 1,
    'headers': headers,
    'response': {
      'status': 200,
      'latency': 0,
      'http_version': '1.1',
      'timestamp': 1,
      'headers': {},
    },
  }


def _write_scenario_yaml(data_dir: DataDir, stem: str, scenario_uuid: str, requests: dict) -> str:
  scenarios_dir = data_dir.snapshots_scenarios_dir_path
  os.makedirs(scenarios_dir, exist_ok=True)
  path = os.path.join(scenarios_dir, f'{stem}.yaml')
  with open(path, 'w') as fp:
    yaml.safe_dump({
      'uuid': scenario_uuid,
      'description': '',
      'requests': requests,
    }, fp, sort_keys=False)
  return path


def _plant_slug_blob(data_dir: DataDir, slug: str, kind: str, digest: str, content: bytes) -> str:
  path = os.path.join(data_dir.snapshots_requests_dir_path, slug, kind, digest)
  os.makedirs(os.path.dirname(path), exist_ok=True)
  with open(path, 'wb') as fp:
    fp.write(content)
  return path


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


class TestScenarioSnapshotRequestEntries:
  def test_is_request_entry(self):
    assert ScenarioSnapshot.is_request_entry({
      'method': 'GET',
      'headers': {},
      'response': {},
    })
    assert not ScenarioSnapshot.is_request_entry('requests/foo/uuid')

  def test_iter_request_entries_dict(self):
    entry = {'method': 'GET', 'headers': {}, 'response': {}}
    assert list(ScenarioSnapshot.iter_request_entries({REQUEST_UUID: entry})) == [
      (REQUEST_UUID, entry),
    ]

  def test_iter_request_entries_legacy_list(self):
    item = {
      'uuid': REQUEST_UUID,
      'method': 'GET',
      'headers': {},
      'response': {},
    }
    assert list(ScenarioSnapshot.iter_request_entries([item])) == [(
      REQUEST_UUID,
      {'method': 'GET', 'headers': {}, 'response': {}},
    )]

  def test_iter_request_entries_skips_non_uuid_keys_and_incomplete(self):
    good = {'method': 'GET', 'headers': {}, 'response': {}}
    requests = {
      'not-a-uuid': good,
      REQUEST_UUID: {'method': 'GET'},  # missing headers/response
      REQUEST_UUID_B: good,
    }
    assert list(ScenarioSnapshot.iter_request_entries(requests)) == [
      (REQUEST_UUID_B, good),
    ]


class TestScenarioSnapshotDeleteSharedSlug:
  def test_delete_keeps_shared_slug_blobs_for_other_scenario(self):
    data_dir = DataDir.instance()
    slug = 'GET-api-shared-slug'
    body_hash = 'a' * 16
    header_hash = 'b' * 16
    body_path = _plant_slug_blob(data_dir, slug, 'bodies', body_hash, b'shared-body')
    header_path = _plant_slug_blob(data_dir, slug, 'headers', header_hash, b'Host: example.com')

    entry_a = _minimal_entry('https://example.com/api/shared-slug', slug, body_hash, header_hash)
    entry_b = _minimal_entry('https://example.com/api/shared-slug', slug, body_hash, header_hash)
    _write_scenario_yaml(data_dir, 'shared-a', UUID_C, {REQUEST_UUID: entry_a})
    _write_scenario_yaml(data_dir, 'shared-b', UUID_D, {REQUEST_UUID_B: entry_b})

    snap_a = ScenarioSnapshotV2(UUID_C, data_dir, name='shared-a')
    snap_a.remove()

    assert not snap_a.exists
    assert os.path.isfile(body_path)
    assert os.path.isfile(header_path)
    assert ScenarioSnapshotV2(UUID_D, data_dir, name='shared-b').exists
    assert RequestSnapshotV2.from_entry(entry_b, data_dir, uuid=REQUEST_UUID_B).request is not None

    ScenarioSnapshotV2(UUID_D, data_dir, name='shared-b').remove()
    assert not os.path.isdir(os.path.join(data_dir.snapshots_requests_dir_path, slug))

  def test_delete_keeps_shared_request_uuid_blobs(self):
    data_dir = DataDir.instance()
    slug = 'GET-api-shared-uuid'
    body_hash = 'c' * 16
    body_path = _plant_slug_blob(data_dir, slug, 'bodies', body_hash, b'uuid-body')
    entry = _minimal_entry('https://example.com/api/shared-uuid', slug, body_hash)
    _write_scenario_yaml(data_dir, 'owner-a', UUID_C, {REQUEST_UUID: entry})
    _write_scenario_yaml(data_dir, 'owner-b', UUID_D, {REQUEST_UUID: dict(entry)})

    ScenarioSnapshotV2(UUID_C, data_dir, name='owner-a').remove()

    assert os.path.isfile(body_path)
    remaining = ScenarioSnapshotV2(UUID_D, data_dir, name='owner-b')
    assert remaining.exists
    snaps = remaining.request_snapshots
    assert len(snaps) == 1
    assert snaps[0].uuid == REQUEST_UUID
    assert snaps[0].request is not None


class TestScenarioSnapshotPreferStandalone:
  def test_iter_prefers_standalone_yaml_over_embed(self):
    data_dir = DataDir.instance()
    slug = 'GET-api-prefer'
    embed = _minimal_entry('https://example.com/api/prefer', slug)
    embed['headers']['X-From'] = 'embed'
    _write_scenario_yaml(data_dir, 'prefer', UUID, {REQUEST_UUID: embed})

    standalone = RequestSnapshotV2(REQUEST_UUID, data_dir, slug=slug)
    standalone._ensure_parent(standalone.path)
    with open(standalone.path, 'w') as fp:
      yaml.safe_dump({
        **embed,
        'headers': {'X-From': 'standalone'},
        'response': embed['response'],
      }, fp, sort_keys=False)

    snap = ScenarioSnapshotV2(UUID, data_dir, name='prefer')
    seen = []
    snap.iter_request_snapshots(lambda s: seen.append(s))
    assert len(seen) == 1
    assert seen[0].path == standalone.path
    assert os.path.isfile(seen[0].path)
    assert seen[0].entry['headers'].get('X-From') == 'standalone'


class TestScenarioSnapshotHistoryLocator:
  def test_requires_uuid(self):
    with pytest.raises(ValueError, match='requires a uuid'):
      ScenarioSnapshotV2.history_locator_for('', 'checkout')

  def test_uses_on_disk_stem(self):
    data_dir = DataDir.instance()
    _write_scenario_yaml(data_dir, 'checkout-flow', UUID, {})
    locator = ScenarioSnapshotV2.history_locator_for(UUID, 'ignored-name', data_dir)
    assert locator == f'checkout-flow/{UUID}'

  def test_allocates_collision_stem(self):
    data_dir = DataDir.instance()
    scenarios_dir = data_dir.snapshots_scenarios_dir_path
    os.makedirs(scenarios_dir, exist_ok=True)
    with open(os.path.join(scenarios_dir, 'dup-name.yaml'), 'w') as fp:
      yaml.safe_dump({'uuid': UUID_C, 'description': '', 'requests': {}}, fp)

    locator = ScenarioSnapshotV2.history_locator_for(UUID_D, 'dup-name', data_dir)
    assert locator == f'dup-name-2/{UUID_D}'


class TestScenarioSnapshotUpdateRequestEntries:
  def test_merges_entries_in_place(self):
    data_dir = DataDir.instance()
    original = _minimal_entry('https://example.com/api', 'GET-api')
    path = _write_scenario_yaml(data_dir, 'merge', UUID, {REQUEST_UUID: original})
    snap = ScenarioSnapshotV2(UUID, data_dir, name='merge')

    updated = {**original, 'headers': {'X-New': '1'}, 'response': original['response']}
    snap.update_request_entries({REQUEST_UUID: updated, 'skip-me': 'not-a-dict'})

    with open(path, 'r') as fp:
      data = yaml.safe_load(fp)
    assert data['requests'][REQUEST_UUID]['headers'] == {'X-New': '1'}
    assert 'skip-me' not in data['requests']

  def test_noop_when_missing_or_non_dict_requests(self):
    data_dir = DataDir.instance()
    snap = ScenarioSnapshotV2(UUID, data_dir, name='missing')
    snap.update_request_entries({REQUEST_UUID: _minimal_entry('https://example.com/', 'GET')})
    assert not snap.exists

    path = _write_scenario_yaml(data_dir, 'legacy-list', UUID, {})
    with open(path, 'w') as fp:
      yaml.safe_dump({
        'uuid': UUID,
        'description': '',
        'requests': [RequestSnapshotV2.request_relative_path('GET-api', REQUEST_UUID)],
      }, fp)
    snap = ScenarioSnapshotV2(UUID, data_dir, name='legacy-list')
    before = open(path).read()
    snap.update_request_entries({REQUEST_UUID: _minimal_entry('https://example.com/', 'GET-api')})
    assert open(path).read() == before


class TestScenarioSnapshotWriteMetadataPreservesRequests:
  def test_write_metadata_keeps_existing_embeds(self):
    from stoobly_agent.lib.orm.scenario import Scenario

    data_dir = DataDir.instance()
    entry = _minimal_entry('https://example.com/api/keep', 'GET-api-keep')
    path = _write_scenario_yaml(data_dir, 'keep-meta', UUID, {REQUEST_UUID: entry})

    scenario = Scenario.create(uuid=UUID, name='keep-meta', description='updated')
    snap = ScenarioSnapshotV2(UUID, data_dir, name='keep-meta')
    snap.write_metadata(scenario)

    with open(path, 'r') as fp:
      data = yaml.safe_load(fp)
    assert data['description'] == 'updated'
    assert REQUEST_UUID in data['requests']
    assert data['requests'][REQUEST_UUID]['url'] == entry['url']


class TestScenarioSnapshotRenameCollision:
  def test_rename_into_occupied_stem_uses_unique_path(self):
    from stoobly_agent.app.models.factories.resource.local_db.helpers.snapshot_service import snapshot_scenario
    from stoobly_agent.app.models.factories.resource.local_db.helpers.snapshot_types import PUT_ACTION
    from stoobly_agent.lib.orm.scenario import Scenario

    # On-disk stem already owned by another uuid (ORM names are unique, so plant YAML only)
    data_dir = DataDir.instance()
    occupied_path = _write_scenario_yaml(data_dir, 'taken', UUID_C, {})

    moving = Scenario.create(name='old-stem', description='')
    old_path = snapshot_scenario(moving, action=PUT_ACTION)
    assert os.path.basename(old_path) == 'old-stem.yaml'

    moving.update({'name': 'taken'})
    moving = Scenario.find(moving.id)
    new_path = snapshot_scenario(moving, action=PUT_ACTION)

    assert os.path.basename(new_path) == 'taken-2.yaml'
    assert os.path.isfile(new_path)
    assert not os.path.exists(old_path)
    assert os.path.isfile(occupied_path)
    assert ScenarioSnapshotV2._uuid_from_v2_yaml(new_path) == moving.uuid
    assert ScenarioSnapshotV2._uuid_from_v2_yaml(occupied_path) == UUID_C


class TestScenarioSnapshotCopyEmbedRefs:
  def test_copy_requests_copies_body_and_header_blobs(self):
    data_dir = DataDir.instance()
    slug = 'GET-api-copy'
    body_hash = 'd' * 16
    header_hash = 'e' * 16
    _plant_slug_blob(data_dir, slug, 'bodies', body_hash, b'copy-body')
    _plant_slug_blob(data_dir, slug, 'headers', header_hash, b'Host: copy.example')
    entry = _minimal_entry(
      'https://example.com/api/copy', slug, body_hash, header_hash
    )
    _write_scenario_yaml(data_dir, 'copy-flow', UUID, {REQUEST_UUID: entry})

    with tempfile.TemporaryDirectory() as dest:
      snap = ScenarioSnapshotV2(UUID, data_dir, name='copy-flow')
      snap.copy_requests(dest)

      dest_body = os.path.join(
        dest, '.stoobly', 'snapshots', 'requests', slug, 'bodies', body_hash
      )
      dest_header = os.path.join(
        dest, '.stoobly', 'snapshots', 'requests', slug, 'headers', header_hash
      )
      # copy_file replaces data_dir parent; fall back to searching if layout differs
      if not os.path.isfile(dest_body):
        matches = []
        for root, _dirs, files in os.walk(dest):
          if body_hash in files:
            matches.append(os.path.join(root, body_hash))
        assert matches, f'body blob not copied under {dest}'
        dest_body = matches[0]
        dest_header = os.path.join(os.path.dirname(os.path.dirname(dest_body)), 'headers', header_hash)

      assert os.path.isfile(dest_body)
      assert os.path.isfile(dest_header)
      with open(dest_body, 'rb') as fp:
        assert fp.read() == b'copy-body'


class TestScenarioSnapshotYmlExtension:
  def test_from_path_and_create_accept_yml(self):
    data_dir = DataDir.instance()
    scenarios_dir = data_dir.snapshots_scenarios_dir_path
    os.makedirs(scenarios_dir, exist_ok=True)
    path = os.path.join(scenarios_dir, 'yml-flow.yml')
    with open(path, 'w') as fp:
      yaml.safe_dump({
        'uuid': UUID,
        'description': 'yml',
        'requests': {},
      }, fp)

    from_path = ScenarioSnapshot.from_path(path, data_dir)
    assert isinstance(from_path, ScenarioSnapshotV2)
    assert from_path.uuid == UUID

    by_stem = ScenarioSnapshot.create('yml-flow', data_dir)
    assert isinstance(by_stem, ScenarioSnapshotV2)
    assert by_stem.uuid == UUID
    assert by_stem.metadata_path == path

  def test_uuid_scan_finds_yml(self):
    data_dir = DataDir.instance()
    scenarios_dir = data_dir.snapshots_scenarios_dir_path
    os.makedirs(scenarios_dir, exist_ok=True)
    path = os.path.join(scenarios_dir, 'scan-me.yml')
    with open(path, 'w') as fp:
      yaml.safe_dump({'uuid': UUID_C, 'description': '', 'requests': {}}, fp)

    snap = ScenarioSnapshot.create(UUID_C, data_dir)
    assert isinstance(snap, ScenarioSnapshotV2)
    assert snap.metadata_path == path


class TestScenarioSnapshotCorruptEmbedSkipped:
  def test_from_entry_value_error_does_not_block_siblings(self):
    data_dir = DataDir.instance()
    good = _minimal_entry('https://example.com/api/good', 'GET-api-good')
    bad = _minimal_entry('https://example.com/api/bad', 'GET-api-bad')
    _write_scenario_yaml(
      data_dir,
      'partial',
      UUID,
      {REQUEST_UUID: bad, REQUEST_UUID_B: good},
    )

    real_from_entry = RequestSnapshotV2.from_entry

    def flaky_from_entry(entry, data_dir=None, slug=None, uuid=None):
      if str(uuid) == REQUEST_UUID:
        raise ValueError('simulated corrupt embed')
      return real_from_entry(entry, data_dir=data_dir, slug=slug, uuid=uuid)

    snap = ScenarioSnapshotV2(UUID, data_dir, name='partial')
    with patch.object(RequestSnapshotV2, 'from_entry', side_effect=flaky_from_entry):
      snaps = snap.request_snapshots

    assert len(snaps) == 1
    assert snaps[0].uuid == REQUEST_UUID_B


class TestScenarioSnapshotBackup:
  def test_backup_metadata_and_requests(self):
    data_dir = DataDir.instance()
    slug = 'GET-api-backup'
    body_hash = 'f' * 16
    _plant_slug_blob(data_dir, slug, 'bodies', body_hash, b'backup-body')
    entry = _minimal_entry('https://example.com/api/backup', slug, body_hash)
    path = _write_scenario_yaml(data_dir, 'backup-flow', UUID, {REQUEST_UUID: entry})

    snap = ScenarioSnapshotV2(UUID, data_dir, name='backup-flow')
    snap.backup_metadata()
    snap.backup_requests()

    assert snap.metadata_backup is not None
    assert 'backup-flow' in snap.metadata_backup or UUID in snap.metadata_backup
    with open(path, 'r') as fp:
      assert snap.metadata_backup == fp.read()

    assert snap.requests_backup is not None
    assert REQUEST_UUID in snap.requests_backup
    assert snap.requests_backup[REQUEST_UUID] is not None


class TestScenarioSnapshotHistoryLocatorFresh:
  def test_allocates_stem_when_no_yaml_exists(self):
    data_dir = DataDir.instance()
    locator = ScenarioSnapshotV2.history_locator_for(UUID, 'brand-new', data_dir)
    assert locator == f'brand-new/{UUID}'


class TestScenarioSnapshotUpdatePreservesSiblings:
  def test_update_does_not_rewrite_unrelated_embeds(self):
    data_dir = DataDir.instance()
    keep = _minimal_entry('https://example.com/api/keep', 'GET-api-keep')
    change = _minimal_entry('https://example.com/api/change', 'GET-api-change')
    path = _write_scenario_yaml(
      data_dir,
      'siblings',
      UUID,
      {REQUEST_UUID: change, REQUEST_UUID_B: keep},
    )
    snap = ScenarioSnapshotV2(UUID, data_dir, name='siblings')

    updated = {**change, 'headers': {'X-Changed': 'yes'}, 'response': change['response']}
    snap.update_request_entries({REQUEST_UUID: updated})

    with open(path, 'r') as fp:
      data = yaml.safe_load(fp)
    assert data['requests'][REQUEST_UUID]['headers'] == {'X-Changed': 'yes'}
    assert data['requests'][REQUEST_UUID_B] == keep


class TestScenarioSnapshotMetadataShape:
  def test_metadata_exposes_name_and_description_only(self):
    data_dir = DataDir.instance()
    _write_scenario_yaml(data_dir, 'shape-flow', UUID, {
      REQUEST_UUID: _minimal_entry('https://example.com/', 'GET'),
    })
    # Name comes from stem when YAML omits name
    scenarios_dir = data_dir.snapshots_scenarios_dir_path
    path = os.path.join(scenarios_dir, 'shape-flow.yaml')
    with open(path, 'w') as fp:
      yaml.safe_dump({
        'uuid': UUID,
        'description': 'desc',
        'requests': {REQUEST_UUID: _minimal_entry('https://example.com/', 'GET')},
      }, fp)

    snap = ScenarioSnapshotV2(UUID, data_dir, name='shape-flow')
    meta = snap.metadata
    assert meta == {'name': 'shape-flow', 'description': 'desc'}
    assert 'uuid' not in meta
    assert 'requests' not in meta


class TestScenarioSnapshotPutDropsRequest:
  def test_rewrite_drops_removed_request_embed(self):
    from stoobly_agent.app.models.factories.resource.local_db.helpers.snapshot_service import snapshot_scenario
    from stoobly_agent.app.models.factories.resource.local_db.helpers.snapshot_types import PUT_ACTION
    from stoobly_agent.cli import record
    from stoobly_agent.lib.orm.request import Request
    from stoobly_agent.lib.orm.scenario import Scenario
    from stoobly_agent.test.test_helper import DETERMINISTIC_GET_REQUEST_URL
    from click.testing import CliRunner

    runner = CliRunner()
    scenario = Scenario.create(name='drop-req', description='')
    assert runner.invoke(
      record,
      ['--scenario-key', scenario.key(), DETERMINISTIC_GET_REQUEST_URL],
    ).exit_code == 0
    first = Request.last()
    assert runner.invoke(
      record,
      ['--scenario-key', scenario.key(), DETERMINISTIC_GET_REQUEST_URL],
    ).exit_code == 0
    second = Request.last()
    assert first.uuid != second.uuid

    snapshot_scenario(scenario, action=PUT_ACTION)
    snap = ScenarioSnapshot.create(scenario.uuid)
    assert {s.uuid for s in snap.request_snapshots} == {first.uuid, second.uuid}

    # Drop first request from the scenario ORM and re-snapshot
    first.delete()
    scenario = Scenario.find(scenario.id)
    snapshot_scenario(scenario, action=PUT_ACTION)

    with open(snap.metadata_path, 'r') as fp:
      data = yaml.safe_load(fp)
    assert second.uuid in data['requests']
    assert first.uuid not in data['requests']
    assert ScenarioSnapshot.create(scenario.uuid).request_snapshots[0].uuid == second.uuid
