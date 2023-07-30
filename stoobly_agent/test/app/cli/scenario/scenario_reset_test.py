import pdb
import pytest

from click.testing import CliRunner

from stoobly_agent.test.test_helper import DETERMINISTIC_GET_REQUEST_URL, NON_DETERMINISTIC_GET_REQUEST_URL, reset

from stoobly_agent.cli import record, scenario
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
  def created_scenario(self, runner: CliRunner):
      create_result = runner.invoke(scenario, ['create', 'test'])
      assert create_result.exit_code == 0
      return Scenario.last()

  @pytest.fixture(scope='class', autouse=True)
  def recorded_request_one(self, runner: CliRunner, created_scenario: Scenario):
      record_result = runner.invoke(record, ['--scenario-key', created_scenario.key(), DETERMINISTIC_GET_REQUEST_URL])
      assert record_result.exit_code == 0
      return Request.last()

  @pytest.fixture(scope='class', autouse=True)
  def recorded_request_two(self, runner: CliRunner, created_scenario: Scenario):
      record_result = runner.invoke(record, ['--scenario-key', created_scenario.key(), NON_DETERMINISTIC_GET_REQUEST_URL])
      assert record_result.exit_code == 0
      return Request.last()

  @pytest.fixture(scope='class', autouse=True)
  def snapshot_result(self, runner: CliRunner, created_scenario: Scenario):
    snapshot_result = runner.invoke(scenario, ['snapshot', created_scenario.key()])
    assert snapshot_result.exit_code == 0
    return snapshot_result

  def test_it_resets(self, runner: CliRunner, created_scenario: Scenario):
    requests = created_scenario.requests
    assert len(requests) == 2

    requests[1].delete()

    snapshot_result = runner.invoke(scenario, ['reset', created_scenario.key()])
    assert snapshot_result.exit_code == 0

    requests = Scenario.find(created_scenario.id).requests
    assert len(requests) == 2