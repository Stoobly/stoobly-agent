import json
import pdb
import pytest

from click.testing import CliRunner

from stoobly_agent.test.test_helper import DETERMINISTIC_GET_REQUEST_URL, reset

from stoobly_agent.app.cli.helpers.print_service import JSON_FORMAT
from stoobly_agent.cli import record, request
from stoobly_agent.lib.api.keys import RequestKey
from stoobly_agent.lib.orm.request import Request

@pytest.fixture(scope='module')
def runner():
      return CliRunner()

class TestList():

  @pytest.fixture(autouse=True)
  def settings(self):
    return reset()

  def test_it_shows_request(self, runner: CliRunner):
    self.__record_request(runner, DETERMINISTIC_GET_REQUEST_URL)

    request_result = runner.invoke(request, ['list', '--without-headers', '--select', 'key'])
    assert request_result.exit_code == 0

    output = request_result.stdout
    request_key = RequestKey(output.strip())

    _request = Request.find_by(uuid=request_key.id)

    assert _request.url == DETERMINISTIC_GET_REQUEST_URL

  def test_it_shows_all_requests(self, runner: CliRunner):
    self.__record_request(runner, DETERMINISTIC_GET_REQUEST_URL)
    self.__record_request(runner, DETERMINISTIC_GET_REQUEST_URL)

    request_result = runner.invoke(request, ['list', '--without-headers', '--select', 'key'])
    assert request_result.exit_code == 0

    output = request_result.stdout
    assert len(output.strip().split("\n")) == 2

  def test_it_shows_requests_on_page(self, runner: CliRunner):
    self.__record_request(runner, DETERMINISTIC_GET_REQUEST_URL)
    self.__record_request(runner, DETERMINISTIC_GET_REQUEST_URL)

    request_result = runner.invoke(request, ['list', '--without-headers', '--select', 'key', '--page', '2', '--size', '1'])
    assert request_result.exit_code == 0

    output = request_result.stdout
    assert len(output.strip().split("\n")) == 1

  def test_it_sorts_by_host(self, runner: CliRunner):
    self.__record_request(runner, 'https://www.google.com')
    self.__record_request(runner, 'https://www.facebook.com')

    request_result = runner.invoke(request, ['list', '--without-headers', '--select', 'host', '--sort-by', 'host', '--sort-order', 'asc'])
    assert request_result.exit_code == 0

    output = request_result.stdout
    host = output.strip().split("\n")[0]
    assert host == 'www.facebook.com'

  def test_it_formats_json(self, runner: CliRunner):
    self.__record_request(runner, DETERMINISTIC_GET_REQUEST_URL)

    request_result = runner.invoke(request, ['list', '--format', JSON_FORMAT])
    assert request_result.exit_code == 0

    output = request_result.stdout
    requests = json.loads(output)

    assert requests[0].get('status') == '200'

  def __record_request(self, runner: CliRunner, url: str):
    record_result = runner.invoke(record, [url])
    assert record_result.exit_code == 0