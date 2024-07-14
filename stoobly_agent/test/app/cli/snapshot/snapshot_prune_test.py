import pdb
import pytest
import time

from click.testing import CliRunner

from stoobly_agent.app.models.factories.resource.local_db.helpers.log import Log
from stoobly_agent.app.models.factories.resource.local_db.helpers.log_event import DELETE_ACTION, LogEvent
from stoobly_agent.cli import record, request, snapshot
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.test.test_helper import DETERMINISTIC_GET_REQUEST_URL, reset

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