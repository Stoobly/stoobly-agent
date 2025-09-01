import os
import pdb
import pytest
import requests
import shutil

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

    @pytest.fixture()
    def public_directory_default_response(self, index_file_path: str, mitmproxy_request: MitmproxyRequest, public_directory: str):
      path = os.path.join(public_directory, 'index')
      shutil.move(index_file_path, path)
      res: requests.Response = eval_fixtures(mitmproxy_request, public_directory_path=public_directory)
      assert res != None
      return res

    def test_it_sets_contents(
      self, public_directory_response: requests.Response, index_file_contents: str
    ):
      assert public_directory_response.raw.read() == index_file_contents

    def test_it_headers(self, public_directory_response: requests.Response):
      assert public_directory_response.headers['Content-Type'] == 'text/html'
    
    def test_it_sets_status_code(self, public_directory_response: requests.Response):
      assert public_directory_response.status_code == 200

    def test_default_it_headers(self, public_directory_default_response: requests.Response):
      assert public_directory_default_response.headers['Content-Type'] == 'application/json'

  class TestMultiplePublicDirectories():
    @pytest.fixture(scope='class')
    def request_method(self):
      return 'GET'

    @pytest.fixture(scope='class')
    def request_url(self):
      return 'https://petstore.swagger.io'
    
    @pytest.fixture(scope='class')
    def api_request_url(self):
      return 'https://api.example.com'
    
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
    
    @pytest.fixture(scope='class')
    def api_created_request(
      self, settings: Settings, request_method: str, api_request_url: str
    ):
      status = RequestBuilder(
        method=request_method,
        request_headers={'accept': 'text/html;q=0.1,application/json;q=0.9'},
        response_body='',
        status_code=200,
        url=api_request_url,
      ).with_settings(settings).build()[1]
      assert status == 200

      return Request.last()

    @pytest.fixture()
    def mitmproxy_request(self, created_request: Request) -> MitmproxyRequest:
      return MitmproxyRequestAdapter(created_request).adapt()
    
    @pytest.fixture()
    def api_mitmproxy_request(self, api_created_request: Request) -> MitmproxyRequest:
      return MitmproxyRequestAdapter(api_created_request).adapt()

    @pytest.fixture(scope='class')
    def main_public_directory(self):
      tmp_dir_path = DataDir.instance().tmp_dir_path
      public_dir_path = os.path.join(tmp_dir_path, 'main_public') 
      if not os.path.exists(public_dir_path):
        os.mkdir(public_dir_path)
      return public_dir_path
    
    @pytest.fixture(scope='class')
    def api_public_directory(self):
      tmp_dir_path = DataDir.instance().tmp_dir_path
      public_dir_path = os.path.join(tmp_dir_path, 'api_public') 
      if not os.path.exists(public_dir_path):
        os.mkdir(public_dir_path)
      return public_dir_path
    
    @pytest.fixture(scope='class')
    def fallback_public_directory(self):
      tmp_dir_path = DataDir.instance().tmp_dir_path
      public_dir_path = os.path.join(tmp_dir_path, 'fallback_public') 
      if not os.path.exists(public_dir_path):
        os.mkdir(public_dir_path)
      return public_dir_path

    @pytest.fixture(scope='class')
    def main_file_contents(self):
      return b'Main Site Content'
    
    @pytest.fixture(scope='class')
    def api_file_contents(self):
      return b'API Documentation'
    
    @pytest.fixture(scope='class')
    def fallback_file_contents(self):
      return b'Fallback Content'

    @pytest.fixture(autouse=True, scope='class')
    def setup_files(self, main_public_directory: str, api_public_directory: str, fallback_public_directory: str,
                   main_file_contents: bytes, api_file_contents: bytes, fallback_file_contents: bytes):
      # Create index.html in main directory
      main_path = os.path.join(main_public_directory, 'index.html')
      with open(main_path, 'wb') as fp:
        fp.write(main_file_contents)
      
      # Create index.html in API directory
      api_path = os.path.join(api_public_directory, 'index.html')
      with open(api_path, 'wb') as fp:
        fp.write(api_file_contents)
      
      # Create index.html in fallback directory
      fallback_path = os.path.join(fallback_public_directory, 'index.html')
      with open(fallback_path, 'wb') as fp:
        fp.write(fallback_file_contents)

    def test_origin_specific_routing(self, api_mitmproxy_request: MitmproxyRequest, 
                                   main_public_directory: str, api_public_directory: str, fallback_public_directory: str,
                                   api_file_contents: bytes):
      """Test that origin-specific paths are used when origin matches."""
      # Multiple paths with origin specification
      public_paths = f"petstore.swagger.io:{main_public_directory},api.example.com:{api_public_directory},{fallback_public_directory}"
      
      res: requests.Response = eval_fixtures(api_mitmproxy_request, public_directory_path=public_paths)
      assert res is not None
      assert res.raw.read() == api_file_contents

    def test_fallback_routing(self, mitmproxy_request: MitmproxyRequest, 
                            main_public_directory: str, api_public_directory: str, fallback_public_directory: str,
                            main_file_contents: bytes):
      """Test that origin-specific paths are used when origin matches."""
      # Multiple paths with origin specification - petstore.swagger.io should match first path
      public_paths = f"petstore.swagger.io:{main_public_directory},api.example.com:{api_public_directory},{fallback_public_directory}"
      
      res: requests.Response = eval_fixtures(mitmproxy_request, public_directory_path=public_paths)
      assert res is not None
      assert res.raw.read() == main_file_contents

    def test_wildcard_origin_matching(self, settings: Settings, main_public_directory: str, api_public_directory: str,
                                    fallback_public_directory: str, api_file_contents: bytes):
      """Test wildcard origin matching (*.example.com)."""
      # Create request for subdomain
      status = RequestBuilder(
        method='GET',
        request_headers={'accept': 'text/html'},
        response_body='',
        status_code=200,
        url='https://sub.example.com',
      ).with_settings(settings).build()[1]
      assert status == 200

      subdomain_request = Request.last()
      subdomain_mitmproxy_request = MitmproxyRequestAdapter(subdomain_request).adapt()
      
      # Use wildcard pattern
      public_paths = f"petstore.swagger.io:{main_public_directory},*.example.com:{api_public_directory},{fallback_public_directory}"
      
      res: requests.Response = eval_fixtures(subdomain_mitmproxy_request, public_directory_path=public_paths)
      assert res is not None
      assert res.raw.read() == api_file_contents

    def test_no_origin_match_uses_fallback(self, settings: Settings, main_public_directory: str, 
                                         api_public_directory: str, fallback_public_directory: str,
                                         fallback_file_contents: bytes):
      """Test that requests with no matching origin use fallback path."""
      # Create request for unmatched origin
      status = RequestBuilder(
        method='GET',
        request_headers={'accept': 'text/html'},
        response_body='',
        status_code=200,
        url='https://unknown.com',
      ).with_settings(settings).build()[1]
      assert status == 200

      unknown_request = Request.last()
      unknown_mitmproxy_request = MitmproxyRequestAdapter(unknown_request).adapt()
      
      public_paths = f"petstore.swagger.io:{main_public_directory},api.example.com:{api_public_directory},{fallback_public_directory}"
      
      res: requests.Response = eval_fixtures(unknown_mitmproxy_request, public_directory_path=public_paths)
      assert res is not None
      assert res.raw.read() == fallback_file_contents

    def test_multiple_fallback_paths(self, settings: Settings, fallback_public_directory: str,
                                   fallback_file_contents: bytes):
      """Test multiple fallback paths (no origin specified)."""
      # Create request for unknown origin
      status = RequestBuilder(
        method='GET',
        request_headers={'accept': 'text/html'},
        response_body='',
        status_code=200,
        url='https://unknown.com',
      ).with_settings(settings).build()[1]
      assert status == 200

      unknown_request = Request.last()
      unknown_mitmproxy_request = MitmproxyRequestAdapter(unknown_request).adapt()
      
      # Multiple fallback paths (no origin specified)
      public_paths = f"/nonexistent/path,{fallback_public_directory}"
      
      res: requests.Response = eval_fixtures(unknown_mitmproxy_request, public_directory_path=public_paths)
      assert res is not None
      assert res.raw.read() == fallback_file_contents