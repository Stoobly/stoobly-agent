import pdb
import pytest

from click.testing import CliRunner

from stoobly_agent.test.test_helper import reset

from stoobly_agent.cli import config, intercept, scenario
from stoobly_agent.lib.orm.scenario import Scenario
from stoobly_agent.app.settings import Settings
from stoobly_agent.lib.api.keys.project_key import ProjectKey

from stoobly_agent.config.constants import mode, record_order, record_strategy, test_strategy

@pytest.fixture(scope='module')
def runner():
  return CliRunner()

@pytest.fixture(autouse=True, scope='module')
def settings():
  return reset()

class TestInterceptConfigure():

  class TestRecordOrder():

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

        configure_result = runner.invoke(intercept, ['configure', '--mode', mode.RECORD ,'--order', record_order.OVERWRITE])
        assert configure_result.exit_code == 0

      class TestChangingOrder():

        def test_scenario_not_overwritable(self, runner: CliRunner, scenario: Scenario):
          Scenario.find(scenario.id).update(overwritable=True)

          configure_result = runner.invoke(intercept, ['configure', '--order', record_order.APPEND])
          assert configure_result.exit_code == 0

          assert not Scenario.find(scenario.id).overwritable

  class TestStrategy():

    class TestRecordStrategy():

      def test_strategy_record_mode_full(self, runner: CliRunner):
        configure_result = runner.invoke(intercept, ['configure', '--mode', mode.RECORD, '--strategy', record_strategy.FULL])
        assert configure_result.exit_code == 0

        settings = Settings.instance()
        project_key = ProjectKey(settings.proxy.intercept.project_key)
        data_rule = settings.proxy.data.data_rules(project_key.id)
        assert data_rule.record_strategy == record_strategy.FULL

      def test_strategy_record_mode_minimal(self, runner: CliRunner):
        configure_result = runner.invoke(intercept, ['configure', '--mode', mode.RECORD, '--strategy', record_strategy.MINIMAL])
        assert configure_result.exit_code == 0

        settings = Settings.instance()
        project_key = ProjectKey(settings.proxy.intercept.project_key)
        data_rule = settings.proxy.data.data_rules(project_key.id)
        assert data_rule.record_strategy == record_strategy.MINIMAL

      def test_strategy_without_mode_record_existing(self, runner: CliRunner):
        runner.invoke(intercept, ['configure', '--mode', mode.RECORD])
        configure_result = runner.invoke(intercept, ['configure', '--strategy', record_strategy.MINIMAL])
        assert configure_result.exit_code == 0

        settings = Settings.instance()
        project_key = ProjectKey(settings.proxy.intercept.project_key)
        data_rule = settings.proxy.data.data_rules(project_key.id)
        assert data_rule.record_strategy == record_strategy.MINIMAL

    class TestTestStrategy():

      def test_strategy_test_mode_contract(self, runner: CliRunner):
        configure_result = runner.invoke(intercept, ['configure', '--mode', mode.TEST, '--strategy', test_strategy.CONTRACT])
        assert configure_result.exit_code == 0

        settings = Settings.instance()
        project_key = ProjectKey(settings.proxy.intercept.project_key)
        data_rule = settings.proxy.data.data_rules(project_key.id)
        assert data_rule.test_strategy == test_strategy.CONTRACT

      def test_strategy_test_mode_diff(self, runner: CliRunner):
        configure_result = runner.invoke(intercept, ['configure', '--mode', mode.TEST, '--strategy', test_strategy.DIFF])
        assert configure_result.exit_code == 0

        settings = Settings.instance()
        project_key = ProjectKey(settings.proxy.intercept.project_key)
        data_rule = settings.proxy.data.data_rules(project_key.id)
        assert data_rule.test_strategy == test_strategy.DIFF

      def test_strategy_without_mode_test_existing(self, runner: CliRunner):
        runner.invoke(intercept, ['configure', '--mode', mode.TEST])
        configure_result = runner.invoke(intercept, ['configure', '--strategy', test_strategy.FUZZY])
        assert configure_result.exit_code == 0

        settings = Settings.instance()
        project_key = ProjectKey(settings.proxy.intercept.project_key)
        data_rule = settings.proxy.data.data_rules(project_key.id)
        assert data_rule.test_strategy == test_strategy.FUZZY

    class TestInvalidInput():
      def test_strategy_mock_mode_error(self, runner: CliRunner):
        configure_result = runner.invoke(intercept, ['configure', '--mode', mode.MOCK, '--strategy', record_strategy.FULL])
        assert configure_result.exit_code == 1
        assert "Error: set --strategy to a intercept mode that supports the strategy option" in configure_result.output

      def test_strategy_replay_mode_error(self, runner: CliRunner):
        configure_result = runner.invoke(intercept, ['configure', '--mode', mode.REPLAY, '--strategy', record_strategy.FULL])
        assert configure_result.exit_code == 1
        assert "Error: set --strategy to a intercept mode that supports the strategy option" in configure_result.output

      def test_strategy_without_mode_unsupported_existing(self, runner: CliRunner):
        runner.invoke(intercept, ['configure', '--mode', mode.MOCK])
        configure_result = runner.invoke(intercept, ['configure', '--strategy', record_strategy.FULL])
        assert configure_result.exit_code == 1
        assert "Error: set --strategy to a intercept mode that supports the strategy option" in configure_result.output
