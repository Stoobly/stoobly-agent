import json
import os
import tempfile
import time

import pytest
import yaml
from click.testing import CliRunner

from stoobly_agent.app.cli.request_cli import request
from stoobly_agent.app.cli.scenario_cli import scenario
from stoobly_agent.app.cli.snapshot_cli import snapshot
from stoobly_agent.app.models.adapters.orm import JoinedRequestStringAdapter
from stoobly_agent.app.models.factories.resource.local_db.helpers.body_ref import BODY_REF_HEADER
from stoobly_agent.app.models.factories.resource.local_db.helpers.log import Log
from stoobly_agent.app.models.factories.resource.local_db.helpers.request_snapshot import RequestSnapshot, RequestSnapshotV2
from stoobly_agent.app.models.factories.resource.local_db.helpers.scenario_snapshot import ScenarioSnapshot
from stoobly_agent.app.models.factories.resource.local_db.helpers.snapshot_format import (
  FORMAT_V1,
  FORMAT_V2,
  detect_snapshot_format,
)
from stoobly_agent.app.models.factories.resource.local_db.helpers.snapshot_migrate import (
  migrate_snapshots,
  migrate_snapshots_to_v1,
  migrate_snapshots_to_v2,
)
from stoobly_agent.app.models.factories.resource.local_db.helpers.snapshot_types import DELETE_ACTION, PUT_ACTION
from stoobly_agent.cli import record
from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.lib.orm.scenario import Scenario
from stoobly_agent.test.test_helper import DETERMINISTIC_GET_REQUEST_URL, reset


@pytest.fixture(scope='module')
def runner():
  return CliRunner()


