import json
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

class TestResponseGet():

  @pytest.fixture(autouse=True, scope='class')
  def request_create_cli_result(self, runner: CliRunner):
    record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
    assert record_result.exit_code == 0
    return record_result

  def test_it_returns_correct_response(self, runner: CliRunner):
    _request = Request.last()

    request_result = runner.invoke(request, ['response', 'get', _request.key()])
    assert request_result.exit_code == 0

    output = request_result.stdout
    assert type(output) is str
    assert type(output) is not bytes

    # Note: the invoke result's stdout can actually return a string of
    # a byte literal so parse the json for extra validation
    json_response = json.loads(output)
    assert json_response['message'] is not None
    assert json_response['status'] == 'success'

