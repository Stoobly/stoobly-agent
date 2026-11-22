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

class TestUpdate():

  @pytest.fixture(autouse=True, scope='class')
  @classmethod
  def created_scenario(cls, runner: CliRunner):
    create_result = runner.invoke(scenario, [
      'create', '--description', 'original description', 'update-test'
    ])
    assert create_result.exit_code == 0
    return Scenario.last()

  def test_it_updates_name(self, runner: CliRunner, created_scenario: Scenario):
    update_result = runner.invoke(scenario, [
      'update', '--name', 'update-test-renamed', created_scenario.key()
    ])
    assert update_result.exit_code == 0

    _scenario = Scenario.find(created_scenario.id)
    assert _scenario.name == 'update-test-renamed'
    assert _scenario.description == 'original description'

  def test_it_updates_description(self, runner: CliRunner, created_scenario: Scenario):
    update_result = runner.invoke(scenario, [
      'update', '--description', 'updated description', created_scenario.key()
    ])
    assert update_result.exit_code == 0

    _scenario = Scenario.find(created_scenario.id)
    assert _scenario.description == 'updated description'

  def test_it_requires_an_update_option(self, runner: CliRunner, created_scenario: Scenario):
    update_result = runner.invoke(scenario, ['update', created_scenario.key()])
    assert update_result.exit_code == 1
    assert 'At least one update option is required' in update_result.output
