import json
import pdb
import pytest

from click.testing import CliRunner

from stoobly_agent.test.test_helper import DETERMINISTIC_GET_REQUEST_URL, NON_DETERMINISTIC_GET_REQUEST_URL, reset

from stoobly_agent.app.cli.scenario_cli import scenario
from stoobly_agent.app.models.adapters.orm import JoinedRequestStringAdapter
from stoobly_agent.app.models.factories.resource.local_db.helpers.log import Log
from stoobly_agent.app.models.factories.resource.local_db.helpers.scenario_snapshot import ScenarioSnapshot
from stoobly_agent.cli import record
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.lib.orm.scenario import Scenario

@pytest.fixture(scope='module')
def runner():
    return CliRunner()

class TestScenario():
    @pytest.fixture(scope='class', autouse=True)
    def settings(self):
      return reset()

    class TestWhenReplacing():

      @pytest.fixture(scope='class')
      def created_scenario(self, runner: CliRunner):
          create_result = runner.invoke(scenario, ['create', 'test'])
          assert create_result.exit_code == 0
          return Scenario.last()

      @pytest.fixture(scope='class', autouse=True)
      def recorded_request_one(self, runner: CliRunner, created_scenario: Scenario):
          record_result = runner.invoke(record, ['--scenario-key', created_scenario.key(), DETERMINISTIC_GET_REQUEST_URL])
          assert record_result.exit_code == 0
          return Request.last()

      @pytest.fixture(scope='class', autouse=True)
      def recorded_request_two(self, runner: CliRunner, created_scenario: Scenario):
          record_result = runner.invoke(record, ['--scenario-key', created_scenario.key(), NON_DETERMINISTIC_GET_REQUEST_URL])
          assert record_result.exit_code == 0
          return Request.last()

      @pytest.fixture(scope='class', autouse=True)
      def snapshot_result(self, runner: CliRunner, created_scenario: Scenario):
        snapshot_result = runner.invoke(scenario, ['snapshot', created_scenario.key()])
        assert snapshot_result.exit_code == 0
        return snapshot_result

      def test_it_prints_request_snapshot_paths(self, created_scenario: Scenario, snapshot_result: CliRunner):
        snapshot = ScenarioSnapshot(created_scenario.uuid)
        request_snapshots = snapshot.request_snapshots

        request_snapshot_paths = []
        for request_snapshot in request_snapshots:
          request_snapshot_paths.append(request_snapshot.path)

        assert sorted(request_snapshot_paths) == sorted(snapshot_result.stdout.strip().split('\n'))

      def test_it_snapshots_metadata(self, created_scenario: Scenario):
        snapshot = ScenarioSnapshot(created_scenario.uuid)

        scenario_metadata = snapshot.metadata
        
        assert scenario_metadata['name'] == created_scenario.name
        assert scenario_metadata['description'] == created_scenario.description

      def test_it_snapshots(self, created_scenario: Scenario, recorded_request_one: Request, recorded_request_two: Request):
        snapshot = ScenarioSnapshot(created_scenario.uuid)

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
        snapshot_result = runner.invoke(scenario, ['snapshot', created_scenario.key()])
        assert snapshot_result.exit_code == 0

        log = Log()

        events = log.raw_events
        assert len(events) == 2

        unprocessed_events = log.unprocessed_events
        assert len(unprocessed_events) == 1