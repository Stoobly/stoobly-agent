import os
import time

import pytest

from click.testing import CliRunner

from stoobly_agent.test.test_helper import DETERMINISTIC_GET_REQUEST_URL, NON_DETERMINISTIC_GET_REQUEST_URL, reset

from stoobly_agent.app.cli.scenario_cli import scenario
from stoobly_agent.app.models.adapters.joined_request_adapter import JoinedRequestAdapter
from stoobly_agent.app.models.adapters.orm import JoinedRequestStringAdapter
from stoobly_agent.app.models.adapters.raw_http_request_adapter import RawHttpRequestAdapter
from stoobly_agent.app.models.adapters.raw_http_response_adapter import RawHttpResponseAdapter
from stoobly_agent.app.models.factories.resource.local_db.helpers.log import Log
from stoobly_agent.app.models.factories.resource.local_db.helpers.log_event import DELETE_ACTION
from stoobly_agent.app.models.factories.resource.local_db.helpers.request_snapshot import RequestSnapshot
from stoobly_agent.app.models.factories.resource.local_db.helpers.scenario_snapshot import ScenarioSnapshot
from stoobly_agent.app.models.factories.resource.local_db.helpers.snapshot_service import snapshot_scenario
from stoobly_agent.cli import record
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.lib.orm.scenario import Scenario

@pytest.fixture(scope='module')
def runner():
    return CliRunner()

def _headers_by_lower_name(headers) -> dict:
  return {str(k).lower(): v for k, v in dict(headers).items()}

def assert_joined_requests_equivalent(actual: bytes, expected: bytes):
  """
  Compare reconstituted snapshot bytes to ORM joined bytes.

  Header line order among mixed dedup-list / non-dedup-list headers may differ
  after v2 externalize/reconstitute; compare header maps and bodies instead.
  """
  actual_adapter = JoinedRequestAdapter(actual)
  expected_adapter = JoinedRequestAdapter(expected)

  actual_req = RawHttpRequestAdapter(actual_adapter.build_request_string().get(control=False))
  expected_req = RawHttpRequestAdapter(expected_adapter.build_request_string().get(control=False))
  assert actual_req.method == expected_req.method
  assert actual_req.url == expected_req.url
  assert _headers_by_lower_name(actual_req.headers) == _headers_by_lower_name(expected_req.headers)
  assert actual_req.body == expected_req.body

  actual_res = RawHttpResponseAdapter(actual_adapter.build_response_string().get(control=False))
  expected_res = RawHttpResponseAdapter(expected_adapter.build_response_string().get(control=False))
  assert actual_res.status == expected_res.status
  assert _headers_by_lower_name(actual_res.headers) == _headers_by_lower_name(expected_res.headers)
  assert actual_res.body == expected_res.body

