import importlib
import os
import pdb
import pytest
import tempfile

from click.testing import CliRunner

from stoobly_agent.app.models.factories.resource.local_db.helpers.log import Log
from stoobly_agent.cli import record, request, snapshot
from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.lib.api.keys import RequestKey
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.test.test_helper import DETERMINISTIC_GET_REQUEST_URL, reset

@pytest.fixture(scope='module')
def runner():
    return CliRunner()

class TestCopy():
    @pytest.fixture(scope='class', autouse=True)
    def settings(self):
      return reset()

    class TestWhenRequest():
      @pytest.fixture(scope='class')
      def recorded_request(self, runner: CliRunner):
        record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
        assert record_result.exit_code == 0
        return Request.last()

      @pytest.fixture(autouse=True, scope='class')
      def snapshot_result(self, runner: CliRunner, recorded_request: Request):
        snapshot_result = runner.invoke(request, ['snapshot', recorded_request.key()])
        assert snapshot_result.exit_code == 0
        return snapshot_result

      def test_it_copies(self, runner: CliRunner, recorded_request: Request):
        with tempfile.TemporaryDirectory() as dirpath:
          data_dir = DataDir(dirpath)
          log = Log(data_dir)

          # Check that no events have been copied
          assert len(log.events) == 0

          apply_result = runner.invoke(snapshot, ['copy', dirpath, '--request-key', recorded_request.key()])
          assert apply_result.exit_code == 0

          # Check that one event has been copied
          assert len(log.events) == 1

          event = log.events[0]
          request_key = RequestKey(recorded_request.key())

          # Check that the event is the request
          assert request_key.id == event.resource_uuid