import json
import os
import pdb
import time

import pytest

from click.testing import CliRunner

from stoobly_agent.test.test_helper import DETERMINISTIC_GET_REQUEST_URL, NON_DETERMINISTIC_GET_REQUEST_URL, reset

from stoobly_agent.app.cli.scenario_cli import scenario
from stoobly_agent.app.models.adapters.orm import JoinedRequestStringAdapter
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

        raw_requests = snapshot.requests

        assert raw_requests[0] == JoinedRequestStringAdapter(recorded_request_one).adapt()
        assert raw_requests[1] == JoinedRequestStringAdapter(recorded_request_two).adapt()

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

        # Move request to B and snapshot B without re-snapshotting A — both YAMLs list the request
        shared_request.update(scenario_id=scenario_two.id)
        time.sleep(0.5)
        put_two = runner.invoke(scenario, ['snapshot', 'create', scenario_two.key()])
        assert put_two.exit_code == 0

        request_path = RequestSnapshot.create(shared_request.uuid).path
        assert os.path.isfile(request_path)

        delete_one = runner.invoke(
          scenario,
          ['snapshot', 'create', '--action', DELETE_ACTION, scenario_one.key()],
        )
        assert delete_one.exit_code == 0

        assert os.path.isfile(request_path)
        assert ScenarioSnapshot.create(scenario_two.uuid).exists
        assert not ScenarioSnapshot.create(scenario_one.uuid).exists

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
        request_path = RequestSnapshot.create(recorded_request.uuid).path
        assert os.path.isfile(metadata_path)
        assert os.path.isfile(request_path)

        delete_result = runner.invoke(
          scenario,
          ['snapshot', 'create', '--action', DELETE_ACTION, created_scenario.key()],
        )
        assert delete_result.exit_code == 0
        assert not os.path.exists(metadata_path)
        assert not os.path.exists(request_path)
        assert Log().events[-1].action == DELETE_ACTION

      def test_it_rejects_invalid_action(self, created_scenario: Scenario):
        assert snapshot_scenario(created_scenario, action='INVALID') is None