class TestScenario():
    @pytest.fixture(scope='class', autouse=True)
    @classmethod
    def settings(cls):
      return reset()

    class TestWhenReplacing():

      @pytest.fixture(scope='class')
      @classmethod
      def created_scenario(cls, runner: CliRunner):
          create_result = runner.invoke(scenario, ['create', 'test'])
          assert create_result.exit_code == 0
          return Scenario.last()

      @pytest.fixture(scope='class', autouse=True)
      @classmethod
      def recorded_request_one(cls, runner: CliRunner, created_scenario: Scenario):
          record_result = runner.invoke(record, ['--scenario-key', created_scenario.key(), DETERMINISTIC_GET_REQUEST_URL])
          assert record_result.exit_code == 0
          return Request.last()

      @pytest.fixture(scope='class', autouse=True)
      @classmethod
      def recorded_request_two(cls, runner: CliRunner, created_scenario: Scenario):
          record_result = runner.invoke(record, ['--scenario-key', created_scenario.key(), NON_DETERMINISTIC_GET_REQUEST_URL])
          assert record_result.exit_code == 0
          return Request.last()

      @pytest.fixture(scope='class', autouse=True)
      @classmethod
      def snapshot_result(cls, runner: CliRunner, created_scenario: Scenario):
        snapshot_result = runner.invoke(scenario, ['snapshot', 'create', created_scenario.key()])
        assert snapshot_result.exit_code == 0
        return snapshot_result

      def test_it_prints_request_snapshot_paths(self, created_scenario: Scenario, snapshot_result: CliRunner):
        snapshot = ScenarioSnapshot.create(created_scenario.uuid)
        request_snapshots = snapshot.request_snapshots

        request_snapshot_paths = []
        for request_snapshot in request_snapshots:
          request_snapshot_paths.append(request_snapshot.path)

        assert sorted(request_snapshot_paths) == sorted(snapshot_result.stdout.strip().split('\n'))

      def test_it_snapshots_metadata(self, created_scenario: Scenario):
        snapshot = ScenarioSnapshot.create(created_scenario.uuid)

        scenario_metadata = snapshot.metadata
        
        assert scenario_metadata['name'] == created_scenario.name
        assert scenario_metadata['description'] == created_scenario.description

      def test_it_snapshots(self, created_scenario: Scenario, recorded_request_one: Request, recorded_request_two: Request):
        snapshot = ScenarioSnapshot.create(created_scenario.uuid)

        by_uuid = {s.uuid: s.request for s in snapshot.request_snapshots}
        assert set(by_uuid) == {recorded_request_one.uuid, recorded_request_two.uuid}

        assert_joined_requests_equivalent(
          by_uuid[recorded_request_one.uuid],
          JoinedRequestStringAdapter(recorded_request_one).adapt(),
        )
        assert_joined_requests_equivalent(
          by_uuid[recorded_request_two.uuid],
          JoinedRequestStringAdapter(recorded_request_two).adapt(),
        )

      def test_it_logs(self):
        log = Log()

        events = log.raw_events
        assert len(events) == 1

        unprocessed_events = log.unprocessed_events
        assert len(unprocessed_events) == 1

      def test_it_deletes(self, runner: CliRunner, created_scenario: Scenario):
        snapshot_result = runner.invoke(scenario, ['snapshot', 'create', created_scenario.key()])
        assert snapshot_result.exit_code == 0

        log = Log()

        events = log.raw_events
        assert len(events) == 2

        unprocessed_events = log.unprocessed_events
        assert len(unprocessed_events) == 1

    class TestWhenSharedRequestAcrossScenarios():
      '''
      Deleting scenario A keeps request files still referenced by scenario B's snapshot.
      '''

      @pytest.fixture(scope='class', autouse=True)
      @classmethod
      def settings(cls):
        return reset()

      @pytest.fixture(scope='class')
      @classmethod
      def scenario_one(cls, runner: CliRunner):
        create_result = runner.invoke(scenario, ['create', 'shared-one'])
        assert create_result.exit_code == 0
        return Scenario.last()

      @pytest.fixture(scope='class')
      @classmethod
      def scenario_two(cls, runner: CliRunner):
        create_result = runner.invoke(scenario, ['create', 'shared-two'])
        assert create_result.exit_code == 0
        return Scenario.last()

      @pytest.fixture(scope='class', autouse=True)
      @classmethod
      def shared_request(cls, runner: CliRunner, scenario_one: Scenario):
        record_result = runner.invoke(
          record,
          ['--scenario-key', scenario_one.key(), DETERMINISTIC_GET_REQUEST_URL],
        )
        assert record_result.exit_code == 0
        return Request.last()

      def test_delete_keeps_shared_request_file(
        self,
        runner: CliRunner,
        scenario_one: Scenario,
        scenario_two: Scenario,
        shared_request: Request,
      ):
        # Snapshot A while it owns the request
        put_one = runner.invoke(scenario, ['snapshot', 'create', scenario_one.key()])
        assert put_one.exit_code == 0

        # Move request to B and snapshot B without re-snapshotting A — both YAMLs embed the request
        shared_request.update(scenario_id=scenario_two.id)
        time.sleep(0.5)
        put_two = runner.invoke(scenario, ['snapshot', 'create', scenario_two.key()])
        assert put_two.exit_code == 0

        assert RequestSnapshot.create(shared_request.uuid).request is not None

        request_snap = RequestSnapshot.create(shared_request.uuid)
        slug_dir = getattr(request_snap, 'slug_dir', None)
        bodies_dir = os.path.join(slug_dir, 'bodies') if slug_dir else None
        body_names = os.listdir(bodies_dir) if bodies_dir and os.path.isdir(bodies_dir) else []

        delete_one = runner.invoke(
          scenario,
          ['snapshot', 'create', '--action', DELETE_ACTION, scenario_one.key()],
        )
        assert delete_one.exit_code == 0

        # Request data remains via scenario two's embedded entry
        assert RequestSnapshot.create(shared_request.uuid).request is not None
        assert ScenarioSnapshot.create(scenario_two.uuid).exists
        assert not ScenarioSnapshot.create(scenario_one.uuid).exists
        # Shared slug blobs must survive delete of the other scenario
        if body_names:
          assert os.path.isdir(bodies_dir)
          for name in body_names:
            assert os.path.isfile(os.path.join(bodies_dir, name))

    class TestWhenDeleteAction():
      @pytest.fixture(scope='class', autouse=True)
      @classmethod
      def settings(cls):
        return reset()

      @pytest.fixture(scope='class')
      @classmethod
      def created_scenario(cls, runner: CliRunner):
        create_result = runner.invoke(scenario, ['create', 'delete-only'])
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

      def test_it_removes_exclusive_files(
        self,
        runner: CliRunner,
        created_scenario: Scenario,
        recorded_request: Request,
      ):
        put_result = runner.invoke(scenario, ['snapshot', 'create', created_scenario.key()])
        assert put_result.exit_code == 0

        metadata_path = ScenarioSnapshot.create(created_scenario.uuid).metadata_path
        assert os.path.isfile(metadata_path)
        assert RequestSnapshot.create(recorded_request.uuid).request is not None

        delete_result = runner.invoke(
          scenario,
          ['snapshot', 'create', '--action', DELETE_ACTION, created_scenario.key()],
        )
        assert delete_result.exit_code == 0
        assert not os.path.exists(metadata_path)
        assert RequestSnapshot.create(recorded_request.uuid).request is None
        assert Log().events[-1].action == DELETE_ACTION

      def test_it_rejects_invalid_action(self, created_scenario: Scenario):
        assert snapshot_scenario(created_scenario, action='INVALID') is None