import os
import pdb
import pytest
import requests

from click.testing import CliRunner
from mitmproxy.http import Request as MitmproxyRequest

from stoobly_agent.test.test_helper import reset

from stoobly_agent.app.models.adapters.orm.request.mitmproxy_adapter import MitmproxyRequestAdapter
from stoobly_agent.app.models.factories.resource.local_db.helpers.request_builder import RequestBuilder
from stoobly_agent.app.proxy.mock.eval_fixtures_service import eval_fixtures
from stoobly_agent.app.proxy.mock.types import Fixtures
from stoobly_agent.app.settings import Settings
from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.lib.orm.request import Request

@pytest.fixture(scope='module')
def runner():
    return CliRunner()

@pytest.fixture(scope='module')
def settings():
  return reset()

class TestEvalFixturesService():
  @pytest.fixture(scope='class')
  def request_method(self):
    return 'POST'

  @pytest.fixture(scope='class')
  def request_url(self):
    return 'https://petstore.swagger.io/index.html'

  @pytest.fixture(scope='class')
  def created_request(
    self, settings: Settings, request_method: str, request_url: str
  ):
    status = RequestBuilder(
      method=request_method,
      response_body='',
      status_code=200,
      url=request_url,
    ).with_settings(settings).build()[1]
    assert status == 200

    return Request.last()

  @pytest.fixture(scope='class')
  def public_directory(self):
    tmp_dir_path = DataDir.instance().tmp_dir_path
    public_dir_path = os.path.join(tmp_dir_path, 'public') 
    if not os.path.exists(public_dir_path):
      os.mkdir(public_dir_path)
    return public_dir_path

  @pytest.fixture(scope='class')
  def index_file_contents(self):
    return b'Hello World!'

  @pytest.fixture(autouse=True, scope='class')
  def index_file_path(self, public_directory: str, index_file_contents: str):
    path = os.path.join(public_directory, 'index.html')
    with open(path, 'wb') as fp:
      fp.write(index_file_contents)
    return path

  @pytest.fixture(scope='class')
  def response_fixtures(self, request_method: str, index_file_path: str) -> Fixtures:
    fixtures = {}
    fixtures[request_method] = {
      '/index.html': {
        'headers': {
          'Content-Length': '1',
        },
        'path': index_file_path,
      }
    }
    return fixtures

  @pytest.fixture()
  def mitmproxy_request(self, created_request: Request) -> MitmproxyRequest:
    return MitmproxyRequestAdapter(created_request).adapt()

  def test_it_evaluates_response_fixture(
    self, mitmproxy_request: MitmproxyRequest, response_fixtures: Fixtures, index_file_contents: str
  ):
    res: requests.Response = eval_fixtures(mitmproxy_request, response_fixtures=response_fixtures)
    assert res
    assert res.raw.read() == index_file_contents
    assert res.headers['Content-Length'] == '1'

  def test_it_evaluates_public_directory(
    self, mitmproxy_request: MitmproxyRequest, public_directory: str, index_file_contents: str
  ):
    res: requests.Response = eval_fixtures(mitmproxy_request, public_directory_path=public_directory)
    assert res
    assert res.raw.read() == index_file_contents