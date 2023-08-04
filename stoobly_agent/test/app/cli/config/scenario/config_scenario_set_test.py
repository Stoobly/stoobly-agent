import pdb
import pytest

from click.testing import CliRunner

from stoobly_agent.test.test_helper import DETERMINISTIC_GET_REQUEST_URL, reset

from stoobly_agent.app.settings import Settings
from stoobly_agent.cli import config, record, scenario
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.lib.orm.scenario import Scenario
from stoobly_agent.config.constants import record_policy

from stoobly_agent.lib.api.keys import ProjectKey

@pytest.fixture(scope='module')
def runner():
    return CliRunner()

class TestConfigScenarioSet():

  @pytest.fixture(scope='class', autouse=True)
  def settings(self):
    return reset()

  class TestWhenRecordPolicyOverwrite():
    @pytest.fixture(scope='class')
    def created_scenario(self, runner: CliRunner):
      scenario_create_result = runner.invoke(scenario, ['create', 'test'])
      assert scenario_create_result.exit_code == 0
      _scenario = Scenario.last()
      _scenario.update(overwritable=True)
      return _scenario

    @pytest.fixture(scope='class')
    def recorded_request(self, runner: CliRunner, created_scenario: Scenario):
        record_result = runner.invoke(record, ['--scenario-key', created_scenario.key(), DETERMINISTIC_GET_REQUEST_URL])
        assert record_result.exit_code == 0
        return Request.last()

    @pytest.fixture(scope='class')
    def new_scenario(self, runner: CliRunner):
      scenario_create_result = runner.invoke(scenario, ['create', 'test'])
      assert scenario_create_result.exit_code == 0

      return Scenario.last() 

    @pytest.fixture(scope='class', autouse=True)
    def change_scenario_results(self, runner: CliRunner, settings: Settings, created_scenario: Scenario, new_scenario: Scenario):
      project_key = settings.proxy.intercept.project_key
      _project_key = ProjectKey(project_key)

      data_rule = settings.proxy.data.data_rules(_project_key.id)
      data_rule.scenario_key = created_scenario.key()
      data_rule.record_policy = record_policy.OVERWRITE
      settings.commit()

      set_results = runner.invoke(config, ['scenario', 'set', new_scenario.key()])
      assert set_results.exit_code == 0

    def test_it_sets_new_scenario_overwritable(self, new_scenario: Scenario):
      _new_scenario = Scenario.find(new_scenario.id)
      assert _new_scenario.overwritable

    def test_it_sets_old_scenario_not_overwritable(self, created_scenario: Scenario):
      _created_scenario = Scenario.find(created_scenario.id)
      assert not _created_scenario.overwritable