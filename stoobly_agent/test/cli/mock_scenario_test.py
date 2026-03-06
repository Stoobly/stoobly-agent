import pdb
import pytest

from click.testing import CliRunner
from pathlib import Path

from stoobly_agent.test.test_helper import DETERMINISTIC_GET_REQUEST_URL, NON_DETERMINISTIC_GET_REQUEST_URL

from stoobly_agent.app.cli.scenario_cli import scenario
from stoobly_agent.config.constants.custom_headers import SESSION_ID
from stoobly_agent.cli import mock, record
from stoobly_agent.lib.api.keys.scenario_key import ScenarioKey
from stoobly_agent.lib.orm.request import Request

@pytest.fixture(scope='module')
def runner():
  return CliRunner()

class TestMocking():
  @pytest.fixture(scope='class')
  def lifecycle_hooks_path(self):
    return str(Path(__file__).parent / 'mock_scenario_lifecycle_hooks.py')

  class TestScenario():
    @pytest.fixture(scope='class')
    def scenario_key(self, runner: CliRunner):
      res = runner.invoke(scenario, ['create', '--select', 'key', '--without-headers', 'test-scenario'])
      assert res.exit_code == 0
      return ScenarioKey(res.stdout.strip()).raw

    @pytest.fixture(autouse=True, scope='class')
    def recorded_request1(self, runner: CliRunner, scenario_key: str):
      record_result = runner.invoke(record, ['--scenario-key', scenario_key, DETERMINISTIC_GET_REQUEST_URL])
      assert record_result.exit_code == 0
      return Request.last()

    @pytest.fixture(autouse=True, scope='class')
    def recorded_request2(self, runner: CliRunner, scenario_key: str):
      record_result = runner.invoke(record, ['--scenario-key', scenario_key, DETERMINISTIC_GET_REQUEST_URL])
      assert record_result.exit_code == 0
      return Request.last()

    def test_it_does_not_mocks(self, runner: CliRunner, scenario_key: str):
      mock_result = runner.invoke(mock, ['--scenario-key', scenario_key, NON_DETERMINISTIC_GET_REQUEST_URL])
      assert mock_result.exit_code == 1

    def test_it_mocks(self, runner: CliRunner, scenario_key: str):
      mock_result = runner.invoke(mock, ['--scenario-key', scenario_key, DETERMINISTIC_GET_REQUEST_URL])
      assert mock_result.exit_code == 0

    def test_it_mocks_in_order(
      self, runner: CliRunner, lifecycle_hooks_path: str, recorded_request1: Request, recorded_request2: Request, scenario_key: str
    ):
      session_id = 'test'
      args = [
        '--lifecycle-hooks-path', lifecycle_hooks_path, '--scenario-key', scenario_key, '--output', '/dev/null',
        '-H', f"{SESSION_ID}: {session_id}", DETERMINISTIC_GET_REQUEST_URL
      ]
      mock_result = runner.invoke(mock, args)
      assert int(mock_result.stdout) == recorded_request1.id

      mock_result = runner.invoke(mock, args)
      assert int(mock_result.stdout) == recorded_request2.id