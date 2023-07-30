import pdb
import pytest

from click.testing import CliRunner

from stoobly_agent.test.test_helper import DETERMINISTIC_GET_REQUEST_URL, reset

from stoobly_agent.cli import record, request, scenario
from stoobly_agent.lib.api.keys import ScenarioKey
from stoobly_agent.lib.orm.scenario import Scenario

@pytest.fixture(scope='module')
def runner():
  return CliRunner()

@pytest.fixture(autouse=True, scope='module')
def settings():
  return reset()

class TestCreate():
  @pytest.fixture(scope='class')
  def scenario_name(self):
    return 'Login 1.0.0'

  @pytest.fixture(scope='class')
  def scenario_description(self):
    return 'Login flow for service A'

  @pytest.fixture(scope='class')
  def scenario_create_cli_results(self, runner: CliRunner, scenario_name: str, scenario_description: str):
    scenario_create_result = runner.invoke(scenario, ['create', '--without-headers', '--description', scenario_description, '--select', 'key', scenario_name])
    assert scenario_create_result.exit_code == 0

    return scenario_create_result

  @pytest.fixture(scope='class')
  def scenario_key(self, scenario_create_cli_results):
    output = scenario_create_cli_results.stdout
    return output.strip()

  def test_it_lists_scenario(self, runner: CliRunner, scenario_name: str, scenario_description: str, scenario_key: str):
    scenario_result = runner.invoke(scenario, ['list', '--without-headers', '--select', 'key'])
    assert scenario_result.exit_code == 0

    output = scenario_result.stdout
    _scenario_key = output.strip()

    _scenario = Scenario.find_by(uuid=ScenarioKey(_scenario_key).id)

    assert _scenario.key() == scenario_key
    assert _scenario.name == scenario_name
    assert _scenario.description == scenario_description

  def test_it_shows_scenario(self, runner: CliRunner, scenario_name: str, scenario_description: str, scenario_key: str):
    scenario_result = runner.invoke(scenario, ['show', '--without-headers', '--select', 'key', scenario_key])
    assert scenario_result.exit_code == 0

    output = scenario_result.stdout
    _scenario_key = output.strip()

    _scenario = Scenario.find_by(uuid=ScenarioKey(_scenario_key).id)

    assert _scenario.key() == scenario_key
    assert _scenario.name == scenario_name
    assert _scenario.description == scenario_description

  class TestWhenCreatingRequests():

    def test_it_increments_request_count(self, runner: CliRunner, scenario_key: str):
      requests_count = 2
      for i in range(requests_count):
        self.__record_request(runner, DETERMINISTIC_GET_REQUEST_URL, scenario_key)

      scenario_result = runner.invoke(scenario, ['show', '--without-headers', '--select', 'requests_count', scenario_key])
      assert scenario_result.exit_code == 0

      _requests_count = int(scenario_result.stdout.strip())
      assert _requests_count == requests_count
  
    def __record_request(self, runner: CliRunner, url: str, scenario_key: str):
      record_result = runner.invoke(record, ['--scenario-key', scenario_key, url])
      assert record_result.exit_code == 0

    class TestWhenDeletingRequests():

      def test_it_decrements_request_count(self, runner: CliRunner, scenario_key: str):
        requests_result = runner.invoke(request, ['list', '--scenario-key', scenario_key, '--without-headers', '--select', 'key'])
        assert requests_result.exit_code == 0

        keys = requests_result.stdout.strip().split("\n")
        for key in keys:
          self.__delete_request(runner, key)

        scenario_result = runner.invoke(scenario, ['show', '--without-headers', '--select', 'requests_count', scenario_key])
        assert scenario_result.exit_code == 0

        _requests_count = int(scenario_result.stdout.strip())
        assert _requests_count == 0

      def __delete_request(self, runner: CliRunner, request_key: str):
        delete_result = runner.invoke(request, ['delete', request_key])
        assert delete_result.exit_code == 0