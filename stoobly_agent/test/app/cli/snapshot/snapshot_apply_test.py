import os
import pdb
import pytest
import time

from click.testing import CliRunner
from typing import List

from stoobly_agent.app.cli.request_cli import request
from stoobly_agent.app.cli.scenario_cli import scenario
from stoobly_agent.app.cli.snapshot_cli import snapshot
from stoobly_agent.app.models.factories.resource.local_db.helpers.log import Log
from stoobly_agent.app.models.factories.resource.local_db.helpers.log_event import DELETE_ACTION, LogEvent
from stoobly_agent.app.models.factories.resource.local_db.helpers.scenario_snapshot import ScenarioSnapshot
from stoobly_agent.cli import record
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.lib.orm.scenario import Scenario
from stoobly_agent.test.test_helper import assert_orm_request_equivalent, DETERMINISTIC_GET_REQUEST_URL, NON_DETERMINISTIC_GET_REQUEST_URL, reset

def write_junk(path: str):
  with open(path, 'w') as fp:
    fp.write('junk')

@pytest.fixture(scope='module')
def runner():
    return CliRunner()

class TestApply():
    @pytest.fixture(scope='class', autouse=True)
    def settings(self):
      return reset()

    class TestWhenDeletingRequest():

      @pytest.fixture(scope='class')
      def log(self):
        return Log()

      @pytest.fixture(scope='class')
      def recorded_request(self, runner: CliRunner):
        record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
        assert record_result.exit_code == 0
        return Request.last()

      @pytest.fixture(autouse=True, scope='class')
      def events(self, runner: CliRunner, recorded_request: Request, log: Log):
        snapshot_result = runner.invoke(request, ['snapshot', recorded_request.key()])
        assert snapshot_result.exit_code == 0

        events = log.events
        event: LogEvent = events[len(events) - 1]
        log.version = event.uuid

        time.sleep(1)

        snapshot_result = runner.invoke(request, ['snapshot', '--action', DELETE_ACTION, recorded_request.key()])
        assert snapshot_result.exit_code == 0

        return log.events

      @pytest.fixture(scope='class')
      def delete_event(self, events: List[LogEvent]):
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
        snapshot_result = runner.invoke(request, ['snapshot', recorded_request.key()])
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

    class TestWhenDeletingScenario():

      @pytest.fixture(scope='class')
      def log(self):
        return Log()

      @pytest.fixture(scope='class')
      def created_scenario(self, runner: CliRunner):
          create_result = runner.invoke(scenario, ['create', 'test'])
          assert create_result.exit_code == 0
          return Scenario.last()

      @pytest.fixture(autouse=True, scope='class')
      def events(self, runner: CliRunner, created_scenario: Scenario, log: Log):
        snapshot_result = runner.invoke(scenario, ['snapshot',  created_scenario.key()])
        assert snapshot_result.exit_code == 0

        events = log.events
        event: LogEvent = events[len(events) - 1]
        log.version = event.uuid

        time.sleep(1)

        snapshot_result = runner.invoke(scenario, ['snapshot', '--action', DELETE_ACTION, created_scenario.key()])
        assert snapshot_result.exit_code == 0

        return log.events

      @pytest.fixture(scope='class')
      def delete_event(self, events):
        return events[1]

      def test_it_deletes(self, runner: CliRunner, created_scenario: Scenario, delete_event: LogEvent):
        snapshot_result = runner.invoke(snapshot, ['apply', '--force', delete_event.uuid])
        assert snapshot_result.exit_code == 0

        scenario = Scenario.find(created_scenario.id)

        assert scenario == None

    class TestWhenCreatingScenario():

      @pytest.fixture(scope='class')
      def created_scenario(self, runner: CliRunner):
          create_result = runner.invoke(scenario, ['create', 'test'])
          assert create_result.exit_code == 0
          return Scenario.last()

      @pytest.fixture(scope='class', autouse=True)
      def created_scenario_requests(self, runner: CliRunner, created_scenario: Scenario):
          record_result = runner.invoke(record, ['--scenario-key', created_scenario.key(), DETERMINISTIC_GET_REQUEST_URL])
          assert record_result.exit_code == 0

          record_result = runner.invoke(record, ['--scenario-key', created_scenario.key(), NON_DETERMINISTIC_GET_REQUEST_URL])
          assert record_result.exit_code == 0

          return created_scenario.requests

      @pytest.fixture(scope='class', autouse=True)
      def put_event(self, runner: CliRunner, created_scenario: Scenario):
        snapshot_result = runner.invoke(scenario, ['snapshot', created_scenario.key()])
        assert snapshot_result.exit_code == 0

        log = Log()
        events = log.events
        return events[len(events) - 1]

      @pytest.fixture(scope='class', autouse=True)
      def recreated_scenario(self, runner: CliRunner, created_scenario: Scenario):
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

    class TestWhenMergingScenario():

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
        def created_scenario(self, runner: CliRunner):
          create_result = runner.invoke(scenario, ['create', 'test'])
          assert create_result.exit_code == 0
          return Scenario.last()

        @pytest.fixture(scope='class', autouse=True)
        def created_scenario_requests(self, runner: CliRunner, created_scenario: Scenario):
          record_result = runner.invoke(record, ['--scenario-key', created_scenario.key(), DETERMINISTIC_GET_REQUEST_URL])
          assert record_result.exit_code == 0

          record_result = runner.invoke(record, ['--scenario-key', created_scenario.key(), NON_DETERMINISTIC_GET_REQUEST_URL])
          assert record_result.exit_code == 0

          return created_scenario.requests

        @pytest.fixture(scope='class', autouse=True)
        def put_event(self, runner: CliRunner, created_scenario: Scenario):
          snapshot_result = runner.invoke(scenario, ['snapshot', created_scenario.key()])
          assert snapshot_result.exit_code == 0

          log = Log()
          events = log.events
          return events[len(events) - 1]

        # This request was created after the snapshot
        # Later when we apply changes, we expect this request to not exist
        @pytest.fixture(scope='class', autouse=True)
        def new_scenario_request(self, runner: CliRunner, created_scenario: Scenario, put_event: LogEvent):
          assert created_scenario.uuid == put_event.resource_uuid
          assert created_scenario.requests.count() == 2

          record_result = runner.invoke(record, ['--scenario-key', created_scenario.key(), DETERMINISTIC_GET_REQUEST_URL])
          assert record_result.exit_code == 0

          return created_scenario.requests.last()

        @pytest.fixture(scope='class')
        def apply_result(self, runner: CliRunner, created_scenario: Scenario):
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
        def created_scenario(self, runner: CliRunner):
          create_result = runner.invoke(scenario, ['create', 'test'])
          assert create_result.exit_code == 0
          return Scenario.last()

        @pytest.fixture(scope='class', autouse=True)
        def created_scenario_requests(self, runner: CliRunner, created_scenario: Scenario):
          record_result = runner.invoke(record, ['--scenario-key', created_scenario.key(), DETERMINISTIC_GET_REQUEST_URL])
          assert record_result.exit_code == 0

          record_result = runner.invoke(record, ['--scenario-key', created_scenario.key(), NON_DETERMINISTIC_GET_REQUEST_URL])
          assert record_result.exit_code == 0

          return created_scenario.requests

        @pytest.fixture(scope='class', autouse=True)
        def delete_event(self, runner: CliRunner, created_scenario: Scenario):
          snapshot_result = runner.invoke(scenario, ['snapshot', created_scenario.key()])
          assert snapshot_result.exit_code == 0

          last_request = created_scenario.requests.last()
          last_request.delete()

          snapshot_result = runner.invoke(scenario, ['snapshot', created_scenario.key()])
          assert snapshot_result.exit_code == 0

          # Re-create the request
          Request.create(**last_request.attributes_to_dict())

          log = Log()
          events = log.events
          return events[len(events) - 1]

        @pytest.fixture(scope='class')
        def apply_result(self, runner: CliRunner, created_scenario: Scenario):
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
          scenario_snapshot = ScenarioSnapshot(delete_event.resource_uuid)
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
        def recorded_request_one(self, runner: CliRunner):
          record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
          assert record_result.exit_code == 0
          return Request.last()

        @pytest.fixture(scope='class')
        def recorded_request_two(self, runner: CliRunner):
          record_result = runner.invoke(record, [NON_DETERMINISTIC_GET_REQUEST_URL])
          assert record_result.exit_code == 0
          return Request.last()

        @pytest.fixture(scope='class', autouse=True)
        def snapshot_one_result(self, runner: CliRunner, recorded_request_one: Request):
          snapshot_result = runner.invoke(request, ['snapshot', recorded_request_one.key()])
          assert snapshot_result.exit_code == 0
          return snapshot_result

        @pytest.fixture(scope='class', autouse=True)
        def snapshot_two_result(self, runner: CliRunner, recorded_request_two: Request):
          snapshot_result = runner.invoke(request, ['snapshot', recorded_request_two.key()])
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
      def created_scenario(self, runner: CliRunner):
          create_result = runner.invoke(scenario, ['create', 'test'])
          assert create_result.exit_code == 0
          return Scenario.last()

      @pytest.fixture(scope='class', autouse=True)
      def put_event(self, runner: CliRunner, created_scenario: Scenario):
        snapshot_result = runner.invoke(scenario, ['snapshot', created_scenario.key()])
        assert snapshot_result.exit_code == 0

        log = Log()
        events = log.events
        event = events[len(events) - 1]
        metadata_path = event.snapshot().metadata_path
        with open(metadata_path, 'w') as fp:
          fp.write('junk')

        return event

      @pytest.fixture(scope='class', autouse=True)
      def removed_scenario(self, created_scenario: Scenario):
        created_scenario.delete()
        assert Scenario.find(created_scenario.id) == None

      def test_creates_scenario_with_uuid_name(self, runner: CliRunner, created_scenario: Scenario):
        apply_result = runner.invoke(snapshot, ['apply'])
        assert apply_result.exit_code == 0

        recreated_scenario = Scenario.find_by(uuid=created_scenario.uuid)
        assert recreated_scenario.name == created_scenario.uuid

    class TestWhenMissingScenarioMetadata():

      @pytest.fixture(scope='class')
      def created_scenario(self, runner: CliRunner):
          create_result = runner.invoke(scenario, ['create', 'test'])
          assert create_result.exit_code == 0
          return Scenario.last()

      @pytest.fixture(scope='class', autouse=True)
      def put_event(self, runner: CliRunner, created_scenario: Scenario):
        snapshot_result = runner.invoke(scenario, ['snapshot', created_scenario.key()])
        assert snapshot_result.exit_code == 0

        log = Log()
        events = log.events
        event = events[len(events) - 1]
        metadata_path = event.snapshot().metadata_path
        os.remove(metadata_path)

        return event

      @pytest.fixture(scope='class', autouse=True)
      def removed_scenario(self, created_scenario: Scenario):
        created_scenario.delete()
        assert Scenario.find(created_scenario.id) == None

      def test_skips_scenario(self, runner: CliRunner, created_scenario: Scenario):
        apply_result = runner.invoke(snapshot, ['apply'])
        assert apply_result.exit_code == 0

        recreated_scenario = Scenario.find_by(uuid=created_scenario.uuid)
        assert recreated_scenario == None
  
    class TestWhenMalformedRequest():

      @pytest.fixture(scope='class')
      def recorded_request(self, runner: CliRunner):
        record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
        assert record_result.exit_code == 0
        return Request.last()

      @pytest.fixture(autouse=True, scope='class')
      def put_event(self, runner: CliRunner, recorded_request: Request):
        snapshot_result = runner.invoke(request, ['snapshot', recorded_request.key()])
        assert snapshot_result.exit_code == 0

        log = Log()
        events = log.events
        event = events[len(events) - 1]

        with open(event.snapshot().path, 'w') as fp:
          fp.write('junk')

        return event

      @pytest.fixture(scope='class', autouse=True)
      def removed_request(self, recorded_request: Request):
        recorded_request.delete()
        assert Request.find(recorded_request.id) == None

      def test_it_creates_request(self, runner: CliRunner, recorded_request: Request):
        apply_result = runner.invoke(snapshot, ['apply'])
        assert apply_result.exit_code == 1

        assert Request.find_by(uuid=recorded_request.uuid) == None

      def test_idempotent(self, runner: CliRunner, recorded_request: Request, put_event: LogEvent):
        apply_result = runner.invoke(snapshot, ['apply', put_event.uuid])
        assert apply_result.exit_code == 1

        assert Request.find_by(uuid=recorded_request.uuid) == None

    class TestWhenMalformedScenarioRequest():

      @pytest.fixture(scope='class')
      def created_scenario(self, runner: CliRunner):
          create_result = runner.invoke(scenario, ['create', 'test'])
          assert create_result.exit_code == 0
          return Scenario.last()

      @pytest.fixture(scope='class', autouse=True)
      def created_scenario_requests(self, runner: CliRunner, created_scenario: Scenario):
          record_result = runner.invoke(record, ['--scenario-key', created_scenario.key(), DETERMINISTIC_GET_REQUEST_URL])
          assert record_result.exit_code == 0

          return created_scenario.requests

      @pytest.fixture(scope='class', autouse=True)
      def put_event(self, runner: CliRunner, created_scenario: Scenario):
        snapshot_result = runner.invoke(scenario, ['snapshot', created_scenario.key()])
        assert snapshot_result.exit_code == 0

        log = Log()
        events = log.events
        event = events[len(events) - 1]
        event.snapshot().iter_request_snapshots(lambda snapshot: write_junk(snapshot.path))

        return event

      @pytest.fixture(scope='class', autouse=True)
      def removed_scenario(self, created_scenario: Scenario):
        created_scenario.delete()
        assert Scenario.find(created_scenario.id) == None

      def test_skips_scenario(self, runner: CliRunner, created_scenario: Scenario):
        apply_result = runner.invoke(snapshot, ['apply'])
        assert apply_result.exit_code == 1

        recreated_scenario = Scenario.find_by(uuid=created_scenario.uuid)
        assert recreated_scenario

        assert len(recreated_scenario.requests) == 0

      def test_idempotent(self, runner: CliRunner, created_scenario: Scenario, put_event: LogEvent):
        apply_result = runner.invoke(snapshot, ['apply', put_event.uuid])
        assert apply_result.exit_code == 1

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
        def created_scenario(self, runner: CliRunner):
          create_result = runner.invoke(scenario, ['create', 'test'])
          assert create_result.exit_code == 0
          return Scenario.last()

        @pytest.fixture(scope='class', autouse=True)
        def created_scenario_requests(self, runner: CliRunner, created_scenario: Scenario):
          record_result = runner.invoke(record, ['--scenario-key', created_scenario.key(), DETERMINISTIC_GET_REQUEST_URL])
          assert record_result.exit_code == 0

          record_result = runner.invoke(record, ['--scenario-key', created_scenario.key(), NON_DETERMINISTIC_GET_REQUEST_URL])
          assert record_result.exit_code == 0

          return created_scenario.requests

        @pytest.fixture(scope='class', autouse=True)
        def delete_event(self, runner: CliRunner, created_scenario: Scenario, created_scenario_requests: List[Request]):
          snapshot_result = runner.invoke(scenario, ['snapshot', created_scenario.key()])
          assert snapshot_result.exit_code == 0

          time.sleep(0.5) # So events do not have the same uuid

          created_request = created_scenario_requests[1]
          snapshot_result = runner.invoke(request, ['snapshot', created_request.key(), '--action', DELETE_ACTION])
          assert snapshot_result.exit_code == 0

          log = Log()
          events = log.events
          return events[len(events) - 1]

        @pytest.fixture(scope='class')
        def apply_result(self, runner: CliRunner, created_scenario: Scenario):
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
        def created_scenario_one(self, runner: CliRunner):
          create_result = runner.invoke(scenario, ['create', 'test1'])
          assert create_result.exit_code == 0
          return Scenario.last()

        @pytest.fixture(scope='class')
        def created_scenario_two(self, runner: CliRunner):
          create_result = runner.invoke(scenario, ['create', 'test2'])
          assert create_result.exit_code == 0
          return Scenario.last()

        @pytest.fixture(scope='class', autouse=True)
        def created_scenario_request(self, runner: CliRunner, created_scenario_one: Scenario):
          record_result = runner.invoke(record, ['--scenario-key', created_scenario_one.key(), DETERMINISTIC_GET_REQUEST_URL])
          assert record_result.exit_code == 0

          return created_scenario_one.requests[0]

        @pytest.fixture(scope='class', autouse=True)
        def put_event_one(self, runner: CliRunner, created_scenario_one: Scenario, created_scenario_request: Request):
          snapshot_result = runner.invoke(scenario, ['snapshot', created_scenario_one.key()])
          assert snapshot_result.exit_code == 0

          log = Log()
          events = log.events
          return events[len(events) - 1]

        @pytest.fixture(scope='class', autouse=True)
        def put_event_two(self, runner: CliRunner, created_scenario_two: Scenario, created_scenario_request: Request):
          created_scenario_request.update(scenario_id=created_scenario_two.id)

          snapshot_result = runner.invoke(scenario, ['snapshot', created_scenario_two.key()])
          assert snapshot_result.exit_code == 0

          log = Log()
          events = log.events
          return events[len(events) - 1]

        @pytest.fixture(scope='class')
        def apply_result(self, runner: CliRunner):
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
        def created_scenario(self, runner: CliRunner):
          create_result = runner.invoke(scenario, ['create', 'test'])
          assert create_result.exit_code == 0
          return Scenario.last()

        @pytest.fixture(scope='class', autouse=True)
        def created_scenario_requests(self, runner: CliRunner, created_scenario: Scenario):
          record_result = runner.invoke(record, ['--scenario-key', created_scenario.key(), DETERMINISTIC_GET_REQUEST_URL])
          assert record_result.exit_code == 0

          record_result = runner.invoke(record, ['--scenario-key', created_scenario.key(), NON_DETERMINISTIC_GET_REQUEST_URL])
          assert record_result.exit_code == 0

          return created_scenario.requests

        @pytest.fixture(scope='class', autouse=True)
        def snapshots(self, runner: CliRunner, created_scenario: Scenario, created_scenario_requests: List[Request]):
          snapshot_result = runner.invoke(scenario, ['snapshot', created_scenario.key()])
          assert snapshot_result.exit_code == 0

          created_request = created_scenario_requests[1]
          snapshot_result = runner.invoke(request, ['snapshot', created_request.key(), '--action', DELETE_ACTION])
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
        def created_scenario(self, runner: CliRunner):
          create_result = runner.invoke(scenario, ['create', 'test'])
          assert create_result.exit_code == 0
          return Scenario.last()

        @pytest.fixture(scope='class', autouse=True)
        def created_scenario_requests(self, runner: CliRunner, created_scenario: Scenario):
          record_result = runner.invoke(record, ['--scenario-key', created_scenario.key(), DETERMINISTIC_GET_REQUEST_URL])
          assert record_result.exit_code == 0

          record_result = runner.invoke(record, ['--scenario-key', created_scenario.key(), NON_DETERMINISTIC_GET_REQUEST_URL])
          assert record_result.exit_code == 0

          return created_scenario.requests

        @pytest.fixture(scope='class', autouse=True)
        def apply_result(self, runner: CliRunner, created_scenario: Scenario, created_scenario_requests: List[Request]):
          snapshot_result = runner.invoke(scenario, ['snapshot', created_scenario.key()])
          assert snapshot_result.exit_code == 0

          created_scenario = Scenario.find(created_scenario.id)
          assert created_scenario.requests_count == 2
          apply_result = runner.invoke(snapshot, ['apply'])
          assert apply_result.exit_code == 0

          created_request = created_scenario_requests[1]
          snapshot_result = runner.invoke(request, ['snapshot', created_request.key(), '--action', DELETE_ACTION])
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