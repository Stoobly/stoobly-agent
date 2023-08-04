import pdb
import pytest

from click.testing import CliRunner

from stoobly_agent.test.test_helper import reset

from stoobly_agent.cli import config, intercept, scenario
from stoobly_agent.lib.api.keys import ScenarioKey
from stoobly_agent.lib.orm.scenario import Scenario


from stoobly_agent.config.constants import mode, record_policy

@pytest.fixture(scope='module')
def runner():
  return CliRunner()

@pytest.fixture(autouse=True, scope='module')
def settings():
  return reset()

class TestInterceptEnable():

  class TestRecordPolicy():

    class TestScenario():
      @pytest.fixture(scope='class')
      def scenario_name(self):
        return 'Login 1.0.0'

      @pytest.fixture(scope='class', autouse=True)
      def scenario(self, runner: CliRunner, scenario_name: str):
        scenario_create_result = runner.invoke(scenario, ['create', '--without-headers', '--select', 'key', scenario_name])
        assert scenario_create_result.exit_code == 0

        return Scenario.last()

      @pytest.fixture(scope='class', autouse=True)
      def configure(self, runner: CliRunner, scenario: Scenario):
        configure_result = runner.invoke(config, ['scenario', 'set', scenario.key()])
        assert configure_result.exit_code == 0

        configure_result = runner.invoke(intercept, ['configure', '--mode', mode.RECORD ,'--policy', record_policy.OVERWRITE])

      def test_enabling_sets_overwritable(self, runner: CliRunner, scenario: Scenario):
        enable_result = runner.invoke(intercept, ['enable'])
        assert enable_result.exit_code == 0

        assert Scenario.find(scenario.id).overwritable

      def test_disabling_sets_not_overwritable(self, runner: CliRunner, scenario: Scenario):
        Scenario.find(scenario.id).update(overwritable=False)

        enable_result = runner.invoke(intercept, ['disable'])
        assert enable_result.exit_code == 0

        assert not Scenario.find(scenario.id).overwritable