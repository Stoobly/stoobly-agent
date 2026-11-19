import pytest

from click.testing import CliRunner

from stoobly_agent.app.cli.scenario_cli import scenario
from stoobly_agent.lib.orm.scenario import Scenario
from stoobly_agent.test.test_helper import reset

@pytest.fixture(scope='module')
def runner():
  return CliRunner()

@pytest.fixture(autouse=True, scope='module')
def settings():
  return reset()

class TestDelete():

  @pytest.fixture(autouse=True, scope='class')
  @classmethod
  def created_scenario(cls, runner: CliRunner):
    create_result = runner.invoke(scenario, ['create', 'delete-test'])
    assert create_result.exit_code == 0
    return Scenario.last()

  @pytest.fixture(autouse=True, scope='class')
  @classmethod
  def scenario_delete_cli_results(cls, runner: CliRunner, created_scenario: Scenario):
    delete_result = runner.invoke(scenario, ['delete', created_scenario.key()])
    assert delete_result.exit_code == 0
    return delete_result

  def test_it_sets_is_deleted(self, created_scenario: Scenario):
    _scenario = Scenario.find(created_scenario.id)
    assert _scenario and _scenario.is_deleted

  def test_it_prints_moved_to_trash(self, scenario_delete_cli_results):
    assert 'Scenario moved to trash!' in scenario_delete_cli_results.output

  class TestWhenDeletingAgain():

    def test_it_hard_deletes(self, runner: CliRunner, created_scenario: Scenario):
      delete_result = runner.invoke(scenario, ['delete', created_scenario.key()])
      assert delete_result.exit_code == 0
      assert Scenario.find(created_scenario.id) is None
      assert 'Scenario deleted!' in delete_result.output


class TestDeleteWithForce():

  @pytest.fixture(autouse=True, scope='class')
  @classmethod
  def created_scenario(cls, runner: CliRunner):
    create_result = runner.invoke(scenario, ['create', 'delete-force-test'])
    assert create_result.exit_code == 0
    return Scenario.last()

  @pytest.fixture(autouse=True, scope='class')
  @classmethod
  def scenario_delete_cli_results(cls, runner: CliRunner, created_scenario: Scenario):
    delete_result = runner.invoke(scenario, ['delete', '--force', created_scenario.key()])
    assert delete_result.exit_code == 0
    return delete_result

  def test_it_hard_deletes(self, created_scenario: Scenario, scenario_delete_cli_results):
    assert Scenario.find(created_scenario.id) is None
    assert 'Scenario deleted!' in scenario_delete_cli_results.output
