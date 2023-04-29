import pdb
import pytest

from click.testing import CliRunner

from stoobly_agent.test.test_helper import DETERMINISTIC_GET_REQUEST_URL, reset

from stoobly_agent.cli import record, request
from stoobly_agent.lib.orm.request import Request

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

