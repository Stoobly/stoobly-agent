import pdb
import pytest
import tempfile

from click.testing import CliRunner

from stoobly_agent.app.cli.request_cli import request
from stoobly_agent.app.cli.scenario_cli import scenario
from stoobly_agent.app.cli.snapshot_cli import snapshot
from stoobly_agent.app.models.factories.resource.local_db.helpers.log import Log
from stoobly_agent.app.models.factories.resource.local_db.helpers.scenario_snapshot import ScenarioSnapshotV2
from stoobly_agent.app.models.factories.resource.local_db.helpers.snapshot_types import SCENARIO_RESOURCE
from stoobly_agent.cli import record
from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.lib.api.keys import RequestKey, ScenarioKey
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.lib.orm.scenario import Scenario
from stoobly_agent.test.test_helper import DETERMINISTIC_GET_REQUEST_URL, reset

@pytest.fixture(scope='module')
def runner():
    return CliRunner()

class TestCopy():
    @pytest.fixture(scope='class', autouse=True)
    @classmethod
    def settings(cls):
      return reset()

    class TestWhenRequest():
      @pytest.fixture(scope='class')
      @classmethod
      def recorded_request(cls, runner: CliRunner):
        record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
        assert record_result.exit_code == 0
        return Request.last()

      @pytest.fixture(autouse=True, scope='class')
      @classmethod
      def snapshot_result(cls, runner: CliRunner, recorded_request: Request):
        snapshot_result = runner.invoke(request, ['snapshot', 'create', recorded_request.key()])
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
          assert request_key.id == event.resource_id

    class TestWhenScenario():
      @pytest.fixture(scope='class', autouse=True)
      @classmethod
      def settings(cls):
        return reset()

      @pytest.fixture(scope='class')
      @classmethod
      def created_scenario(cls, runner: CliRunner):
        create_result = runner.invoke(scenario, ['create', 'copy-flow'])
        assert create_result.exit_code == 0
        return Scenario.last()

      @pytest.fixture(scope='class', autouse=True)
      @classmethod
      def snapshot_result(cls, runner: CliRunner, created_scenario: Scenario):
        record_result = runner.invoke(
          record,
          ['--scenario-key', created_scenario.key(), DETERMINISTIC_GET_REQUEST_URL],
        )
        assert record_result.exit_code == 0

        snapshot_result = runner.invoke(scenario, ['snapshot', 'create', created_scenario.key()])
        assert snapshot_result.exit_code == 0
        return snapshot_result

      def test_it_copies(self, runner: CliRunner, created_scenario: Scenario):
        with tempfile.TemporaryDirectory() as dirpath:
          data_dir = DataDir(dirpath)
          log = Log(data_dir)

          assert len(log.events) == 0

          copy_result = runner.invoke(
            snapshot,
            ['copy', dirpath, '--scenario-key', created_scenario.key()],
          )
          assert copy_result.exit_code == 0
          assert 'No snapshot found' not in (copy_result.output or '')

          assert len(log.events) == 1
          event = log.events[0]
          assert event.resource == SCENARIO_RESOURCE
          # Destination may write v2 name locator or v1 uuid depending on format
          sanitized = ScenarioSnapshotV2.sanitize_scenario_filename(created_scenario.name)
          assert event.resource_id in (created_scenario.uuid, sanitized)
          assert event.snapshot().uuid == ScenarioKey(created_scenario.key()).id
