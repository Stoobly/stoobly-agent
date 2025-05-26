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
  class TestResponseFixtures():
    @pytest.fixture(scope='class')
    def request_method(self):
      return 'POST'

    @pytest.fixture(scope='class')
    def request_url(self):
      return 'https://petstore.swagger.io/404.html'

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
    def not_found_file_contents(self):
      return b'Not Found'

    @pytest.fixture(scope='class')
    def public_directory(self):
      tmp_dir_path = DataDir.instance().tmp_dir_path
      public_dir_path = os.path.join(tmp_dir_path, 'public') 
      if not os.path.exists(public_dir_path):
        os.mkdir(public_dir_path)
      return public_dir_path

    @pytest.fixture(autouse=True, scope='class')
    def not_found_file_path(self, public_directory: str, not_found_file_contents: str):
      path = os.path.join(public_directory, '404.html')
      with open(path, 'wb') as fp:
        fp.write(not_found_file_contents)
      return path

    @pytest.fixture(scope='class')
    def response_fixtures(self, request_method: str, not_found_file_path: str) -> Fixtures:
      fixtures = {}
      fixtures[request_method] = {
        '/404.html': {
          'headers': {
            'test': '1',
          },
          'path': not_found_file_path,
          'status_code': 404,
        }
      }
      return fixtures

    @pytest.fixture()
    def mitmproxy_request(self, created_request: Request) -> MitmproxyRequest:
      return MitmproxyRequestAdapter(created_request).adapt()

    @pytest.fixture()
    def fixtures_response(self, mitmproxy_request: MitmproxyRequest, response_fixtures: Fixtures):
      res: requests.Response = eval_fixtures(mitmproxy_request, response_fixtures=response_fixtures)
      assert res != None
      return res

    def test_it_sets_response(
      self, fixtures_response: requests.Response, not_found_file_contents: str
    ):
      assert fixtures_response.raw.read() == not_found_file_contents

    def test_it_sets_headers(self, fixtures_response: requests.Response):
      assert fixtures_response.headers['test'] == '1'
      assert fixtures_response.headers['Content-Type'] == 'text/html'

    def test_it_sets_status_code(self,  fixtures_response: requests.Response):
      assert fixtures_response.status_code == 404

  class TestPublicDirectory():
    @pytest.fixture(scope='class')
    def request_method(self):
      return 'GET'

    @pytest.fixture(scope='class')
    def request_url(self):
      return 'https://petstore.swagger.io'

    @pytest.fixture(scope='class')
    def created_request(
      self, settings: Settings, request_method: str, request_url: str
    ):
      status = RequestBuilder(
        method=request_method,
        request_headers={'accept': 'text/html;q=0.1,application/json;q=0.9'},
        response_body='',
        status_code=200,
        url=request_url,
      ).with_settings(settings).build()[1]
      assert status == 200

      return Request.last()

    @pytest.fixture()
    def mitmproxy_request(self, created_request: Request) -> MitmproxyRequest:
      return MitmproxyRequestAdapter(created_request).adapt()

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

    @pytest.fixture()
    def public_directory_response(self, mitmproxy_request: MitmproxyRequest, public_directory: str):
      res: requests.Response = eval_fixtures(mitmproxy_request, public_directory_path=public_directory)
      assert res != None
      return res

    def test_it_sets_contents(
      self, public_directory_response: requests.Response, index_file_contents: str
    ):
      assert public_directory_response.raw.read() == index_file_contents

    def test_it_headers(self, public_directory_response: requests.Response):
      assert public_directory_response.headers['Content-Type'] == 'text/html'
    
    def test_it_sets_status_code(self,  public_directory_response: requests.Response):
      assert public_directory_response.status_code == 200