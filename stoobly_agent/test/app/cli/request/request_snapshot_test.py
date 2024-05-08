import pdb
import pytest

from click.testing import CliRunner

from stoobly_agent.test.test_helper import DETERMINISTIC_GET_REQUEST_URL, reset

from stoobly_agent.app.models.adapters.orm import JoinedRequestStringAdapter
from stoobly_agent.app.models.factories.resource.local_db.helpers.log import Log
from stoobly_agent.app.models.factories.resource.local_db.helpers.log_event import DELETE_ACTION
from stoobly_agent.app.models.factories.resource.local_db.helpers.request_snapshot import RequestSnapshot
from stoobly_agent.cli import record, request
from stoobly_agent.lib.orm.request import Request

@pytest.fixture(scope='module')
def runner():
    return CliRunner()

class TestRequestSnapshot():
    @pytest.fixture(scope='class', autouse=True)
    def settings(self):
      return reset()

    class TestWhenReplacing():

      @pytest.fixture(scope='class')
      def recorded_request(self, runner: CliRunner):
        record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
        assert record_result.exit_code == 0
        return Request.last()

      def test_it_snapshots(self, runner: CliRunner, recorded_request: Request):
        snapshot_result = runner.invoke(request, ['snapshot', recorded_request.key()])
        assert snapshot_result.exit_code == 0

        snapshot = RequestSnapshot(recorded_request.uuid)
        raw_request = snapshot.request

        expected_raw_request = JoinedRequestStringAdapter(recorded_request).adapt()

        assert raw_request == expected_raw_request

        log = Log()

        events = log.raw_events
        assert len(events) == 1

        unprocessed_events = log.unprocessed_events
        assert len(unprocessed_events) == 1

      def test_it_replaces(self, runner: CliRunner, recorded_request: Request):
        snapshot_result = runner.invoke(request, ['snapshot', recorded_request.key()])
        assert snapshot_result.exit_code == 0

        snapshot = RequestSnapshot(recorded_request.uuid)
        raw_request = snapshot.request

        expected_raw_request = JoinedRequestStringAdapter(recorded_request).adapt()

        assert raw_request == expected_raw_request

        log = Log()

        events = log.raw_events
        assert len(events) == 2

        unprocessed_events = log.unprocessed_events
        assert len(unprocessed_events) == 1

      def test_it_deletes(self, runner: CliRunner, recorded_request: Request):
        snapshot_result = runner.invoke(request, ['snapshot', '--action', DELETE_ACTION, recorded_request.key()])
        assert snapshot_result.exit_code == 0

        log = Log()

        events = log.raw_events
        assert len(events) == 3

        unprocessed_events = log.unprocessed_events
        assert len(unprocessed_events) == 0

    class TestWhenAppending():

      @pytest.fixture(scope='class')
      def recorded_request_one(self, runner: CliRunner):
        record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
        assert record_result.exit_code == 0
        return Request.last()

      @pytest.fixture(scope='class')
      def recorded_request_two(self, runner: CliRunner):
        record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
        assert record_result.exit_code == 0
        return Request.last()

      def test_it_appends(self, runner: CliRunner, recorded_request_one: Request, recorded_request_two: Request):
        snapshot_result = runner.invoke(request, ['snapshot', recorded_request_one.key()])
        assert snapshot_result.exit_code == 0

        snapshot_result = runner.invoke(request, ['snapshot', recorded_request_two.key()])
        assert snapshot_result.exit_code == 0

        log = Log()

        events = log.raw_events
        assert len(events) == 2

        unprocessed_events = log.unprocessed_events
        assert len(unprocessed_events) == 2

      def test_it_deletes(self, runner: CliRunner, recorded_request_one: Request, recorded_request_two: Request):
        snapshot_result = runner.invoke(request, ['snapshot', '--action', DELETE_ACTION, recorded_request_one.key()])
        assert snapshot_result.exit_code == 0

        log = Log()

        events = log.raw_events
        assert len(events) == 3

        unprocessed_events = log.unprocessed_events
        assert len(unprocessed_events) == 1

        event = unprocessed_events[0]
        assert event.resource_uuid == recorded_request_two.uuid
