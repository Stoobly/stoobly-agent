import os
import pdb
from unittest.mock import patch

import pytest

from click.testing import CliRunner

from stoobly_agent.app.cli.request_cli import request
from stoobly_agent.app.cli.scenario_cli import scenario
from stoobly_agent.app.models.adapters.orm import JoinedRequestStringAdapter
from stoobly_agent.app.models.factories.resource.local_db.helpers.log import Log
from stoobly_agent.app.models.factories.resource.local_db.helpers.log_event import DELETE_ACTION, PUT_ACTION
from stoobly_agent.app.models.factories.resource.local_db.helpers.request_snapshot import RequestSnapshot
from stoobly_agent.app.models.factories.resource.local_db.helpers.snapshot_service import snapshot_request
from stoobly_agent.cli import record
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.lib.orm.scenario import Scenario
from stoobly_agent.test.test_helper import DETERMINISTIC_GET_REQUEST_URL, reset

@pytest.fixture(scope='module')
def runner():
    return CliRunner()

class TestRequestSnapshot():
    @pytest.fixture(scope='class', autouse=True)
    @classmethod
    def settings(cls):
      return reset()

    class TestWhenReplacing():

      @pytest.fixture(scope='class')
      @classmethod
      def recorded_request(cls, runner: CliRunner):
        record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
        assert record_result.exit_code == 0
        return Request.last()

      def test_it_snapshots(self, runner: CliRunner, recorded_request: Request):
        snapshot_result = runner.invoke(request, ['snapshot', 'create', recorded_request.key()])
        assert snapshot_result.exit_code == 0

        snapshot = RequestSnapshot.create(recorded_request.uuid)

        # Assert the snapshot path is printed to stdout
        assert snapshot_result.stdout.strip() == snapshot.path

        raw_request = snapshot.request
        expected_raw_request = JoinedRequestStringAdapter(recorded_request).adapt()

        assert raw_request == expected_raw_request

        log = Log()

        events = log.raw_events
        assert len(events) == 1

        unprocessed_events = log.unprocessed_events
        assert len(unprocessed_events) == 1

      def test_it_replaces(self, runner: CliRunner, recorded_request: Request):
        snapshot_result = runner.invoke(request, ['snapshot', 'create', recorded_request.key()])
        assert snapshot_result.exit_code == 0

        snapshot = RequestSnapshot.create(recorded_request.uuid)
        raw_request = snapshot.request

        expected_raw_request = JoinedRequestStringAdapter(recorded_request).adapt()

        assert raw_request == expected_raw_request

        log = Log()

        events = log.raw_events
        assert len(events) == 2

        unprocessed_events = log.unprocessed_events
        assert len(unprocessed_events) == 1

      def test_it_deletes(self, runner: CliRunner, recorded_request: Request):
        snapshot_result = runner.invoke(request, ['snapshot', 'create', '--action', DELETE_ACTION, recorded_request.key()])
        assert snapshot_result.exit_code == 0

        log = Log()

        events = log.raw_events
        assert len(events) == 3

        unprocessed_events = log.unprocessed_events
        assert len(unprocessed_events) == 0

    class TestWhenAppending():

      @pytest.fixture(scope='class')
      @classmethod
      def recorded_request_one(cls, runner: CliRunner):
        record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
        assert record_result.exit_code == 0
        return Request.last()

      @pytest.fixture(scope='class')
      @classmethod
      def recorded_request_two(cls, runner: CliRunner):
        record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
        assert record_result.exit_code == 0
        return Request.last()

      def test_it_appends(self, runner: CliRunner, recorded_request_one: Request, recorded_request_two: Request):
        snapshot_result = runner.invoke(request, ['snapshot', 'create', recorded_request_one.key()])
        assert snapshot_result.exit_code == 0

        snapshot_result = runner.invoke(request, ['snapshot', 'create', recorded_request_two.key()])
        assert snapshot_result.exit_code == 0

        log = Log()

        events = log.raw_events
        assert len(events) == 2

        unprocessed_events = log.unprocessed_events
        assert len(unprocessed_events) == 2

      def test_it_deletes(self, runner: CliRunner, recorded_request_one: Request, recorded_request_two: Request):
        snapshot_result = runner.invoke(request, ['snapshot', 'create', '--action', DELETE_ACTION, recorded_request_one.key()])
        assert snapshot_result.exit_code == 0

        log = Log()

        events = log.raw_events
        assert len(events) == 3

        unprocessed_events = log.unprocessed_events
        assert len(unprocessed_events) == 1

        event = unprocessed_events[0]
        assert event.resource_id == recorded_request_two.uuid
        assert event.action == PUT_ACTION

    class TestWhenDeleteFirst():

      @pytest.fixture(scope='class')
      @classmethod
      def recorded_request(cls, runner: CliRunner):
        record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
        assert record_result.exit_code == 0
        return Request.last()

      def test_initial_delete(self, runner: CliRunner, recorded_request: Request):
        snapshot_result = runner.invoke(request, ['snapshot', 'create', '--action', DELETE_ACTION, recorded_request.key()])
        assert snapshot_result.exit_code == 0

        log = Log()

        events = log.raw_events
        assert len(events) == 1

        unprocessed_events = log.unprocessed_events
        assert len(unprocessed_events) == 0

      def test_puts(self, runner: CliRunner, recorded_request: Request):
        snapshot_result = runner.invoke(request, ['snapshot', 'create', '--action', PUT_ACTION, recorded_request.key()])
        assert snapshot_result.exit_code == 0

        log = Log()

        events = log.raw_events
        assert len(events) == 2

        unprocessed_events = log.unprocessed_events
        assert len(unprocessed_events) == 1
        assert unprocessed_events[0].action == PUT_ACTION

      def test_final_delete(self, runner: CliRunner, recorded_request: Request):
        snapshot_result = runner.invoke(request, ['snapshot', 'create', '--action', DELETE_ACTION, recorded_request.key()])
        assert snapshot_result.exit_code == 0

        log = Log()

        events = log.events
        assert len(events) == 3

        collapsed_events = log.collapse(events)
        assert len(collapsed_events) == 1
        unprocessed_events = log.unprocessed_events
        assert len(unprocessed_events) == 0

    class TestWhenDeleteWhileScenarioReferences():
      '''
      Request DELETE create keeps the snapshot file when a scenario still references it.
      '''

      @pytest.fixture(scope='class', autouse=True)
      @classmethod
      def settings(cls):
        return reset()

      @pytest.fixture(scope='class')
      @classmethod
      def created_scenario(cls, runner: CliRunner):
        create_result = runner.invoke(scenario, ['create', 'keeps-request'])
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

      def test_it_keeps_request_file(
        self,
        runner: CliRunner,
        created_scenario: Scenario,
        recorded_request: Request,
      ):
        scenario_result = runner.invoke(scenario, ['snapshot', 'create', created_scenario.key()])
        assert scenario_result.exit_code == 0

        request_path = RequestSnapshot.create(recorded_request.uuid).path
        assert os.path.isfile(request_path)

        delete_result = runner.invoke(
          request,
          ['snapshot', 'create', '--action', DELETE_ACTION, recorded_request.key()],
        )
        assert delete_result.exit_code == 0
        assert os.path.isfile(request_path)
        assert Log().events[-1].action == DELETE_ACTION

    class TestWhenLogAppendFailsRollsBack():
      '''
      If history append fails after rewriting a request snapshot, file contents are restored.
      '''

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

      def test_it_restores_previous_contents(self, recorded_request: Request):
        from stoobly_agent.app.models.factories.resource.local_db.helpers.request_snapshot import RequestSnapshotV2

        snapshot_request(recorded_request, action=PUT_ACTION)
        path = RequestSnapshot.create(recorded_request.uuid).path
        with open(path, 'rb') as fp:
          original_on_disk = fp.read()

        def write_distinct(self, text):
          self._ensure_parent(self.path)
          with open(self.path, 'wb') as fp:
            fp.write(b'NEW_CONTENT_SHOULD_NOT_PERSIST')

        with patch.object(RequestSnapshotV2, 'write_raw', write_distinct):
          with patch.object(Log, 'put', side_effect=RuntimeError('log append failed')):
            snapshot_request(recorded_request, action=PUT_ACTION)

        with open(path, 'rb') as fp:
          assert fp.read() == original_on_disk

      def test_it_rejects_invalid_action(self, recorded_request: Request):
        assert snapshot_request(recorded_request, action='INVALID') is None