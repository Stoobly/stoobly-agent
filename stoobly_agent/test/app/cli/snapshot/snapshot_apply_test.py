import os
import pdb
import pytest
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

from click.testing import CliRunner
from typing import List

from stoobly_agent.app.cli.request_cli import request
from stoobly_agent.app.cli.scenario_cli import scenario
from stoobly_agent.app.cli.snapshot_cli import snapshot
from stoobly_agent.app.models.factories.resource.local_db.helpers.log import Log
from stoobly_agent.app.models.factories.resource.local_db.helpers.log_event import DELETE_ACTION, LogEvent
from stoobly_agent.app.models.factories.resource.local_db.helpers.request_snapshot import RequestSnapshotV2
from stoobly_agent.app.models.factories.resource.local_db.helpers.scenario_snapshot import ScenarioSnapshot
from stoobly_agent.cli import record
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.lib.orm.scenario import Scenario
from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.test.test_helper import assert_orm_request_equivalent, DETERMINISTIC_GET_REQUEST_URL, NON_DETERMINISTIC_GET_REQUEST_URL, reset

def write_junk(path: str):
  with open(path, 'w') as fp:
    fp.write('junk')

def create_pending_request_snapshots(runner: CliRunner, urls: List[str]) -> List[LogEvent]:
  # Mark events from previous tests as processed so only the snapshots created here are pending
  log = Log()
  log.version = log.generate_version(log.uuids())

  for url in urls:
    record_result = runner.invoke(record, [url])
    assert record_result.exit_code == 0
    recorded_request = Request.last()

    snapshot_result = runner.invoke(request, ['snapshot', 'create', recorded_request.key()])
    assert snapshot_result.exit_code == 0

  return Log().unprocessed_events

@pytest.fixture(scope='module')
def runner():
    return CliRunner()