class TestSnapshotFormatV2:
  @pytest.fixture(scope='class', autouse=True)
  @classmethod
  def settings(cls):
    return reset()

  class TestEmptyDirWritesV2:
    @pytest.fixture(scope='class')
    @classmethod
    def recorded_request(cls, runner: CliRunner):
      record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
      assert record_result.exit_code == 0
      return Request.last()

    def test_writes_v2_layout(self, runner: CliRunner, recorded_request: Request):
      result = runner.invoke(request, ['snapshot', 'create', recorded_request.key()])
      assert result.exit_code == 0

      data_dir = DataDir.instance()
      assert detect_snapshot_format(data_dir) == FORMAT_V2

      slug = RequestSnapshotV2.build_request_slug(recorded_request.method, recorded_request.path)
      snapshot = RequestSnapshot.create(recorded_request.uuid)
      assert snapshot.format == FORMAT_V2
      assert snapshot.path.endswith(f'{slug}/{recorded_request.uuid}.http')
      assert os.path.isfile(snapshot.path)

      # Reconstituted contents match ORM joined bytes
      assert snapshot.request == JoinedRequestStringAdapter(recorded_request).adapt()

      # History stores slug/<uuid> for O(1) apply path resolution
      from stoobly_agent.app.models.factories.resource.local_db.helpers.log import Log
      event = Log().events[-1]
      assert event.resource_uuid == f'{slug}/{recorded_request.uuid}'
      assert event.resource_id == recorded_request.uuid
      assert event.snapshot().path == snapshot.path

  class TestScenarioV2Yaml:
    @pytest.fixture(scope='class', autouse=True)
    @classmethod
    def settings(cls):
      return reset()

    @pytest.fixture(scope='class')
    @classmethod
    def created_scenario(cls, runner: CliRunner):
      create_result = runner.invoke(scenario, ['create', 'checkout-flow'])
      assert create_result.exit_code == 0
      return Scenario.last()

    @pytest.fixture(scope='class', autouse=True)
    @classmethod
    def recorded_request(cls, runner: CliRunner, created_scenario: Scenario):
      record_result = runner.invoke(
        record,
        ['--scenario-key', created_scenario.key(), DETERMINISTIC_GET_REQUEST_URL],
      )
      assert record_result.exit_code == 0
      return Request.last()

    def test_writes_scenario_yaml(self, runner: CliRunner, created_scenario: Scenario, recorded_request: Request):
      result = runner.invoke(scenario, ['snapshot', 'create', created_scenario.key()])
      assert result.exit_code == 0

      snap = ScenarioSnapshot.create(created_scenario.uuid)
      assert snap.format == FORMAT_V2
      assert snap.metadata_path.endswith('checkout-flow.yaml')
      assert snap.metadata['name'] == 'checkout-flow'

      with open(snap.metadata_path, 'r') as fp:
        data = yaml.safe_load(fp)

      assert data['uuid'] == created_scenario.uuid
      assert len(data['requests']) == 1
      assert data['requests'][0].endswith(f'{recorded_request.uuid}.http')
      assert '/' in data['requests'][0]

      assert snap.requests[0] == JoinedRequestStringAdapter(recorded_request).adapt()

      from stoobly_agent.app.models.factories.resource.local_db.helpers.log import Log
      event = Log().events[-1]
      assert event.resource_uuid == 'checkout-flow'
      assert event.resource_id == 'checkout-flow'
      assert event.snapshot().metadata_path == snap.metadata_path
      assert event.snapshot().uuid == created_scenario.uuid
      assert not os.path.exists(
        os.path.join(
          DataDir.instance().snapshots_scenarios_dir_path,
          '.uuid-index',
          created_scenario.uuid,
        )
      )

  class TestMigrateV1ToV2:
    @pytest.fixture(scope='class', autouse=True)
    @classmethod
    def settings(cls):
      return reset()

    @pytest.fixture(scope='class')
    @classmethod
    def recorded_request(cls, runner: CliRunner):
      record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
      assert record_result.exit_code == 0
      return Request.last()

    @pytest.fixture(scope='class', autouse=True)
    @classmethod
    def v1_snapshot(cls, recorded_request: Request):
      # Force v1 write
      from stoobly_agent.app.models.factories.resource.local_db.helpers.snapshot_service import snapshot_request

      path = snapshot_request(recorded_request, action=PUT_ACTION, format=FORMAT_V1)
      assert path is not None
      assert detect_snapshot_format(DataDir.instance()) == FORMAT_V1
      return path

    def test_migrate_creates_v2_files(self, recorded_request: Request, v1_snapshot: str):
      assert os.path.isfile(v1_snapshot)

      result = migrate_snapshots_to_v2(DataDir.instance())
      assert result['requests'] == 1
      assert detect_snapshot_format(DataDir.instance()) == FORMAT_V2
      assert not os.path.exists(v1_snapshot)

      snap = RequestSnapshot.create(recorded_request.uuid)
      assert snap.format == FORMAT_V2
      assert snap.path.endswith('.http')
      assert snap.request == JoinedRequestStringAdapter(recorded_request).adapt()

      # History locators are rewritten; no uuid-index needed
      from stoobly_agent.app.models.factories.resource.local_db.helpers.log import Log

      slug = RequestSnapshotV2.build_request_slug(recorded_request.method, recorded_request.path)
      event = Log().events[-1]
      assert event.resource_uuid == f'{slug}/{recorded_request.uuid}'
      assert event.resource_id == recorded_request.uuid
      assert event.snapshot().path == snap.path

      index_path = os.path.join(
        DataDir.instance().snapshots_requests_dir_path,
        '.uuid-index',
        recorded_request.uuid,
      )
      assert not os.path.exists(index_path)

  class TestMigrateScenarioV1ToV2:
    @pytest.fixture(scope='class', autouse=True)
    @classmethod
    def settings(cls):
      return reset()

    @pytest.fixture(scope='class')
    @classmethod
    def created_scenario(cls, runner: CliRunner):
      create_result = runner.invoke(scenario, ['create', 'legacy-flow'])
      assert create_result.exit_code == 0
      return Scenario.last()

    @pytest.fixture(scope='class')
    @classmethod
    def recorded_request(cls, runner: CliRunner, created_scenario: Scenario):
      record_result = runner.invoke(
        record,
        ['--scenario-key', created_scenario.key(), DETERMINISTIC_GET_REQUEST_URL],
      )
      assert record_result.exit_code == 0
      return Request.last()

    @pytest.fixture(scope='class', autouse=True)
    @classmethod
    def v1_snapshots(cls, created_scenario: Scenario, recorded_request: Request):
      from stoobly_agent.app.models.factories.resource.local_db.helpers.snapshot_service import (
        snapshot_request,
        snapshot_scenario,
      )

      snapshot_request(recorded_request, action=PUT_ACTION, format=FORMAT_V1)
      path = snapshot_scenario(created_scenario, action=PUT_ACTION, format=FORMAT_V1)
      assert path is not None
      assert detect_snapshot_format(DataDir.instance()) == FORMAT_V1
      return path

    def test_migrate_rewrites_history_without_uuid_index(
      self,
      created_scenario: Scenario,
      recorded_request: Request,
    ):
      result = migrate_snapshots_to_v2(DataDir.instance())
      assert result['requests'] == 1
      assert result['scenarios'] == 1
      assert detect_snapshot_format(DataDir.instance()) == FORMAT_V2

      from stoobly_agent.app.models.factories.resource.local_db.helpers.log import Log

      scenario_snap = ScenarioSnapshot.create(created_scenario.uuid)
      assert scenario_snap.format == FORMAT_V2
      assert scenario_snap.metadata_path.endswith('legacy-flow.yaml')

      event = next(e for e in reversed(Log().events) if e.is_scenario())
      assert event.resource_uuid == 'legacy-flow'
      assert event.resource_id == 'legacy-flow'
      assert event.snapshot().metadata_path == scenario_snap.metadata_path
      assert event.snapshot().uuid == created_scenario.uuid

      index_path = os.path.join(
        DataDir.instance().snapshots_scenarios_dir_path,
        '.uuid-index',
        created_scenario.uuid,
      )
      assert not os.path.exists(index_path)

      request_event = next(e for e in reversed(Log().events) if e.is_request() and e.resource_id == recorded_request.uuid)
      assert '/' in request_event.resource_uuid
      assert request_event.resource_id == recorded_request.uuid

  class TestMigrateV2ToV1:
    @pytest.fixture(scope='class', autouse=True)
    @classmethod
    def settings(cls):
      return reset()

    @pytest.fixture(scope='class')
    @classmethod
    def created_scenario(cls, runner: CliRunner):
      create_result = runner.invoke(scenario, ['create', 'migrate-flow'])
      assert create_result.exit_code == 0
      return Scenario.last()

    @pytest.fixture(scope='class')
    @classmethod
    def recorded_request(cls, runner: CliRunner, created_scenario: Scenario):
      record_result = runner.invoke(
        record,
        ['--scenario-key', created_scenario.key(), DETERMINISTIC_GET_REQUEST_URL],
      )
      assert record_result.exit_code == 0
      return Request.last()

    @pytest.fixture(scope='class', autouse=True)
    @classmethod
    def v2_snapshots(cls, runner: CliRunner, created_scenario: Scenario, recorded_request: Request):
      result = runner.invoke(scenario, ['snapshot', 'create', created_scenario.key()])
      assert result.exit_code == 0
      assert detect_snapshot_format(DataDir.instance()) == FORMAT_V2
      return RequestSnapshot.create(recorded_request.uuid).path

    def test_migrate_creates_v1_files(
      self,
      created_scenario: Scenario,
      recorded_request: Request,
      v2_snapshots: str,
    ):
      assert os.path.isfile(v2_snapshots)

      result = migrate_snapshots_to_v1(DataDir.instance())
      assert result['requests'] == 1
      assert result['scenarios'] == 1
      assert detect_snapshot_format(DataDir.instance()) == FORMAT_V1
      assert not os.path.exists(v2_snapshots)

      snap = RequestSnapshot.create(recorded_request.uuid)
      assert snap.format == FORMAT_V1
      assert snap.request == JoinedRequestStringAdapter(recorded_request).adapt()

      scenario_snap = ScenarioSnapshot.create(created_scenario.uuid)
      assert scenario_snap.format == FORMAT_V1
      assert scenario_snap.metadata['name'] == 'migrate-flow'

      with open(scenario_snap.metadata_path, 'r') as fp:
        meta = json.loads(fp.read())
      assert meta['name'] == 'migrate-flow'

      with open(scenario_snap.requests_path, 'r') as fp:
        assert recorded_request.uuid in fp.read()

      # History locators are rewritten back to bare uuids
      from stoobly_agent.app.models.factories.resource.local_db.helpers.log import Log

      events = Log().events
      scenario_event = next(e for e in reversed(events) if e.is_scenario())
      assert scenario_event.resource_uuid == created_scenario.uuid
      assert scenario_event.resource_id == created_scenario.uuid
      assert '/' not in scenario_event.resource_uuid

  class TestMigrateCli:
    @pytest.fixture(autouse=True)
    def settings(self):
      return reset()

    @pytest.fixture
    def recorded_request(self, runner: CliRunner):
      record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
      assert record_result.exit_code == 0
      return Request.last()

    def test_migrate_v1_to_v2(self, runner: CliRunner, recorded_request: Request):
      from stoobly_agent.app.models.factories.resource.local_db.helpers.snapshot_service import snapshot_request

      v1_path = snapshot_request(recorded_request, action=PUT_ACTION, format=FORMAT_V1)
      assert detect_snapshot_format(DataDir.instance()) == FORMAT_V1

      result = runner.invoke(snapshot, ['migrate', '--format', 'v2'])
      assert result.exit_code == 0
      assert 'Migrated 1 request(s) and 0 scenario(s) to v2.' in result.output
      assert detect_snapshot_format(DataDir.instance()) == FORMAT_V2
      assert not os.path.exists(v1_path)

      snap = RequestSnapshot.create(recorded_request.uuid)
      assert snap.format == FORMAT_V2
      assert snap.request == JoinedRequestStringAdapter(recorded_request).adapt()

    def test_migrate_to_v2_is_noop_when_already_v2(self, runner: CliRunner, recorded_request: Request):
      result = runner.invoke(request, ['snapshot', 'create', recorded_request.key()])
      assert result.exit_code == 0
      assert detect_snapshot_format(DataDir.instance()) == FORMAT_V2

      migrate_result = runner.invoke(snapshot, ['migrate', '--format', 'v2'])
      assert migrate_result.exit_code == 0
      assert 'Snapshots are already in v2 format.' in migrate_result.output

      noop = migrate_snapshots(DataDir.instance(), format=FORMAT_V2)
      assert noop['noop'] is True
      assert noop['requests'] == 0
      assert noop['scenarios'] == 0

    def test_migrate_v2_to_v1(self, runner: CliRunner, recorded_request: Request):
      create_result = runner.invoke(request, ['snapshot', 'create', recorded_request.key()])
      assert create_result.exit_code == 0
      assert detect_snapshot_format(DataDir.instance()) == FORMAT_V2

      result = runner.invoke(snapshot, ['migrate', '--format', 'v1'])
      assert result.exit_code == 0
      assert 'Migrated 1 request(s) and 0 scenario(s) to v1.' in result.output
      assert detect_snapshot_format(DataDir.instance()) == FORMAT_V1

      snap = RequestSnapshot.create(recorded_request.uuid)
      assert snap.format == FORMAT_V1
      assert snap.request == JoinedRequestStringAdapter(recorded_request).adapt()

    def test_migrate_to_v1_is_noop_when_already_v1(self, runner: CliRunner, recorded_request: Request):
      from stoobly_agent.app.models.factories.resource.local_db.helpers.snapshot_service import snapshot_request

      snapshot_request(recorded_request, action=PUT_ACTION, format=FORMAT_V1)
      assert detect_snapshot_format(DataDir.instance()) == FORMAT_V1

      result = runner.invoke(snapshot, ['migrate', '--format', 'v1'])
      assert result.exit_code == 0
      assert 'Snapshots are already in v1 format.' in result.output

    def test_migrate_empty_dir_is_noop(self, runner: CliRunner):
      assert detect_snapshot_format(DataDir.instance()) is None

      result = runner.invoke(snapshot, ['migrate', '--format', 'v2'])
      assert result.exit_code == 0
      assert 'No snapshots to migrate.' in result.output

      noop = migrate_snapshots(DataDir.instance(), format=FORMAT_V2)
      assert noop['noop'] is True

  class TestMigrateEdgeCases:
    @pytest.fixture(autouse=True)
    def settings(self):
      return reset()

    @pytest.fixture
    def recorded_request(self, runner: CliRunner):
      assert runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL]).exit_code == 0
      return Request.last()

    def test_remigrate_finishes_interrupted_v1_to_v2(self, recorded_request: Request):
      from stoobly_agent.app.models.factories.resource.local_db.helpers.snapshot_service import snapshot_request

      snapshot_request(recorded_request, action=PUT_ACTION, format=FORMAT_V1)
      assert migrate_snapshots_to_v2(DataDir.instance())['requests'] == 1
      assert detect_snapshot_format(DataDir.instance()) == FORMAT_V2

      # Plant leftover v1 file (interrupted migrate left a mixed tree)
      leftover_uuid = 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb'
      shard = os.path.join(DataDir.instance().snapshots_requests_dir_path, leftover_uuid[0:2])
      os.makedirs(shard, exist_ok=True)
      leftover_path = os.path.join(shard, leftover_uuid)
      with open(leftover_path, 'wb') as fp:
        fp.write(RequestSnapshot.create(recorded_request.uuid).request)

      assert detect_snapshot_format(DataDir.instance()) == FORMAT_V2

      result = migrate_snapshots(DataDir.instance(), format=FORMAT_V2)
      assert result['noop'] is False
      assert result['requests'] == 1
      assert not os.path.exists(leftover_path)
      assert RequestSnapshot.create(leftover_uuid).format == FORMAT_V2

      noop = migrate_snapshots(DataDir.instance(), format=FORMAT_V2)
      assert noop['noop'] is True

    def test_skips_corrupt_v1_request(self, recorded_request: Request):
      from stoobly_agent.app.models.factories.resource.local_db.helpers.snapshot_service import snapshot_request

      good_path = snapshot_request(recorded_request, action=PUT_ACTION, format=FORMAT_V1)
      corrupt_uuid = 'cccccccc-cccc-cccc-cccc-cccccccccccc'
      shard = os.path.join(DataDir.instance().snapshots_requests_dir_path, corrupt_uuid[0:2])
      os.makedirs(shard, exist_ok=True)
      corrupt_path = os.path.join(shard, corrupt_uuid)
      with open(corrupt_path, 'wb') as fp:
        fp.write(b'not-a-joined-request')

      result = migrate_snapshots_to_v2(DataDir.instance())
      assert result['requests'] == 1
      assert os.path.isfile(corrupt_path)
      assert not os.path.exists(good_path)
      assert RequestSnapshot.create(recorded_request.uuid).format == FORMAT_V2

    def test_skips_corrupt_v2_request(self, recorded_request: Request):
      from stoobly_agent.app.models.factories.resource.local_db.helpers.snapshot_service import snapshot_request

      snapshot_request(recorded_request, action=PUT_ACTION, format=FORMAT_V2)
      good_path = RequestSnapshot.create(recorded_request.uuid).path

      corrupt_uuid = 'dddddddd-dddd-dddd-dddd-dddddddddddd'
      slug_dir = os.path.join(DataDir.instance().snapshots_requests_dir_path, 'GET-corrupt')
      os.makedirs(slug_dir, exist_ok=True)
      corrupt_path = os.path.join(slug_dir, f'{corrupt_uuid}.http')
      with open(corrupt_path, 'wb') as fp:
        fp.write(b'junk')

      result = migrate_snapshots_to_v1(DataDir.instance())
      assert result['requests'] == 1
      assert os.path.isfile(corrupt_path)
      assert not os.path.exists(good_path)
      assert RequestSnapshot.create(recorded_request.uuid).format == FORMAT_V1

    def test_skips_corrupt_scenario_yaml(self, runner: CliRunner, recorded_request: Request):
      assert runner.invoke(request, ['snapshot', 'create', recorded_request.key()]).exit_code == 0

      scenarios_dir = DataDir.instance().snapshots_scenarios_dir_path
      os.makedirs(scenarios_dir, exist_ok=True)
      bad_yaml = os.path.join(scenarios_dir, 'broken.yaml')
      with open(bad_yaml, 'w') as fp:
        fp.write('not: valid: yaml: [')

      no_uuid_yaml = os.path.join(scenarios_dir, 'no-uuid.yaml')
      with open(no_uuid_yaml, 'w') as fp:
        yaml.safe_dump({'description': 'x', 'requests': []}, fp)

      result = migrate_snapshots_to_v1(DataDir.instance())
      assert result['scenarios'] == 0
      assert os.path.isfile(bad_yaml)
      assert os.path.isfile(no_uuid_yaml)
      assert result['requests'] == 1

    def test_scenario_name_collision_uses_unique_stem(self, runner: CliRunner):
      from stoobly_agent.app.models.factories.resource.local_db.helpers.snapshot_service import snapshot_scenario

      assert runner.invoke(scenario, ['create', 'dup-name']).exit_code == 0
      first = Scenario.last()
      snapshot_scenario(first, action=PUT_ACTION, format=FORMAT_V1)

      # Plant a second v1 scenario metadata with the same display name
      other_uuid = 'eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee'
      meta_path = os.path.join(DataDir.instance().snapshots_scenarios_dir_path, other_uuid)
      with open(meta_path, 'w') as fp:
        json.dump({'name': 'dup-name', 'description': ''}, fp)

      index_dir = DataDir.instance().snapshots_scenario_requests_dir_path
      os.makedirs(index_dir, exist_ok=True)
      with open(os.path.join(index_dir, other_uuid), 'w') as fp:
        fp.write('')

      # History line for the planted scenario (bare uuid)
      from stoobly_agent.app.models.factories.resource.local_db.helpers.log_event import LogEvent, SCENARIO_RESOURCE
      Log().append(LogEvent.serialize(SCENARIO_RESOURCE, other_uuid, PUT_ACTION))

      result = migrate_snapshots_to_v2(DataDir.instance())
      assert result['scenarios'] == 2

      scenarios_dir = DataDir.instance().snapshots_scenarios_dir_path
      assert os.path.isfile(os.path.join(scenarios_dir, 'dup-name.yaml'))
      assert os.path.isfile(os.path.join(scenarios_dir, 'dup-name-2.yaml'))

      def locator_for(scenario_uuid: str) -> str:
        for event in Log().events:
          if not event.is_scenario():
            continue
          if ScenarioSnapshot.create(event.resource_uuid).uuid == scenario_uuid:
            return event.resource_uuid
        raise AssertionError(f'no history locator for {scenario_uuid}')

      locators = {locator_for(first.uuid), locator_for(other_uuid)}
      assert locators == {'dup-name', 'dup-name-2'}

    def test_legacy_scenario_name_uuid_locator_collapsed(self, runner: CliRunner):
      from stoobly_agent.app.models.factories.resource.local_db.helpers.log_event import LogEvent, SCENARIO_RESOURCE
      from stoobly_agent.app.models.factories.resource.local_db.helpers.snapshot_service import snapshot_scenario

      assert runner.invoke(scenario, ['create', 'legacy-loc']).exit_code == 0
      created = Scenario.last()
      snapshot_scenario(created, action=PUT_ACTION, format=FORMAT_V1)

      # Replace last history locator with legacy name/uuid form
      log = Log()
      history_files = log.history_files
      assert history_files
      path = history_files[-1]
      with open(path, 'r') as fp:
        lines = [l for l in fp.read().split('\n') if l]
      legacy = LogEvent.serialize(SCENARIO_RESOURCE, f'legacy-loc/{created.uuid}', PUT_ACTION)
      with open(path, 'w') as fp:
        fp.write('\n'.join(lines[:-1] + [legacy]) + '\n')

      migrate_snapshots_to_v2(DataDir.instance())
      event = next(e for e in reversed(Log().events) if e.is_scenario())
      assert event.resource_uuid == 'legacy-loc'
      assert '/' not in event.resource_uuid

      migrate_snapshots_to_v1(DataDir.instance())
      event = next(e for e in reversed(Log().events) if e.is_scenario())
      assert event.resource_uuid == created.uuid

    def test_rewrites_archived_history_and_preserves_version(self, recorded_request: Request):
      from stoobly_agent.app.models.factories.resource.local_db.helpers.log_event import LogEvent, REQUEST_RESOURCE
      from stoobly_agent.app.models.factories.resource.local_db.helpers.snapshot_service import snapshot_request

      snapshot_request(recorded_request, action=PUT_ACTION, format=FORMAT_V1)
      log = Log()
      event = log.events[-1]
      version_before = log.generate_version([event.uuid])
      log.version = version_before

      # Archived history file with a bare-uuid locator (not the active bucket)
      archived = os.path.join(log.history_dir_path, '1000000000')
      archived_line = LogEvent.serialize(REQUEST_RESOURCE, recorded_request.uuid, PUT_ACTION)
      with open(archived, 'w') as fp:
        fp.write(archived_line + '\n')

      migrate_snapshots_to_v2(DataDir.instance())

      assert Log().version == version_before
      with open(archived, 'r') as fp:
        rewritten = fp.read().strip()
      archived_event = LogEvent.create(rewritten)
      assert '/' in archived_event.resource_uuid
      assert archived_event.resource_id == recorded_request.uuid
      assert archived_event.uuid == archived_line.split()[0]

    def test_removes_planted_uuid_index(self, recorded_request: Request):
      from stoobly_agent.app.models.factories.resource.local_db.helpers.snapshot_service import snapshot_request

      snapshot_request(recorded_request, action=PUT_ACTION, format=FORMAT_V1)
      index_dir = os.path.join(DataDir.instance().snapshots_requests_dir_path, '.uuid-index')
      os.makedirs(index_dir, exist_ok=True)
      index_path = os.path.join(index_dir, recorded_request.uuid)
      with open(index_path, 'w') as fp:
        fp.write('GET-api/' + recorded_request.uuid + '.http')

      migrate_snapshots_to_v2(DataDir.instance())
      assert not os.path.isdir(index_dir)

    def test_v2_to_v1_rewrites_request_history_and_cleans_bodies(self, runner: CliRunner, recorded_request: Request):
      assert runner.invoke(request, ['snapshot', 'create', recorded_request.key()]).exit_code == 0
      v2 = RequestSnapshot.create(recorded_request.uuid)
      slug_dir = os.path.dirname(v2.path)
      bodies_dir = os.path.join(slug_dir, 'bodies')
      assert os.path.isdir(bodies_dir)

      event_before = Log().events[-1]
      assert '/' in event_before.resource_uuid

      result = migrate_snapshots_to_v1(DataDir.instance())
      assert result['requests'] == 1

      event_after = Log().events[-1]
      assert event_after.uuid == event_before.uuid
      assert event_after.resource_uuid == recorded_request.uuid
      assert '/' not in event_after.resource_uuid
      assert not os.path.isdir(bodies_dir)
      assert not os.path.isdir(slug_dir)

    def test_preserves_malformed_history_line(self, recorded_request: Request):
      from stoobly_agent.app.models.factories.resource.local_db.helpers.snapshot_service import snapshot_request

      snapshot_request(recorded_request, action=PUT_ACTION, format=FORMAT_V1)
      log = Log()
      path = log.history_files[-1]
      with open(path, 'a') as fp:
        fp.write('not-enough-fields\n')

      migrate_snapshots_to_v2(DataDir.instance())

      with open(path, 'r') as fp:
        contents = fp.read()
      assert 'not-enough-fields' in contents
      assert any('/' in line and recorded_request.uuid in line for line in contents.split('\n') if line)

  class TestCopyV2WithBodies:
    @pytest.fixture(autouse=True)
    def settings(self):
      return reset()

    @pytest.fixture
    def recorded_request(self, runner: CliRunner):
      record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
      assert record_result.exit_code == 0
      return Request.last()

    def test_copy_includes_http_and_bodies(self, runner: CliRunner, recorded_request: Request):
      create_result = runner.invoke(request, ['snapshot', 'create', recorded_request.key()])
      assert create_result.exit_code == 0

      source = RequestSnapshot.create(recorded_request.uuid)
      assert source.format == FORMAT_V2
      assert os.path.isfile(source.path)

      with open(source.path, 'rb') as fp:
        on_disk = fp.read()
      assert BODY_REF_HEADER.encode() in on_disk

      slug_dir = os.path.dirname(source.path)
      bodies_dir = os.path.join(slug_dir, 'bodies')
      assert os.path.isdir(bodies_dir)
      body_names = os.listdir(bodies_dir)
      assert len(body_names) >= 1

      with tempfile.TemporaryDirectory() as dirpath:
        copy_result = runner.invoke(snapshot, ['copy', dirpath, '--request-key', recorded_request.key()])
        assert copy_result.exit_code == 0

        dest_data_dir = DataDir.instance(dirpath)
        dest = RequestSnapshot.create(recorded_request.uuid, dest_data_dir)
        assert dest.format == FORMAT_V2
        assert os.path.isfile(dest.path)

        dest_bodies = os.path.join(os.path.dirname(dest.path), 'bodies')
        assert os.path.isdir(dest_bodies)
        for name in body_names:
          assert os.path.isfile(os.path.join(dest_bodies, name))

        assert dest.request == source.request

  class TestScenarioDeleteAndPruneV2:
    @pytest.fixture(autouse=True)
    def settings(self):
      return reset()

    @pytest.fixture
    def created_scenario(self, runner: CliRunner):
      create_result = runner.invoke(scenario, ['create', 'delete-flow'])
      assert create_result.exit_code == 0
      return Scenario.last()

    @pytest.fixture
    def recorded_request(self, runner: CliRunner, created_scenario: Scenario):
      record_result = runner.invoke(
        record,
        ['--scenario-key', created_scenario.key(), DETERMINISTIC_GET_REQUEST_URL],
      )
      assert record_result.exit_code == 0
      return Request.last()

    def test_scenario_delete_removes_request_files(
      self,
      runner: CliRunner,
      created_scenario: Scenario,
      recorded_request: Request,
    ):
      put_result = runner.invoke(scenario, ['snapshot', 'create', created_scenario.key()])
      assert put_result.exit_code == 0

      scenario_snap = ScenarioSnapshot.create(created_scenario.uuid)
      request_snap = RequestSnapshot.create(recorded_request.uuid)
      assert scenario_snap.format == FORMAT_V2

      metadata_path = scenario_snap.metadata_path
      request_path = request_snap.path
      slug_dir = os.path.dirname(request_path)
      bodies_dir = os.path.join(slug_dir, 'bodies')
      assert os.path.isfile(metadata_path)
      assert os.path.isfile(request_path)
      assert os.path.isdir(bodies_dir)

      delete_result = runner.invoke(
        scenario,
        ['snapshot', 'create', '--action', DELETE_ACTION, created_scenario.key()],
      )
      assert delete_result.exit_code == 0

      # Use saved paths: accessing RequestSnapshot.path can recreate the slug dir
      assert not os.path.exists(metadata_path)
      assert not os.path.exists(request_path)
      assert not os.path.isdir(slug_dir)

    def test_prune_removes_deleted_scenario_history(
      self,
      runner: CliRunner,
      created_scenario: Scenario,
      recorded_request: Request,
    ):
      put_result = runner.invoke(scenario, ['snapshot', 'create', created_scenario.key()])
      assert put_result.exit_code == 0

      request_path = RequestSnapshot.create(recorded_request.uuid).path
      metadata_path = ScenarioSnapshot.create(created_scenario.uuid).metadata_path
      assert os.path.isfile(request_path)
      assert os.path.isfile(metadata_path)

      time.sleep(0.5)
      delete_result = runner.invoke(
        scenario,
        ['snapshot', 'create', '--action', DELETE_ACTION, created_scenario.key()],
      )
      assert delete_result.exit_code == 0
      assert not os.path.exists(request_path)
      assert not os.path.exists(metadata_path)

      log = Log()
      assert len(log.events) >= 2

      prune_result = runner.invoke(snapshot, ['prune'])
      assert prune_result.exit_code == 0
      assert len(Log().events) == 0
