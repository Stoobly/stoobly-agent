import pdb
import pytest

from click.testing import CliRunner

from stoobly_agent.test.test_helper import DETERMINISTIC_GET_REQUEST_URL, reset

from stoobly_agent.app.cli.request_cli import request
from stoobly_agent.cli import record
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.lib.orm.scenario import Scenario

@pytest.fixture(scope='module')
def runner():
  return CliRunner()

@pytest.fixture(autouse=True, scope='module')
def settings():
  return reset()

class TestDelete():

  @pytest.fixture(autouse=True, scope='class')
  def request_create_cli_result(self, runner: CliRunner):
    record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
    assert record_result.exit_code == 0
    return record_result

  @pytest.fixture(autouse=True, scope='class')
  def request_delete_cli_results(self, runner: CliRunner):
    _request = Request.last()
    request_delete_result = runner.invoke(request, ['delete', _request.key()])
    assert request_delete_result.exit_code == 0

    return request_delete_result

  def test_it_sets_is_deleted(self):
    request = Request.last()
    assert request and request.is_deleted

  class TestWhenDeletingAgain():

    def test_it_hard_deletes(self, runner):
      _request = Request.last()
      request_delete_result = runner.invoke(request, ['delete', _request.key()])
      assert request_delete_result.exit_code == 0

      assert Request.last() == None


class TestDeleteWhenInScenario():

  @pytest.fixture(autouse=True, scope='class')
  def scenario(self):
    record = Scenario.create(name='delete scenario test')
    yield record
    record.delete()

  @pytest.fixture(autouse=True, scope='class')
  def request_in_scenario(self, runner: CliRunner, scenario: Scenario):
    record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
    assert record_result.exit_code == 0
    _request = Request.last()
    _request.update({'scenario_id': scenario.id})
    return _request

  @pytest.fixture(autouse=True, scope='class')
  def soft_delete(self, runner: CliRunner, request_in_scenario: Request):
    result = runner.invoke(request, ['delete', request_in_scenario.key()])
    assert result.exit_code == 0

  def test_it_clears_scenario_id(self, request_in_scenario: Request):
    refreshed = Request.find(request_in_scenario.id)
    assert refreshed.scenario_id is None

  def test_it_decrements_scenario_requests_count(self, scenario: Scenario):
    refreshed = Scenario.find(scenario.id)
    assert refreshed.requests_count == 0