class TestApply():
    @pytest.fixture(scope='class', autouse=True)
    @classmethod
    def settings(cls):
      return reset()

    class TestWhenDeletingRequest():

      @pytest.fixture(scope='class')
      @classmethod
      def log(cls):
        return Log()

      @pytest.fixture(scope='class')
      @classmethod
      def recorded_request(cls, runner: CliRunner):
        record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
        assert record_result.exit_code == 0
        return Request.last()

      @pytest.fixture(autouse=True, scope='class')
      @classmethod
      def events(cls, runner: CliRunner, recorded_request: Request, log: Log):
        snapshot_result = runner.invoke(request, ['snapshot', 'create', recorded_request.key()])
        assert snapshot_result.exit_code == 0

        events = log.events
        event: LogEvent = events[len(events) - 1]
        log.version = event.uuid

        time.sleep(1)

        snapshot_result = runner.invoke(request, ['snapshot', 'create', '--action', DELETE_ACTION, recorded_request.key()])
        assert snapshot_result.exit_code == 0

        return log.events

      @pytest.fixture(scope='class')
      @classmethod
      def delete_event(cls, events: List[LogEvent]):
        return events[1]

      def test_it_deletes(self, runner: CliRunner, recorded_request: Request, delete_event: LogEvent):
        apply_result = runner.invoke(snapshot, ['apply', '--force', delete_event.uuid])
        assert apply_result.exit_code == 0

        _request = Request.find(recorded_request.id)
        assert _request == None

    class TestWhenCreatingRequest():

      @pytest.fixture(scope='function')
      def recorded_request(self, runner: CliRunner):
        record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
        assert record_result.exit_code == 0
        return Request.last()

      @pytest.fixture(autouse=True, scope='function')
      def put_event(self, runner: CliRunner, recorded_request: Request):
        snapshot_result = runner.invoke(request, ['snapshot', 'create', recorded_request.key()])
        assert snapshot_result.exit_code == 0

        log = Log()
        events = log.events
        return events[len(events) - 1]

      def test_it_creates_request(self, runner: CliRunner, recorded_request: Request):
        recorded_request.delete()
        assert Request.find(recorded_request.id) == None

        apply_result = runner.invoke(snapshot, ['apply'])
        assert apply_result.exit_code == 0

        _request = Request.find_by(uuid=recorded_request.uuid)
        assert _request != None
        assert_orm_request_equivalent(_request, recorded_request)

      def test_idempotent(self, runner: CliRunner, recorded_request: Request, put_event: LogEvent):
        apply_result = runner.invoke(snapshot, ['apply', put_event.uuid])
        assert apply_result.exit_code == 0

        _request = Request.find_by(uuid=recorded_request.uuid)
        assert_orm_request_equivalent(_request, recorded_request)

    class TestWhenUpdatingRequestMethodPath():
      '''
      1. Record request, snapshot (old slug)
      2. CLI update --method/--path, snapshot again (slug relocates, orphan removed)
      3. Delete ORM request
      4. Apply
      5. Expect recreated request with new method/path; history collapses by UUID
      '''

      NEW_METHOD = 'POST'
      NEW_PATH = '/api/renamed'

      @pytest.fixture(scope='class')
      @classmethod
      def recorded_request(cls, runner: CliRunner):
        record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
        assert record_result.exit_code == 0
        return Request.last()

      @pytest.fixture(scope='class', autouse=True)
      @classmethod
      def first_snapshot(cls, runner: CliRunner, recorded_request: Request):
        snapshot_result = runner.invoke(request, ['snapshot', 'create', recorded_request.key()])
        assert snapshot_result.exit_code == 0

        old_slug = RequestSnapshotV2.build_request_slug(
          recorded_request.method, recorded_request.path
        )
        old_path = RequestSnapshotV2(recorded_request.uuid, slug=old_slug).path
        assert os.path.isfile(old_path)

        event = Log().events[-1]
        assert event.resource_id == recorded_request.uuid
        assert event.resource_uuid == f'{old_slug}/{recorded_request.uuid}'
        return old_path

      @pytest.fixture(scope='class', autouse=True)
      @classmethod
      def updated_snapshot(cls, runner: CliRunner, recorded_request: Request, first_snapshot: str):
        update_result = runner.invoke(
          request,
          [
            'update',
            recorded_request.key(),
            '--method', cls.NEW_METHOD,
            '--path', cls.NEW_PATH,
          ],
        )
        assert update_result.exit_code == 0

        recorded_request = Request.find(recorded_request.id)
        assert recorded_request.method == cls.NEW_METHOD
        assert recorded_request.path == cls.NEW_PATH

        snapshot_result = runner.invoke(request, ['snapshot', 'create', recorded_request.key()])
        assert snapshot_result.exit_code == 0

        new_slug = RequestSnapshotV2.build_request_slug(cls.NEW_METHOD, cls.NEW_PATH)
        new_path = RequestSnapshotV2(recorded_request.uuid, slug=new_slug).path
        assert os.path.isfile(new_path)
        assert not os.path.exists(first_snapshot)

        event = Log().events[-1]
        assert event.resource_id == recorded_request.uuid
        assert event.resource_uuid == f'{new_slug}/{recorded_request.uuid}'

        targets = [
          e for e in Log().target_events
          if e.is_request() and e.resource_id == recorded_request.uuid
        ]
        assert len(targets) == 1
        assert targets[0].resource_uuid == f'{new_slug}/{recorded_request.uuid}'
        return new_path

      @pytest.fixture(scope='class', autouse=True)
      @classmethod
      def recreated_request(cls, runner: CliRunner, recorded_request: Request, updated_snapshot: str):
        uuid = recorded_request.uuid
        recorded_request.delete()
        assert Request.find_by(uuid=uuid) is None

        apply_result = runner.invoke(snapshot, ['apply'])
        assert apply_result.exit_code == 0

        recreated = Request.find_by(uuid=uuid)
        assert recreated is not None
        assert os.path.isfile(updated_snapshot)
        return recreated

      def test_it_applies_updated_method_and_path(self, recreated_request: Request):
        assert recreated_request.method == self.NEW_METHOD
        assert recreated_request.path == self.NEW_PATH

      def test_it_keeps_relocated_slug(self, recreated_request: Request):
        new_slug = RequestSnapshotV2.build_request_slug(self.NEW_METHOD, self.NEW_PATH)
        snap = RequestSnapshotV2(recreated_request.uuid, slug=new_slug)
        assert snap.path.endswith(f'{new_slug}/{recreated_request.uuid}.http')
        assert os.path.isfile(snap.path)

    class TestWhenDeletingScenario():

      @pytest.fixture(scope='class')
      @classmethod
      def log(cls):
        return Log()

      @pytest.fixture(scope='class')
      @classmethod
      def created_scenario(cls, runner: CliRunner):
          create_result = runner.invoke(scenario, ['create', 'test'])
          assert create_result.exit_code == 0
          return Scenario.last()

      @pytest.fixture(autouse=True, scope='class')
      @classmethod
      def events(cls, runner: CliRunner, created_scenario: Scenario, log: Log):
        snapshot_result = runner.invoke(scenario, ['snapshot', 'create',  created_scenario.key()])
        assert snapshot_result.exit_code == 0

        events = log.events
        event: LogEvent = events[len(events) - 1]
        log.version = event.uuid

        time.sleep(1)

        snapshot_result = runner.invoke(scenario, ['snapshot', 'create', '--action', DELETE_ACTION, created_scenario.key()])
        assert snapshot_result.exit_code == 0

        return log.events

      @pytest.fixture(scope='class')
      @classmethod
      def delete_event(cls, events):
        return events[1]

      def test_it_deletes(self, runner: CliRunner, created_scenario: Scenario, delete_event: LogEvent):
        snapshot_result = runner.invoke(snapshot, ['apply', '--force', delete_event.uuid])
        assert snapshot_result.exit_code == 0

        scenario = Scenario.find(created_scenario.id)

        assert scenario == None

    class TestWhenCreatingScenario():

      @pytest.fixture(scope='class')
      @classmethod
      def created_scenario(cls, runner: CliRunner):
          create_result = runner.invoke(scenario, ['create', 'test'])
          assert create_result.exit_code == 0
          return Scenario.last()

      @pytest.fixture(scope='class', autouse=True)
      @classmethod
      def created_scenario_requests(cls, runner: CliRunner, created_scenario: Scenario):
          record_result = runner.invoke(record, ['--scenario-key', created_scenario.key(), DETERMINISTIC_GET_REQUEST_URL])
          assert record_result.exit_code == 0

          record_result = runner.invoke(record, ['--scenario-key', created_scenario.key(), NON_DETERMINISTIC_GET_REQUEST_URL])
          assert record_result.exit_code == 0

          return created_scenario.requests

      @pytest.fixture(scope='class', autouse=True)
      @classmethod
      def put_event(cls, runner: CliRunner, created_scenario: Scenario):
        snapshot_result = runner.invoke(scenario, ['snapshot', 'create', created_scenario.key()])
        assert snapshot_result.exit_code == 0

        log = Log()
        events = log.events
        return events[len(events) - 1]

      @pytest.fixture(scope='class', autouse=True)
      @classmethod
      def recreated_scenario(cls, runner: CliRunner, created_scenario: Scenario):
        requests = created_scenario.requests

        created_scenario.delete()
        assert Scenario.find(created_scenario.id) == None

        for request in requests:
          request.delete()
          assert Request.find(request.id) == None

        apply_result = runner.invoke(snapshot, ['apply'])
        assert apply_result.exit_code == 0

        _scenario = Scenario.find_by(uuid=created_scenario.uuid)
        assert _scenario != None

        return _scenario

      def test_it_creates_scenario(self, created_scenario: Scenario, recreated_scenario: Scenario):
        assert recreated_scenario.requests_count == 2
        assert recreated_scenario.name == created_scenario.name
        assert recreated_scenario.description == created_scenario.description

      def test_it_creates_requests(self, created_scenario_requests: List[Request], recreated_scenario: Scenario):
        requests = recreated_scenario.requests
        assert len(requests) == 2

        assert_orm_request_equivalent(requests[0], created_scenario_requests[0])
        assert_orm_request_equivalent(requests[1], created_scenario_requests[1])

    class TestWhenRenamingScenario():
      '''
      1. Create scenario old-name, record a request, snapshot
      2. Rename to new-name, snapshot again (YAML relocates)
      3. Delete ORM scenario (+ requests)
      4. Apply
      5. Expect recreated scenario named new-name; history collapses by UUID
      '''

      @pytest.fixture(scope='class')
      @classmethod
      def created_scenario(cls, runner: CliRunner):
        create_result = runner.invoke(scenario, ['create', 'rename-old'])
        assert create_result.exit_code == 0
        return Scenario.last()

      @pytest.fixture(scope='class', autouse=True)
      @classmethod
      def recorded_request(cls, runner: CliRunner, created_scenario: Scenario):
        record_result = runner.invoke(
          record, ['--scenario-key', created_scenario.key(), DETERMINISTIC_GET_REQUEST_URL]
        )
        assert record_result.exit_code == 0
        return Request.last()

      @pytest.fixture(scope='class', autouse=True)
      @classmethod
      def first_snapshot(cls, runner: CliRunner, created_scenario: Scenario):
        snapshot_result = runner.invoke(scenario, ['snapshot', 'create', created_scenario.key()])
        assert snapshot_result.exit_code == 0

        scenarios_dir = DataDir.instance().snapshots_scenarios_dir_path
        old_path = os.path.join(scenarios_dir, 'rename-old.yaml')
        assert os.path.isfile(old_path)

        event = Log().events[-1]
        assert event.resource_id == created_scenario.uuid
        assert event.resource_uuid == f'rename-old/{created_scenario.uuid}'
        return old_path

      @pytest.fixture(scope='class', autouse=True)
      @classmethod
      def renamed_snapshot(cls, runner: CliRunner, created_scenario: Scenario, first_snapshot: str):
        assert created_scenario.update({'name': 'rename-new'})
        created_scenario = Scenario.find(created_scenario.id)

        snapshot_result = runner.invoke(scenario, ['snapshot', 'create', created_scenario.key()])
        assert snapshot_result.exit_code == 0

        scenarios_dir = DataDir.instance().snapshots_scenarios_dir_path
        new_path = os.path.join(scenarios_dir, 'rename-new.yaml')
        assert os.path.isfile(new_path)
        assert not os.path.exists(first_snapshot)

        event = Log().events[-1]
        assert event.resource_id == created_scenario.uuid
        assert event.resource_uuid == f'rename-new/{created_scenario.uuid}'

        targets = [e for e in Log().target_events if e.is_scenario() and e.resource_id == created_scenario.uuid]
        assert len(targets) == 1
        assert targets[0].resource_uuid == f'rename-new/{created_scenario.uuid}'
        return new_path

      @pytest.fixture(scope='class', autouse=True)
      @classmethod
      def recreated_scenario(cls, runner: CliRunner, created_scenario: Scenario, renamed_snapshot: str):
        requests = list(created_scenario.requests)
        uuid = created_scenario.uuid

        created_scenario.delete()
        assert Scenario.find_by(uuid=uuid) is None
        for request in requests:
          request.delete()

        apply_result = runner.invoke(snapshot, ['apply'])
        assert apply_result.exit_code == 0

        recreated = Scenario.find_by(uuid=uuid)
        assert recreated is not None
        assert os.path.isfile(renamed_snapshot)
        return recreated

      def test_it_applies_renamed_scenario(self, created_scenario: Scenario, recreated_scenario: Scenario):
        assert recreated_scenario.uuid == created_scenario.uuid
        assert recreated_scenario.name == 'rename-new'
        assert recreated_scenario.requests_count == 1

      def test_it_keeps_relocated_yaml(self, recreated_scenario: Scenario):
        snap = ScenarioSnapshot.create(recreated_scenario.uuid)
        assert snap.metadata_path.endswith('rename-new.yaml')
        assert snap.metadata['name'] == 'rename-new'

    class TestWhenMergingScenario():
      class TestWhenScenarioNameAlreadyExists():
        @pytest.fixture(scope='class')
        @classmethod
        def source_scenario(cls, runner: CliRunner):
          create_result = runner.invoke(scenario, ['create', 'test'])
          assert create_result.exit_code == 0
          return Scenario.last()

        @pytest.fixture(scope='class', autouse=True)
        @classmethod
        def put_event(cls, runner: CliRunner, source_scenario: Scenario):
          snapshot_result = runner.invoke(scenario, ['snapshot', 'create', source_scenario.key()])
          assert snapshot_result.exit_code == 0

          log = Log()
          events = log.events
          return events[len(events) - 1]

        @pytest.fixture(scope='class')
        @classmethod
        def duplicate_named_scenario(cls, runner: CliRunner, source_scenario: Scenario):
          source_scenario.delete()
          assert Scenario.find(source_scenario.id) == None

          create_result = runner.invoke(scenario, ['create', source_scenario.name])
          assert create_result.exit_code == 0
          return Scenario.last()

        @pytest.fixture(scope='class')
        @classmethod
        def apply_result(cls, runner: CliRunner):
          return runner.invoke(snapshot, ['apply'])

        def test_it_updates_existing_scenario_with_snapshot_uuid(
          self,
          source_scenario: Scenario,
          duplicate_named_scenario: Scenario,
          apply_result,
        ):
          assert apply_result.exit_code == 0

          updated_scenario = Scenario.find_by(uuid=source_scenario.uuid)
          assert updated_scenario != None
          assert updated_scenario.id == duplicate_named_scenario.id
          assert updated_scenario.name == source_scenario.name


      class TestWhenAdditionalRequestExists():
        '''
        1. Create scenario
        2. Add 2 requests to it
        3. Snapshot
        4. Add 1 request to it
        5. Apply
        6. Expect scenario to have first 2 requests
        '''

        @pytest.fixture(scope='class')
        @classmethod
        def created_scenario(cls, runner: CliRunner):
          create_result = runner.invoke(scenario, ['create', 'test'])
          assert create_result.exit_code == 0
          return Scenario.last()

        @pytest.fixture(scope='class', autouse=True)
        @classmethod
        def created_scenario_requests(cls, runner: CliRunner, created_scenario: Scenario):
          record_result = runner.invoke(record, ['--scenario-key', created_scenario.key(), DETERMINISTIC_GET_REQUEST_URL])
          assert record_result.exit_code == 0

          record_result = runner.invoke(record, ['--scenario-key', created_scenario.key(), NON_DETERMINISTIC_GET_REQUEST_URL])
          assert record_result.exit_code == 0

          return created_scenario.requests

        @pytest.fixture(scope='class', autouse=True)
        @classmethod
        def put_event(cls, runner: CliRunner, created_scenario: Scenario):
          snapshot_result = runner.invoke(scenario, ['snapshot', 'create', created_scenario.key()])
          assert snapshot_result.exit_code == 0

          log = Log()
          events = log.events
          return events[len(events) - 1]

        # This request was created after the snapshot
        # Later when we apply changes, we expect this request to not exist
        @pytest.fixture(scope='class', autouse=True)
        @classmethod
        def new_scenario_request(cls, runner: CliRunner, created_scenario: Scenario, put_event: LogEvent):
          assert put_event.resource_id == created_scenario.uuid
          assert put_event.resource_uuid == f'test/{created_scenario.uuid}'
          assert put_event.snapshot().uuid == created_scenario.uuid
          assert created_scenario.requests.count() == 2

          record_result = runner.invoke(record, ['--scenario-key', created_scenario.key(), DETERMINISTIC_GET_REQUEST_URL])
          assert record_result.exit_code == 0

          return created_scenario.requests.last()

        @pytest.fixture(scope='class')
        @classmethod
        def apply_result(cls, runner: CliRunner, created_scenario: Scenario):
          created_scenario = Scenario.find(created_scenario.id)
          assert created_scenario.requests_count == 3
          apply_result = runner.invoke(snapshot, ['apply'])

          return apply_result

        def test_it_merges_scenario(self, created_scenario: Scenario, apply_result):
          assert apply_result.exit_code == 0

          created_scenario = Scenario.find(created_scenario.id)
          assert created_scenario.requests_count == 2

        def test_it_maintains_requests(self, created_scenario: Scenario, created_scenario_requests: List[Request]):
          created_scenario = Scenario.find(created_scenario.id)
          assert len(created_scenario.requests) == 2

          requests = created_scenario.requests

          assert_orm_request_equivalent(requests[0], created_scenario_requests[0])
          assert_orm_request_equivalent(requests[1], created_scenario_requests[1])

      class TestWhenRequestsDeleted():
        '''
        1. Create scenario
        2. Add 2 requests to it
        3. Snapshot
        4. Delete last request added
        5. Snapshot
        6. Re-create last request
        7. Apply
        8. Expect scenario to have 1 request
        '''

        @pytest.fixture(scope='class')
        @classmethod
        def created_scenario(cls, runner: CliRunner):
          create_result = runner.invoke(scenario, ['create', 'test'])
          assert create_result.exit_code == 0
          return Scenario.last()

        @pytest.fixture(scope='class', autouse=True)
        @classmethod
        def created_scenario_requests(cls, runner: CliRunner, created_scenario: Scenario):
          record_result = runner.invoke(record, ['--scenario-key', created_scenario.key(), DETERMINISTIC_GET_REQUEST_URL])
          assert record_result.exit_code == 0

          record_result = runner.invoke(record, ['--scenario-key', created_scenario.key(), NON_DETERMINISTIC_GET_REQUEST_URL])
          assert record_result.exit_code == 0

          return created_scenario.requests

        @pytest.fixture(scope='class', autouse=True)
        @classmethod
        def delete_event(cls, runner: CliRunner, created_scenario: Scenario):
          snapshot_result = runner.invoke(scenario, ['snapshot', 'create', created_scenario.key()])
          assert snapshot_result.exit_code == 0

          last_request = created_scenario.requests.last()
          last_request.delete()

          snapshot_result = runner.invoke(scenario, ['snapshot', 'create', created_scenario.key()])
          assert snapshot_result.exit_code == 0

          # Re-create the request
          Request.create(**last_request.attributes_to_dict())

          log = Log()
          events = log.events
          return events[len(events) - 1]

        @pytest.fixture(scope='class')
        @classmethod
        def apply_result(cls, runner: CliRunner, created_scenario: Scenario):
          created_scenario = Scenario.find(created_scenario.id)
          apply_result = runner.invoke(snapshot, ['apply'])

          return apply_result

        def test_it_merges_scenario(self, created_scenario: Scenario, apply_result):
          assert apply_result.exit_code == 0

          created_scenario = Scenario.find(created_scenario.id)
          assert created_scenario.requests_count == 1

        def test_it_maintains_requests(self, created_scenario: Scenario, created_scenario_requests: List[Request]):
          created_scenario = Scenario.find(created_scenario.id)
          requests = created_scenario.requests

          assert_orm_request_equivalent(requests[0], created_scenario_requests[0])

        def test_it_removes_request_snapshot(self, delete_event: LogEvent):
          scenario_snapshot = ScenarioSnapshot.create(delete_event.resource_id)
          assert len(scenario_snapshot.requests) == 1

      class TestWhenMergingRequests():
        '''
        1. Create 2 requests with event id A and B respectively
        2. Snapshot
        3. Apply snapshots so that log VERSION is [A, B]
        4. Remove A from VERSION, expect VERSION is [B]
        5. Apply snapshots
        6. Expect log VERSION is again [A, B]
        '''

        @pytest.fixture(scope='class')
        @classmethod
        def recorded_request_one(cls, runner: CliRunner):
          record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
          assert record_result.exit_code == 0
          return Request.last()

        @pytest.fixture(scope='class')
        @classmethod
        def recorded_request_two(cls, runner: CliRunner):
          record_result = runner.invoke(record, [NON_DETERMINISTIC_GET_REQUEST_URL])
          assert record_result.exit_code == 0
          return Request.last()

        @pytest.fixture(scope='class', autouse=True)
        @classmethod
        def snapshot_one_result(cls, runner: CliRunner, recorded_request_one: Request):
          snapshot_result = runner.invoke(request, ['snapshot', 'create', recorded_request_one.key()])
          assert snapshot_result.exit_code == 0
          return snapshot_result

        @pytest.fixture(scope='class', autouse=True)
        @classmethod
        def snapshot_two_result(cls, runner: CliRunner, recorded_request_two: Request):
          snapshot_result = runner.invoke(request, ['snapshot', 'create', recorded_request_two.key()])
          assert snapshot_result.exit_code == 0
          return snapshot_result

        @pytest.fixture()
        def apply_result(self, runner: CliRunner):
          apply_result = runner.invoke(snapshot, ['apply'])
          assert apply_result.exit_code == 0
          return apply_result

        def test_it_applies_older_snapshot(self, runner: CliRunner, apply_result):
          log = Log()
          expected_version = log.version

          events = log.events
          log.version = events[1].uuid
          assert log.version != expected_version

          apply_result = runner.invoke(snapshot, ['apply'])
          assert apply_result.exit_code == 0

          assert log.version == expected_version

    class TestWhenMalformedScenarioMetadata():

      @pytest.fixture(scope='class')
      @classmethod
      def created_scenario(cls, runner: CliRunner):
          create_result = runner.invoke(scenario, ['create', 'test'])
          assert create_result.exit_code == 0
          return Scenario.last()

      @pytest.fixture(scope='class', autouse=True)
      @classmethod
      def put_event(cls, runner: CliRunner, created_scenario: Scenario):
        snapshot_result = runner.invoke(scenario, ['snapshot', 'create', created_scenario.key()])
        assert snapshot_result.exit_code == 0

        log = Log()
        events = log.events
        event = events[len(events) - 1]
        metadata_path = event.snapshot().metadata_path
        with open(metadata_path, 'w') as fp:
          fp.write('junk')

        return event

      @pytest.fixture(scope='class', autouse=True)
      @classmethod
      def removed_scenario(cls, created_scenario: Scenario):
        created_scenario.delete()
        assert Scenario.find(created_scenario.id) == None

      def test_skips_scenario_with_malformed_metadata(self, runner: CliRunner, created_scenario: Scenario):
        # v2 YAML must include uuid; corrupt metadata cannot recover identity from name-only history
        apply_result = runner.invoke(snapshot, ['apply'])
        assert apply_result.exit_code == 0

        recreated_scenario = Scenario.find_by(uuid=created_scenario.uuid)
        assert recreated_scenario == None

    class TestWhenMissingScenarioMetadata():

      @pytest.fixture(scope='class')
      @classmethod
      def created_scenario(cls, runner: CliRunner):
          create_result = runner.invoke(scenario, ['create', 'test'])
          assert create_result.exit_code == 0
          return Scenario.last()

      @pytest.fixture(scope='class', autouse=True)
      @classmethod
      def put_event(cls, runner: CliRunner, created_scenario: Scenario):
        snapshot_result = runner.invoke(scenario, ['snapshot', 'create', created_scenario.key()])
        assert snapshot_result.exit_code == 0

        log = Log()
        events = log.events
        event = events[len(events) - 1]
        metadata_path = event.snapshot().metadata_path
        os.remove(metadata_path)

        return event

      @pytest.fixture(scope='class', autouse=True)
      @classmethod
      def removed_scenario(cls, created_scenario: Scenario):
        created_scenario.delete()
        assert Scenario.find(created_scenario.id) == None

      def test_skips_scenario(self, runner: CliRunner, created_scenario: Scenario):
        apply_result = runner.invoke(snapshot, ['apply'])
        assert apply_result.exit_code == 0

        recreated_scenario = Scenario.find_by(uuid=created_scenario.uuid)
        assert recreated_scenario == None
  
    class TestWhenMalformedRequest():

      @pytest.fixture(scope='class')
      @classmethod
      def recorded_request(cls, runner: CliRunner):
        record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
        assert record_result.exit_code == 0
        return Request.last()

      @pytest.fixture(autouse=True, scope='class')
      @classmethod
      def put_event(cls, runner: CliRunner, recorded_request: Request):
        snapshot_result = runner.invoke(request, ['snapshot', 'create', recorded_request.key()])
        assert snapshot_result.exit_code == 0

        log = Log()
        events = log.events
        event = events[len(events) - 1]

        with open(event.snapshot().path, 'w') as fp:
          fp.write('junk')

        return event

      @pytest.fixture(scope='class', autouse=True)
      @classmethod
      def removed_request(cls, recorded_request: Request):
        recorded_request.delete()
        assert Request.find(recorded_request.id) == None

      def test_it_creates_request(self, runner: CliRunner, recorded_request: Request):
        apply_result = runner.invoke(snapshot, ['apply'])
        assert apply_result.exit_code == 1
        assert 'Malformed request snapshot' in apply_result.output
        assert Request.find_by(uuid=recorded_request.uuid) == None

      def test_idempotent(self, runner: CliRunner, recorded_request: Request, put_event: LogEvent):
        apply_result = runner.invoke(snapshot, ['apply', put_event.uuid])
        assert apply_result.exit_code == 1
        assert 'Malformed request snapshot' in apply_result.output
        assert Request.find_by(uuid=recorded_request.uuid) == None

    class TestWhenMalformedScenarioRequest():

      @pytest.fixture(scope='class')
      @classmethod
      def created_scenario(cls, runner: CliRunner):
          create_result = runner.invoke(scenario, ['create', 'test'])
          assert create_result.exit_code == 0
          return Scenario.last()

      @pytest.fixture(scope='class', autouse=True)
      @classmethod
      def created_scenario_requests(cls, runner: CliRunner, created_scenario: Scenario):
          record_result = runner.invoke(record, ['--scenario-key', created_scenario.key(), DETERMINISTIC_GET_REQUEST_URL])
          assert record_result.exit_code == 0

          return created_scenario.requests

      @pytest.fixture(scope='class', autouse=True)
      @classmethod
      def put_event(cls, runner: CliRunner, created_scenario: Scenario):
        snapshot_result = runner.invoke(scenario, ['snapshot', 'create', created_scenario.key()])
        assert snapshot_result.exit_code == 0

        log = Log()
        events = log.events
        event = events[len(events) - 1]
        event.snapshot().iter_request_snapshots(lambda snapshot: write_junk(snapshot.path))

        return event

      @pytest.fixture(scope='class', autouse=True)
      @classmethod
      def removed_scenario(cls, created_scenario: Scenario):
        created_scenario.delete()
        assert Scenario.find(created_scenario.id) == None

      def test_skips_scenario(self, runner: CliRunner, created_scenario: Scenario):
        apply_result = runner.invoke(snapshot, ['apply'])
        assert apply_result.exit_code == 1
        assert 'Malformed request snapshot' in apply_result.output

        recreated_scenario = Scenario.find_by(uuid=created_scenario.uuid)
        assert recreated_scenario

        assert len(recreated_scenario.requests) == 0

      def test_idempotent(self, runner: CliRunner, created_scenario: Scenario, put_event: LogEvent):
        apply_result = runner.invoke(snapshot, ['apply', put_event.uuid])
        assert apply_result.exit_code == 1
        assert 'Malformed request snapshot' in apply_result.output

        recreated_scenario = Scenario.find_by(uuid=created_scenario.uuid)
        assert recreated_scenario

        assert len(recreated_scenario.requests) == 0

    class TestWhenDeletingRequestWhileReferenced():

      class TestWhenRemoveScenarioRequest():
        '''
        1. Create scenario
        2. Add 2 requests to it
        3. Snapshot scenario
        4. Snapshot second request with action DELETE_ACTION
        5. Apply
        6. Expect scenario to have 1 request
        '''

        @pytest.fixture(scope='class')
        @classmethod
        def created_scenario(cls, runner: CliRunner):
          create_result = runner.invoke(scenario, ['create', 'test'])
          assert create_result.exit_code == 0
          return Scenario.last()

        @pytest.fixture(scope='class', autouse=True)
        @classmethod
        def created_scenario_requests(cls, runner: CliRunner, created_scenario: Scenario):
          record_result = runner.invoke(record, ['--scenario-key', created_scenario.key(), DETERMINISTIC_GET_REQUEST_URL])
          assert record_result.exit_code == 0

          record_result = runner.invoke(record, ['--scenario-key', created_scenario.key(), NON_DETERMINISTIC_GET_REQUEST_URL])
          assert record_result.exit_code == 0

          return created_scenario.requests

        @pytest.fixture(scope='class', autouse=True)
        @classmethod
        def delete_event(cls, runner: CliRunner, created_scenario: Scenario, created_scenario_requests: List[Request]):
          snapshot_result = runner.invoke(scenario, ['snapshot', 'create', created_scenario.key()])
          assert snapshot_result.exit_code == 0

          time.sleep(0.5) # So events do not have the same uuid

          created_request = created_scenario_requests[1]
          snapshot_result = runner.invoke(request, ['snapshot', 'create', created_request.key(), '--action', DELETE_ACTION])
          assert snapshot_result.exit_code == 0

          log = Log()
          events = log.events
          return events[len(events) - 1]

        @pytest.fixture(scope='class')
        @classmethod
        def apply_result(cls, runner: CliRunner, created_scenario: Scenario):
          created_scenario = Scenario.find(created_scenario.id)
          assert created_scenario.requests_count == 2
          apply_result = runner.invoke(snapshot, ['apply'])

          return apply_result

        def test_it_updates_scenario(self, created_scenario: Scenario, apply_result):
          assert apply_result.exit_code == 0

          created_scenario = Scenario.find(created_scenario.id)
          assert created_scenario.requests_count == 1

        def test_it_maintains_requests(self, created_scenario: Scenario, created_scenario_requests: List[Request]):
          created_scenario = Scenario.find(created_scenario.id)
          assert len(created_scenario.requests) == 1

          requests = created_scenario.requests

          assert_orm_request_equivalent(requests[0], created_scenario_requests[0])
      
      class TestWhenMovingScenarioRequest():
        '''
        1. Create scenario one and scenario two
        2. Add 1 request to scenario one
        3. Snapshot scenario one
        4. Move scenario one request to scenario two
        5. Snapshot scenario two
        5. Apply
        6. Expect scenario one to have 0 requests
        7. Expect scenario two to have 1 request
        '''

        @pytest.fixture(scope='class')
        @classmethod
        def created_scenario_one(cls, runner: CliRunner):
          create_result = runner.invoke(scenario, ['create', 'test1'])
          assert create_result.exit_code == 0
          return Scenario.last()

        @pytest.fixture(scope='class')
        @classmethod
        def created_scenario_two(cls, runner: CliRunner):
          create_result = runner.invoke(scenario, ['create', 'test2'])
          assert create_result.exit_code == 0
          return Scenario.last()

        @pytest.fixture(scope='class', autouse=True)
        @classmethod
        def created_scenario_request(cls, runner: CliRunner, created_scenario_one: Scenario):
          record_result = runner.invoke(record, ['--scenario-key', created_scenario_one.key(), DETERMINISTIC_GET_REQUEST_URL])
          assert record_result.exit_code == 0

          return created_scenario_one.requests[0]

        @pytest.fixture(scope='class', autouse=True)
        @classmethod
        def put_event_one(cls, runner: CliRunner, created_scenario_one: Scenario, created_scenario_request: Request):
          snapshot_result = runner.invoke(scenario, ['snapshot', 'create', created_scenario_one.key()])
          assert snapshot_result.exit_code == 0

          log = Log()
          events = log.events
          return events[len(events) - 1]

        @pytest.fixture(scope='class', autouse=True)
        @classmethod
        def put_event_two(cls, runner: CliRunner, created_scenario_two: Scenario, created_scenario_request: Request):
          created_scenario_request.update(scenario_id=created_scenario_two.id)

          snapshot_result = runner.invoke(scenario, ['snapshot', 'create', created_scenario_two.key()])
          assert snapshot_result.exit_code == 0

          log = Log()
          events = log.events
          return events[len(events) - 1]

        @pytest.fixture(scope='class')
        @classmethod
        def apply_result(cls, runner: CliRunner):
          apply_result = runner.invoke(snapshot, ['apply'])

          return apply_result

        def test_it_removes_request_from_scenario_one(self, created_scenario_one: Scenario, apply_result):
          assert apply_result.exit_code == 0

          created_scenario_one = Scenario.find(created_scenario_one.id)
          assert created_scenario_one.requests_count == 0

        def test_it_adds_request_to_scenario_two(self, created_scenario_two: Scenario, apply_result):
          assert apply_result.exit_code == 0

          created_scenario_two = Scenario.find(created_scenario_two.id)
          assert created_scenario_two.requests_count == 1

        def test_it_maintains_requests(self, created_scenario_two: Scenario, created_scenario_request):
          created_scenario_two = Scenario.find(created_scenario_two.id)
          assert len(created_scenario_two.requests) == 1

          requests = created_scenario_two.requests

          assert_orm_request_equivalent(requests[0], created_scenario_request)
    
    class TestApply():

      class TestWhenNoApply():
        '''
        1. Create scenario
        2. Add 2 requests to it
        3. Snapshot scenario
        4. Apply scenario
        5. Snapshot second request with action DELETE_ACTION
        6. Prune
        7. Apply
        8. Expect scenario to have 1 request, because scenario depends on the request, should not be able to prune
        '''

        @pytest.fixture(scope='class')
        @classmethod
        def created_scenario(cls, runner: CliRunner):
          create_result = runner.invoke(scenario, ['create', 'test'])
          assert create_result.exit_code == 0
          return Scenario.last()

        @pytest.fixture(scope='class', autouse=True)
        @classmethod
        def created_scenario_requests(cls, runner: CliRunner, created_scenario: Scenario):
          record_result = runner.invoke(record, ['--scenario-key', created_scenario.key(), DETERMINISTIC_GET_REQUEST_URL])
          assert record_result.exit_code == 0

          record_result = runner.invoke(record, ['--scenario-key', created_scenario.key(), NON_DETERMINISTIC_GET_REQUEST_URL])
          assert record_result.exit_code == 0

          return created_scenario.requests

        @pytest.fixture(scope='class', autouse=True)
        @classmethod
        def snapshots(cls, runner: CliRunner, created_scenario: Scenario, created_scenario_requests: List[Request]):
          snapshot_result = runner.invoke(scenario, ['snapshot', 'create', created_scenario.key()])
          assert snapshot_result.exit_code == 0

          created_request = created_scenario_requests[1]
          snapshot_result = runner.invoke(request, ['snapshot', 'create', created_request.key(), '--action', DELETE_ACTION])
          assert snapshot_result.exit_code == 0

        def test_events(self):
          log = Log()

          events = log.events
          assert len(events) == 2

        def test_collapsed_events(self):
          log = Log()

          collapsed_events = log.collapse(log.events)
          assert len(collapsed_events) == 2

        def test_unprocessed_events(self):
          log = Log()

          unprocessed_events = log.unprocessed_events
          assert len(unprocessed_events) == 2

      class TestWhenRemoveScenarioRequest():
        '''
        1. Create scenario
        2. Add 2 requests to it
        3. Snapshot scenario
        4. Apply scenario
        5. Snapshot second request with action DELETE_ACTION
        6. Prune
        7. Apply
        8. Expect scenario to have 1 request, because scenario depends on the request, should not be able to prune
        '''

        @pytest.fixture(scope='class')
        @classmethod
        def created_scenario(cls, runner: CliRunner):
          create_result = runner.invoke(scenario, ['create', 'test'])
          assert create_result.exit_code == 0
          return Scenario.last()

        @pytest.fixture(scope='class', autouse=True)
        @classmethod
        def created_scenario_requests(cls, runner: CliRunner, created_scenario: Scenario):
          record_result = runner.invoke(record, ['--scenario-key', created_scenario.key(), DETERMINISTIC_GET_REQUEST_URL])
          assert record_result.exit_code == 0

          record_result = runner.invoke(record, ['--scenario-key', created_scenario.key(), NON_DETERMINISTIC_GET_REQUEST_URL])
          assert record_result.exit_code == 0

          return created_scenario.requests

        @pytest.fixture(scope='class', autouse=True)
        @classmethod
        def apply_result(cls, runner: CliRunner, created_scenario: Scenario, created_scenario_requests: List[Request]):
          snapshot_result = runner.invoke(scenario, ['snapshot', 'create', created_scenario.key()])
          assert snapshot_result.exit_code == 0

          created_scenario = Scenario.find(created_scenario.id)
          assert created_scenario.requests_count == 2
          apply_result = runner.invoke(snapshot, ['apply'])
          assert apply_result.exit_code == 0

          created_request = created_scenario_requests[1]
          snapshot_result = runner.invoke(request, ['snapshot', 'create', created_request.key(), '--action', DELETE_ACTION])
          assert snapshot_result.exit_code == 0

          return apply_result

        def test_events(self):
          log = Log()

          events = log.events
          assert len(events) == 2

        def test_collapsed_events(self):
          log = Log()

          collapsed_events = log.collapse(log.events)
          assert len(collapsed_events) == 2

        def test_unprocessed_events(self):
          log = Log()

          unprocessed_events = log.unprocessed_events
          assert len(unprocessed_events) == 1
          assert unprocessed_events[0].action == DELETE_ACTION

    class TestWhenApplyingSnapshotByUuid():
      '''
      1. Record two requests and snapshot each, leaving two pending events
      2. Apply the first event by uuid
      3. Expect only the second event to remain pending
      '''

      @pytest.fixture(scope='class')
      @classmethod
      def log(cls):
        return Log()

      @pytest.fixture(scope='class', autouse=True)
      @classmethod
      def pending_events(cls, runner: CliRunner):
        unprocessed_events = create_pending_request_snapshots(runner, [DETERMINISTIC_GET_REQUEST_URL, NON_DETERMINISTIC_GET_REQUEST_URL])
        assert len(unprocessed_events) == 2
        return unprocessed_events

      def test_it_marks_applied_event_processed(self, runner: CliRunner, log: Log, pending_events: List[LogEvent]):
        apply_result = runner.invoke(snapshot, ['apply', pending_events[0].uuid])
        assert apply_result.exit_code == 0

        unprocessed_uuids = [event.uuid for event in log.unprocessed_events]
        assert pending_events[0].uuid not in unprocessed_uuids
        assert unprocessed_uuids == [pending_events[1].uuid]

    class TestWhenApplyingSnapshotByUuidFails():
      '''
      1. Record a request and snapshot it, then corrupt the snapshot file
      2. Apply the event by uuid
      3. Expect the apply to fail and the event to remain pending
      '''

      @pytest.fixture(scope='class', autouse=True)
      @classmethod
      def pending_event(cls, runner: CliRunner):
        unprocessed_events = create_pending_request_snapshots(runner, [DETERMINISTIC_GET_REQUEST_URL])
        assert len(unprocessed_events) == 1

        event = unprocessed_events[0]
        write_junk(event.snapshot().path)
        return event

      def test_it_leaves_event_pending(self, runner: CliRunner, pending_event: LogEvent):
        apply_result = runner.invoke(snapshot, ['apply', pending_event.uuid])
        assert apply_result.exit_code == 1

        unprocessed_uuids = [event.uuid for event in Log().unprocessed_events]
        assert unprocessed_uuids == [pending_event.uuid]

    class TestWhenApplyingSnapshotByUuidThenAll():
      '''
      1. Create two pending snapshots
      2. Apply the first by uuid
      3. Apply all
      4. Expect nothing to remain pending
      '''

      @pytest.fixture(scope='class', autouse=True)
      @classmethod
      def pending_events(cls, runner: CliRunner):
        unprocessed_events = create_pending_request_snapshots(runner, [DETERMINISTIC_GET_REQUEST_URL, NON_DETERMINISTIC_GET_REQUEST_URL])
        assert len(unprocessed_events) == 2
        return unprocessed_events

      def test_it_clears_pending(self, runner: CliRunner, pending_events: List[LogEvent]):
        apply_result = runner.invoke(snapshot, ['apply', pending_events[0].uuid])
        assert apply_result.exit_code == 0

        apply_result = runner.invoke(snapshot, ['apply'])
        assert apply_result.exit_code == 0

        assert Log().unprocessed_events == []

    class TestWhenSoftDeletingRequest():
      '''
      Apply DELETE without --force soft-deletes the ORM row (is_deleted=True).
      '''

      @pytest.fixture(scope='class', autouse=True)
      @classmethod
      def recorded_request(cls, runner: CliRunner):
        pending = create_pending_request_snapshots(runner, [DETERMINISTIC_GET_REQUEST_URL])
        assert len(pending) == 1

        apply_result = runner.invoke(snapshot, ['apply', pending[0].uuid])
        assert apply_result.exit_code == 0

        recorded = Request.find_by(uuid=pending[0].resource_id)
        assert recorded is not None

        time.sleep(0.5)
        delete_result = runner.invoke(
          request,
          ['snapshot', 'create', '--action', DELETE_ACTION, recorded.key()],
        )
        assert delete_result.exit_code == 0
        return recorded

      def test_it_soft_deletes(self, runner: CliRunner, recorded_request: Request):
        delete_event = Log().unprocessed_events[-1]
        assert delete_event.action == DELETE_ACTION

        apply_result = runner.invoke(snapshot, ['apply', delete_event.uuid])
        assert apply_result.exit_code == 0

        soft_deleted = Request.find_by(uuid=recorded_request.uuid)
        assert soft_deleted is not None
        assert bool(soft_deleted.is_deleted) is True

    class TestWhenSoftDeleteThenPutUndeletes():
      '''
      After a soft-deleted request, applying a PUT clears is_deleted.
      '''

      @pytest.fixture(scope='class', autouse=True)
      @classmethod
      def recorded_request(cls, runner: CliRunner):
        pending = create_pending_request_snapshots(runner, [DETERMINISTIC_GET_REQUEST_URL])
        recorded = Request.find_by(uuid=pending[0].resource_id)
        recorded.update({'is_deleted': True})
        assert bool(Request.find_by(uuid=recorded.uuid).is_deleted) is True
        return recorded

      def test_it_undeletes(self, runner: CliRunner, recorded_request: Request):
        put_event = Log().unprocessed_events[-1]
        apply_result = runner.invoke(snapshot, ['apply', put_event.uuid])
        assert apply_result.exit_code == 0

        restored = Request.find_by(uuid=recorded_request.uuid)
        assert restored is not None
        assert bool(restored.is_deleted) is False

    class TestWhenMissingRequestSnapshotSkips():
      '''
      Missing request snapshot file returns 301 (skip). apply all continues and
      advances VERSION past the skip so later events still apply.
      '''

      @pytest.fixture(scope='class', autouse=True)
      @classmethod
      def pending_events(cls, runner: CliRunner):
        pending = create_pending_request_snapshots(
          runner,
          [DETERMINISTIC_GET_REQUEST_URL, NON_DETERMINISTIC_GET_REQUEST_URL],
        )
        assert len(pending) == 2

        missing_path = pending[0].snapshot().path
        assert os.path.isfile(missing_path)
        os.remove(missing_path)

        for event in pending:
          orm_request = Request.find_by(uuid=event.resource_id)
          if orm_request:
            orm_request.delete()

        return pending

      def test_it_skips_and_applies_later_events(self, runner: CliRunner, pending_events: List[LogEvent]):
        apply_result = runner.invoke(snapshot, ['apply'])
        assert apply_result.exit_code == 0

        assert Request.find_by(uuid=pending_events[0].resource_id) is None
        assert Request.find_by(uuid=pending_events[1].resource_id) is not None
        assert Log().unprocessed_events == []

    class TestWhenPartialApplyFailureAdvancesVersion():
      '''
      On mid-batch failure, VERSION advances through the last successful event
      and remaining events stay pending.

      Uses a request PUT (success) followed by a scenario PUT whose nested
      request file is missing (clean 400). Junk .http files raise during v2
      reconstitute and abort apply before VERSION can advance.
      '''

      @pytest.fixture(scope='class', autouse=True)
      @classmethod
      def pending_events(cls, runner: CliRunner):
        log = Log()
        log.version = log.generate_version(log.uuids())

        record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
        assert record_result.exit_code == 0
        recorded_request = Request.last()
        snapshot_result = runner.invoke(request, ['snapshot', 'create', recorded_request.key()])
        assert snapshot_result.exit_code == 0

        time.sleep(0.5)

        create_result = runner.invoke(scenario, ['create', 'partial-fail-scenario'])
        assert create_result.exit_code == 0
        created_scenario = Scenario.last()
        record_result = runner.invoke(
          record,
          ['--scenario-key', created_scenario.key(), NON_DETERMINISTIC_GET_REQUEST_URL],
        )
        assert record_result.exit_code == 0
        snapshot_result = runner.invoke(scenario, ['snapshot', 'create', created_scenario.key()])
        assert snapshot_result.exit_code == 0

        pending = Log().unprocessed_events
        assert len(pending) == 2

        nested = pending[1].snapshot().request_snapshots[0]
        os.remove(nested.path)

        recorded_request.delete()
        scenario_requests = list(created_scenario.requests)
        created_scenario.delete()
        for req in scenario_requests:
          req.delete()

        return pending

      def test_it_advances_version_to_last_success(self, runner: CliRunner, pending_events: List[LogEvent]):
        apply_result = runner.invoke(snapshot, ['apply'])
        assert apply_result.exit_code == 1

        assert Request.find_by(uuid=pending_events[0].resource_id) is not None

        unprocessed = Log().unprocessed_events
        assert [event.uuid for event in unprocessed] == [pending_events[1].uuid]
        assert pending_events[0].uuid in Log().version

    class TestWhenMissingScenarioRequestFile():
      '''
      Scenario PUT with a missing nested request file fails apply (400).
      '''

      @pytest.fixture(scope='class', autouse=True)
      @classmethod
      def put_event(cls, runner: CliRunner):
        log = Log()
        log.version = log.generate_version(log.uuids())

        create_result = runner.invoke(scenario, ['create', 'missing-request-file'])
        assert create_result.exit_code == 0
        created_scenario = Scenario.last()

        record_result = runner.invoke(
          record,
          ['--scenario-key', created_scenario.key(), DETERMINISTIC_GET_REQUEST_URL],
        )
        assert record_result.exit_code == 0

        snapshot_result = runner.invoke(scenario, ['snapshot', 'create', created_scenario.key()])
        assert snapshot_result.exit_code == 0

        event = Log().unprocessed_events[-1]
        request_snap = event.snapshot().request_snapshots[0]
        os.remove(request_snap.path)

        requests = list(created_scenario.requests)
        created_scenario.delete()
        for req in requests:
          req.delete()

        return event

      def test_it_fails_apply(self, runner: CliRunner, put_event: LogEvent):
        apply_result = runner.invoke(snapshot, ['apply'])
        assert apply_result.exit_code == 1

        recreated = Scenario.find_by(uuid=put_event.snapshot().uuid)
        assert recreated is not None
        assert len(recreated.requests) == 0

    class TestWhenScenarioNameExistsAsSoftDeleted():
      '''
      Creating from snapshot hits 409 against a soft-deleted same-name row;
      apply remaps that row to the snapshot UUID and undeletes it.
      '''

      @pytest.fixture(scope='class', autouse=True)
      @classmethod
      def source_scenario(cls, runner: CliRunner):
        log = Log()
        log.version = log.generate_version(log.uuids())

        create_result = runner.invoke(scenario, ['create', 'soft-deleted-name'])
        assert create_result.exit_code == 0
        source = Scenario.last()

        snapshot_result = runner.invoke(scenario, ['snapshot', 'create', source.key()])
        assert snapshot_result.exit_code == 0

        # Replace ORM row with a soft-deleted scenario of the same name but different uuid
        source.delete()
        create_result = runner.invoke(scenario, ['create', 'soft-deleted-name'])
        assert create_result.exit_code == 0
        conflicting = Scenario.last()
        conflicting.update({'is_deleted': True})
        assert bool(Scenario.find(conflicting.id).is_deleted) is True

        return source

      def test_it_remaps_soft_deleted_scenario(self, runner: CliRunner, source_scenario: Scenario):
        apply_result = runner.invoke(snapshot, ['apply'])
        assert apply_result.exit_code == 0

        remapped = Scenario.find_by(uuid=source_scenario.uuid)
        assert remapped is not None
        assert remapped.name == source_scenario.name
        assert bool(remapped.is_deleted) is False

    class TestWhenApplyingUnknownUuid():
      def test_it_exits_nonzero(self, runner: CliRunner):
        apply_result = runner.invoke(snapshot, ['apply', '00000000-0000-0000-0000-000000000000'])
        assert apply_result.exit_code == 1

    class TestWhenHistoryLineMalformed():
      @pytest.fixture(scope='class', autouse=True)
      @classmethod
      def malformed_history(cls, runner: CliRunner):
        log = Log()
        log.version = log.generate_version(log.uuids())
        # Append a truncated history line under snapshots/history
        history_dir = log.history_dir_path
        os.makedirs(history_dir, exist_ok=True)
        path = os.path.join(history_dir, 'malformed-history')
        with open(path, 'a') as fp:
          fp.write('not-enough-fields\n')

      def test_it_reports_error_to_user(self, runner: CliRunner):
        apply_result = runner.invoke(snapshot, ['apply'])
        assert apply_result.exit_code == 1
        assert 'Malformed snapshot history line' in apply_result.output
        assert 'not-enough-fields' in apply_result.output

    class TestLocking():
      def test_concurrent_apply_commands_timeout(self, runner: CliRunner):
        """Test that concurrent snapshot apply commands properly timeout"""
        from filelock import FileLock
        
        data_dir: DataDir = DataDir.instance()
        lock_file_path = os.path.join(data_dir.tmp_dir_path, '.snapshot-apply.lock')
        
        # Acquire lock in a separate thread to simulate a running snapshot apply
        lock_acquired = threading.Event()
        lock_released = threading.Event()
        
        def hold_lock():
          lock = FileLock(lock_file_path)
          with lock:
            lock_acquired.set()
            # Hold the lock for a short time
            time.sleep(0.5)
            lock_released.set()
        
        # Start thread that holds the lock
        lock_thread = threading.Thread(target=hold_lock)
        lock_thread.start()
        
        # Wait for lock to be acquired
        lock_acquired.wait(timeout=2)
        
        try:
          # Try to run snapshot apply while lock is held (with short timeout)
          result = runner.invoke(snapshot, ['apply', '--lock-timeout', '1'])
          
          # Should timeout and exit with error (exit code 1 indicates timeout)
          assert result.exit_code == 1
        finally:
          # Wait for lock to be released
          lock_released.wait(timeout=2)
          lock_thread.join(timeout=2)