import pdb
import pytest

from click.testing import CliRunner

from stoobly_agent.test.test_helper import DETERMINISTIC_GET_REQUEST_URL, NON_DETERMINISTIC_GET_REQUEST_URL, reset

from stoobly_agent.app.cli.scenario_cli import scenario
from stoobly_agent.cli import record
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.lib.orm.scenario import Scenario

@pytest.fixture(scope='module')
def runner():
    return CliRunner()

@pytest.fixture(scope='class', autouse=True)
def settings():
  return reset()

class TestRequest():
  @pytest.fixture(scope='class')
  @classmethod
  def created_scenario(cls, runner: CliRunner):
      create_result = runner.invoke(scenario, ['create', 'test'])
      assert create_result.exit_code == 0
      return Scenario.last()

  @pytest.fixture(scope='class', autouse=True)
  @classmethod
  def recorded_request_one(cls, runner: CliRunner, created_scenario: Scenario):
      record_result = runner.invoke(record, ['--scenario-key', created_scenario.key(), DETERMINISTIC_GET_REQUEST_URL])
      assert record_result.exit_code == 0
      return Request.last()

  @pytest.fixture(scope='class', autouse=True)
  @classmethod
  def recorded_request_two(cls, runner: CliRunner, created_scenario: Scenario):
      record_result = runner.invoke(record, ['--scenario-key', created_scenario.key(), NON_DETERMINISTIC_GET_REQUEST_URL])
      assert record_result.exit_code == 0
      return Request.last()

  @pytest.fixture(scope='class', autouse=True)
  @classmethod
  def snapshot_result(cls, runner: CliRunner, created_scenario: Scenario):
    snapshot_result = runner.invoke(scenario, ['snapshot', 'create', created_scenario.key()])
    assert snapshot_result.exit_code == 0
    return snapshot_result

  def test_it_resets(self, runner: CliRunner, created_scenario: Scenario):
    requests = created_scenario.requests
    assert len(requests) == 2

    requests[1].delete()

    snapshot_result = runner.invoke(scenario, ['snapshot', 'reset', created_scenario.key()])
    assert snapshot_result.exit_code == 0

    requests = Scenario.find(created_scenario.id).requests
    assert len(requests) == 2