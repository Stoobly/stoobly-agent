from multiprocessing.connection import Client
import pdb
import pytest

from click.testing import CliRunner

from stoobly_agent.test.test_helper import reset

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
    url = 'https://www.google.com/'
    self.__record_request(url)

    request_result = runner.invoke(request, ['list', '--without-headers', '--select', 'key'])
    assert request_result.exit_code == 0

    output = request_result.stdout
    request_key = RequestKey(output.strip())

    _request = Request.find(request_key.id)

    assert _request.url == url

  def test_it_shows_all_requests(self, runner: CliRunner):
    self.__record_request('www.google.com')
    self.__record_request('www.google.com')

    request_result = runner.invoke(request, ['list', '--without-headers', '--select', 'key'])
    assert request_result.exit_code == 0

    output = request_result.stdout
    assert len(output.strip().split("\n")) == 2

  def test_it_shows_requests_on_page(self, runner: CliRunner):
    self.__record_request('www.google.com')
    self.__record_request('www.google.com')

    request_result = runner.invoke(request, ['list', '--without-headers', '--select', 'key', '--page', '2', '--size', '1'])
    assert request_result.exit_code == 0

    output = request_result.stdout
    assert len(output.strip().split("\n")) == 1

  def test_it_sorts_by_host(self, runner: CliRunner):
    self.__record_request('www.google.com')
    url = 'www.facebook.com'
    self.__record_request(url)

    request_result = runner.invoke(request, ['list', '--without-headers', '--select', 'host', '--sort-by', 'host', '--sort-order', 'asc'])
    assert request_result.exit_code == 0

    output = request_result.stdout
    host = output.strip().split("\n")[0]
    assert host == url

  def __record_request(self, url):
    runner = CliRunner()
    record_result = runner.invoke(record, [url])
    assert record_result.exit_code == 0