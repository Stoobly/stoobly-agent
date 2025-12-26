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
from stoobly_agent.cli import record
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.lib.orm.scenario import Scenario
from stoobly_agent.test.test_helper import assert_orm_request_equivalent, DETERMINISTIC_GET_REQUEST_URL, NON_DETERMINISTIC_GET_REQUEST_URL, reset

@pytest.fixture(scope='module')
def runner():
    return CliRunner()

class TestPrune():
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

      def test_it_prunes(self, runner: CliRunner, log: Log):
        assert len(log.events) == 2
        apply_result = runner.invoke(snapshot, ['prune'])
        assert apply_result.exit_code == 0
        assert len(log.events) == 0

    class TestWhenCreatingRequest():

      @pytest.fixture(scope='class')
      def log(self):
        return Log()

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

      def test_it_does_not_prune(self, runner: CliRunner, log: Log):
        apply_result = runner.invoke(snapshot, ['prune'])
        assert apply_result.exit_code == 0
        assert len(log.events) == 1

    class TestWhenMissingSnapshot():

      @pytest.fixture(scope='class')
      def log(self):
        return Log()

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

      def test_it_prunes(self, runner: CliRunner, log: Log):
        event = log.events[0]
        event.snapshot().remove()
        assert len(log.events) == 1

        apply_result = runner.invoke(snapshot, ['prune'])
        assert apply_result.exit_code == 0
        assert len(log.events) == 0

    class TestWhenRemoveScenarioRequest():
      '''
      1. Create scenario
      2. Add 2 requests to it
      3. Snapshot scenario
      4. Snapshot second request with action DELETE_ACTION
      5. Prune
      6. Apply
      7. Expect scenario to have 1 request, because scenario depends on the request, should not be able to prune
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
        prune_result = runner.invoke(snapshot, ['prune'])
        assert prune_result.exit_code == 0

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