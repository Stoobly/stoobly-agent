import pdb
import pytest

from click.testing import CliRunner

from stoobly_agent.test.test_helper import DETERMINISTIC_GET_REQUEST_URL, reset

from stoobly_agent.cli import record, request
from stoobly_agent.lib.orm.request import Request

@pytest.fixture(scope='module')
def runner():
    return CliRunner()

@pytest.fixture(scope='class', autouse=True)
def settings():
  return reset()

class TestRequestSnapshot():
  @pytest.fixture(scope='class')
  def recorded_request(self, runner: CliRunner):
    record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
    assert record_result.exit_code == 0
    return Request.last()

  @pytest.fixture(scope='class', autouse=True)
  def snapshot_result(self, runner: CliRunner, recorded_request: Request):
    snapshot_result = runner.invoke(request, ['snapshot', recorded_request.key()])
    assert snapshot_result.exit_code == 0
    return snapshot_result

  def test_it_resets(self, runner: CliRunner, recorded_request: Request):
    original_path = recorded_request.path
    recorded_request.update(path='/test')

    snapshot_result = runner.invoke(request, ['reset', recorded_request.key()])
    assert snapshot_result.exit_code == 0

    _request = Request.find(recorded_request.id)
    assert _request.path == original_path