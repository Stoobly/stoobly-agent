import json
import os
import pdb
import pytest
import requests
import shutil
import yaml

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
    def default_file_contents(self):
      return b'Default'

    @pytest.fixture(scope='class')
    def not_found_file_contents(self):
      return b'Not Found'

    @pytest.fixture(scope='class')
    def user_file_contents(self):
      return b'{"id": 1, "name": "John Doe"}'

    @pytest.fixture(scope='class')
    def public_directory(self):
      tmp_dir_path = DataDir.instance().tmp_dir_path
      public_dir_path = os.path.join(tmp_dir_path, 'public') 
      if not os.path.exists(public_dir_path):
        os.mkdir(public_dir_path)
      return public_dir_path

    @pytest.fixture(autouse=True, scope='class')
    def not_found_file_path(self, public_directory: str, not_found_file_contents: bytes):
      path = os.path.join(public_directory, '404.html')
      with open(path, 'wb') as fp:
        fp.write(not_found_file_contents)
      return path

    @pytest.fixture(autouse=True, scope='class')
    def user_file_path(self, public_directory: str, user_file_contents: bytes):
      path = os.path.join(public_directory, 'user.json')
      with open(path, 'wb') as fp:
        fp.write(user_file_contents)
      return path

    @pytest.fixture(autouse=True, scope='class')
    def default_file_path(self, public_directory: str, default_file_contents: bytes):
      path = os.path.join(public_directory, 'index.html')
      with open(path, 'wb') as fp:
        fp.write(default_file_contents)
      return path

    @pytest.fixture(scope='class')
    def response_fixtures(self, public_directory: str, request_method: str, not_found_file_path: str) -> Fixtures:
      fixtures = {}
      fixtures[request_method] = {
        '/404.html': {
          'headers': {
            'test': '1',
          },
          'path': not_found_file_path,
          'status_code': 404,
        },
        '/.*?': {
          'path': public_directory
        }
      }
      return fixtures

    @pytest.fixture()
    def mitmproxy_request(self, created_request: Request) -> MitmproxyRequest:
      return MitmproxyRequestAdapter(created_request).adapt()

    @pytest.fixture()
    def fixtures_response(self, mitmproxy_request: MitmproxyRequest, response_fixtures: Fixtures):
      # Convert response_fixtures to a temporary YAML file
      tmp_dir_path = DataDir.instance().tmp_dir_path
      fixtures_file = os.path.join(tmp_dir_path, 'test_response_fixtures.yml')
      
      with open(fixtures_file, 'w') as f:
        yaml.dump(response_fixtures, f, sort_keys=False)

      res: requests.Response = eval_fixtures(mitmproxy_request, response_fixtures_path=fixtures_file)
      assert res != None
      return res

    @pytest.fixture()
    def default_fixtures_response(self, mitmproxy_request: MitmproxyRequest, response_fixtures: Fixtures):
      mitmproxy_request.path = '/'
      mitmproxy_request.headers['accept'] = '*/*'

      res: requests.Response = eval_fixtures(mitmproxy_request, response_fixtures=response_fixtures)
      assert res != None
      return res

    @pytest.fixture()
    def user_fixtures_response(self, mitmproxy_request: MitmproxyRequest, response_fixtures: Fixtures):
      mitmproxy_request.path = '/user.json'
      mitmproxy_request.headers['accept'] = 'application/json'
      res: requests.Response = eval_fixtures(mitmproxy_request, response_fixtures=response_fixtures)
      assert res != None
      return res

    def test_it_sets_response(
      self, fixtures_response: requests.Response, not_found_file_contents: bytes
    ):
      assert fixtures_response.raw.read() == not_found_file_contents

    def test_it_sets_headers(self, fixtures_response: requests.Response):
      assert fixtures_response.headers['test'] == '1'
      assert fixtures_response.headers['Content-Type'] == 'text/html'

    def test_it_sets_status_code(self,  fixtures_response: requests.Response):
      assert fixtures_response.status_code == 404

    def test_fixture_directory(self, default_fixtures_response: requests.Response, default_file_contents: bytes):
      assert default_fixtures_response.raw.read() == default_file_contents

    def test_it_sets_user_response(self, user_fixtures_response: requests.Response, user_file_contents: bytes):
      assert user_fixtures_response.raw.read() == user_file_contents

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
      public_paths = f"{main_public_directory}:https://petstore\\.swagger\\.io,{api_public_directory}:https://api\\.example\\.com,{fallback_public_directory}"
      
      res: requests.Response = eval_fixtures(api_mitmproxy_request, public_directory_path=public_paths)
      assert res is not None
      assert res.raw.read() == api_file_contents

    def test_fallback_routing(self, mitmproxy_request: MitmproxyRequest, 
                            main_public_directory: str, api_public_directory: str, fallback_public_directory: str,
                            main_file_contents: bytes):
      """Test that origin-specific paths are used when origin matches."""
      # Multiple paths with origin specification - https://petstore.swagger.io should match first path
      public_paths = f"{main_public_directory}:https://petstore\\.swagger\\.io,{api_public_directory}:https://api\\.example\\.com,{fallback_public_directory}"
      
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
      
      # Use regex wildcard pattern
      public_paths = f"{main_public_directory}:https://petstore\\.swagger\\.io,{api_public_directory}:https://.*\\.example\\.com,{fallback_public_directory}"
      
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
      
      public_paths = f"{main_public_directory}:https://petstore\\.swagger\\.io,{api_public_directory}:https://api\\.example\\.com,{fallback_public_directory}"
      
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

    def test_full_url_origin_parsing_public_directories(self, settings: Settings):
      """Test parsing of full URL origins (scheme://hostname:port) for public directories."""
      # Create test directories
      tmp_dir_path = DataDir.instance().tmp_dir_path
      api_dir = os.path.join(tmp_dir_path, 'full_url_api')
      fallback_dir = os.path.join(tmp_dir_path, 'full_url_fallback')
      os.makedirs(api_dir, exist_ok=True)
      os.makedirs(fallback_dir, exist_ok=True)
      
      # Create test files
      api_file = os.path.join(api_dir, 'index.html')
      fallback_file = os.path.join(fallback_dir, 'index.html')
      
      with open(api_file, 'w') as f:
        f.write('API Content')
      with open(fallback_file, 'w') as f:
        f.write('Fallback Content')
      
      # Test full URL with port
      status = RequestBuilder(
        method='GET',
        request_headers={'accept': 'text/html'},
        response_body='',
        status_code=200,
        url='https://api.example.com:8080/',
      ).with_settings(settings).build()[1]
      assert status == 200
      
      request = Request.last()
      mitmproxy_request = MitmproxyRequestAdapter(request).adapt()
      
      # Test with regex pattern for scheme:hostname:port (request origin is https://api.example.com:8080)
      public_paths = f"{api_dir}:https://api\\.example\\.com:8080,{fallback_dir}"
      
      res: requests.Response = eval_fixtures(mitmproxy_request, public_directory_path=public_paths)
      assert res is not None
      assert res.raw.read() == b'API Content'

    def test_hostname_port_origin_parsing_public_directories(self, settings: Settings):
      """Test parsing of hostname:port origins for public directories."""
      # Create test directories
      tmp_dir_path = DataDir.instance().tmp_dir_path
      api_dir = os.path.join(tmp_dir_path, 'hostname_port_api')
      fallback_dir = os.path.join(tmp_dir_path, 'hostname_port_fallback')
      os.makedirs(api_dir, exist_ok=True)
      os.makedirs(fallback_dir, exist_ok=True)
      
      # Create test files
      api_file = os.path.join(api_dir, 'index.html')
      fallback_file = os.path.join(fallback_dir, 'index.html')
      
      with open(api_file, 'w') as f:
        f.write('Hostname Port Content')
      with open(fallback_file, 'w') as f:
        f.write('Fallback Content')
      
      # Test hostname:port format
      status = RequestBuilder(
        method='GET',
        request_headers={'accept': 'text/html'},
        response_body='',
        status_code=200,
        url='https://api.example.com:9000/',
      ).with_settings(settings).build()[1]
      assert status == 200
      
      request = Request.last()
      mitmproxy_request = MitmproxyRequestAdapter(request).adapt()
      
      # Test with scheme:hostname:port origin format
      public_paths = f"{api_dir}:https://api\\.example\\.com:9000,{fallback_dir}"
      
      res: requests.Response = eval_fixtures(mitmproxy_request, public_directory_path=public_paths)
      assert res is not None
      assert res.raw.read() == b'Hostname Port Content'

  class TestErrorHandling():
    """Test error handling and edge cases."""
    
    @pytest.fixture(scope='class')
    def request_method(self):
      return 'GET'

    @pytest.fixture(scope='class')
    def request_url(self):
      return 'https://example.com/test'
    
    @pytest.fixture(scope='class')
    def created_request(self, settings: Settings, request_method: str, request_url: str):
      status = RequestBuilder(
        method=request_method,
        request_headers={'accept': 'application/json'},
        response_body='',
        status_code=200,
        url=request_url,
      ).with_settings(settings).build()[1]
      assert status == 200
      return Request.last()

    @pytest.fixture()
    def mitmproxy_request(self, created_request: Request) -> MitmproxyRequest:
      return MitmproxyRequestAdapter(created_request).adapt()

    def test_missing_path_pattern_in_fixture(self, mitmproxy_request: MitmproxyRequest):
      """Test fixture without path_pattern key - should handle KeyError gracefully."""
      # Create fixture without path_pattern
      fixture_without_pattern = {
        'GET': {
          '/test': {
            'path': '/tmp/nonexistent_dir'  # Directory that doesn't exist
          }
        }
      }
      
      # This should not raise a KeyError when accessing fixture['path_pattern']
      res = eval_fixtures(mitmproxy_request, response_fixtures=fixture_without_pattern)
      # Should return None since directory doesn't exist
      assert res is None

    def test_nonexistent_fixture_file(self, mitmproxy_request: MitmproxyRequest):
      """Test fixture pointing to nonexistent file."""
      fixture = {
        'GET': {
          '/test': {
            'path': '/tmp/nonexistent_file.json'
          }
        }
      }
      
      res = eval_fixtures(mitmproxy_request, response_fixtures=fixture)
      assert res is None

    def test_nonexistent_public_directory(self, mitmproxy_request: MitmproxyRequest):
      """Test public directory that doesn't exist."""
      res = eval_fixtures(mitmproxy_request, public_directory_path='/tmp/nonexistent_directory')
      assert res is None

    def test_invalid_yaml_in_response_fixtures_path(self, mitmproxy_request: MitmproxyRequest):
      """Test handling of invalid YAML in response fixtures file."""
      tmp_dir_path = DataDir.instance().tmp_dir_path
      invalid_yaml_file = os.path.join(tmp_dir_path, 'invalid.yml')
      
      # Create file with invalid YAML
      with open(invalid_yaml_file, 'w') as f:
        f.write('invalid: yaml: content: [')
      
      res = eval_fixtures(mitmproxy_request, response_fixtures_path=invalid_yaml_file)
      assert res is None

    def test_empty_response_fixtures(self, mitmproxy_request: MitmproxyRequest):
      """Test with empty response fixtures."""
      res = eval_fixtures(mitmproxy_request, response_fixtures={})
      assert res is None

    def test_none_response_fixtures(self, mitmproxy_request: MitmproxyRequest):
      """Test with None response fixtures."""
      res = eval_fixtures(mitmproxy_request, response_fixtures=None)
      assert res is None

    def test_malformed_fixture_structure(self, mitmproxy_request: MitmproxyRequest):
      """Test fixture with malformed structure."""
      malformed_fixture = {
        'GET': 'not_a_dict'  # Should be a dict
      }
      
      res = eval_fixtures(mitmproxy_request, response_fixtures=malformed_fixture)
      assert res is None

    def test_fixture_without_path(self, mitmproxy_request: MitmproxyRequest):
      """Test fixture without path key."""
      fixture_without_path = {
        'GET': {
          '/test': {
            'status_code': 200
            # Missing 'path' key
          }
        }
      }
      
      res = eval_fixtures(mitmproxy_request, response_fixtures=fixture_without_path)
      assert res is None

    def test_directory_fixture_without_matching_subpath(self, mitmproxy_request: MitmproxyRequest):
      """Test directory fixture when no matching subpath file exists."""
      tmp_dir_path = DataDir.instance().tmp_dir_path
      test_dir = os.path.join(tmp_dir_path, 'test_dir')
      os.makedirs(test_dir, exist_ok=True)
      
      # Don't create any files in the directory
      
      fixture = {
        'GET': {
          '/test': {
            'path': test_dir
          }
        }
      }
      
      res = eval_fixtures(mitmproxy_request, response_fixtures=fixture)
      assert res is None

  class TestCustomHeaders():
    """Test custom header handling."""
    
    @pytest.fixture(scope='class')
    def request_method(self):
      return 'GET'

    @pytest.fixture(scope='class')
    def request_url(self):
      return 'https://example.com/test'
    
    @pytest.fixture(scope='class')
    def test_file_contents(self):
      return b'Test content'

    @pytest.fixture(scope='class')
    def test_file_path(self, test_file_contents: bytes):
      tmp_dir_path = DataDir.instance().tmp_dir_path
      file_path = os.path.join(tmp_dir_path, 'custom_headers_test.txt')
      with open(file_path, 'wb') as f:
        f.write(test_file_contents)
      return file_path
    
    @pytest.fixture(scope='class')
    def created_request(self, settings: Settings, request_method: str, request_url: str):
      from stoobly_agent.config.constants.custom_headers import MOCK_FIXTURE_PATH
      status = RequestBuilder(
        method=request_method,
        request_headers={MOCK_FIXTURE_PATH: '/custom/path'},
        response_body='',
        status_code=200,
        url=request_url,
      ).with_settings(settings).build()[1]
      assert status == 200
      return Request.last()

    @pytest.fixture()
    def mitmproxy_request(self, created_request: Request, test_file_path: str) -> MitmproxyRequest:
      from stoobly_agent.config.constants.custom_headers import MOCK_FIXTURE_PATH
      request = MitmproxyRequestAdapter(created_request).adapt()
      # Override the custom header to point to our test file
      request.headers[MOCK_FIXTURE_PATH] = test_file_path
      return request

    def test_custom_fixture_path_header(self, mitmproxy_request: MitmproxyRequest, test_file_contents: bytes):
      """Test fixture path specified via custom header."""
      res = eval_fixtures(mitmproxy_request)
      assert res is not None
      assert res.raw.read() == test_file_contents

    def test_custom_fixture_path_header_nonexistent_file(self, mitmproxy_request: MitmproxyRequest):
      """Test custom fixture path header pointing to nonexistent file."""
      from stoobly_agent.config.constants.custom_headers import MOCK_FIXTURE_PATH
      mitmproxy_request.headers[MOCK_FIXTURE_PATH] = '/tmp/nonexistent_file.txt'
      
      res = eval_fixtures(mitmproxy_request)
      assert res is None

  class TestContentTypeGuessing():
    """Test content type guessing and file extension handling."""
    
    @pytest.fixture(scope='class')
    def request_method(self):
      return 'GET'

    @pytest.fixture(scope='class')
    def request_url(self):
      return 'https://example.com/api/data'
    
    @pytest.fixture(scope='class')
    def created_request(self, settings: Settings, request_method: str, request_url: str):
      status = RequestBuilder(
        method=request_method,
        request_headers={'accept': 'application/json,text/html;q=0.9,*/*;q=0.8'},
        response_body='',
        status_code=200,
        url=request_url,
      ).with_settings(settings).build()[1]
      assert status == 200
      return Request.last()

    @pytest.fixture()
    def mitmproxy_request(self, created_request: Request) -> MitmproxyRequest:
      return MitmproxyRequestAdapter(created_request).adapt()

    def test_json_file_content_type(self, mitmproxy_request: MitmproxyRequest):
      """Test that JSON files get correct content type."""
      tmp_dir_path = DataDir.instance().tmp_dir_path
      json_file = os.path.join(tmp_dir_path, 'test.json')
      
      with open(json_file, 'w') as f:
        json.dump({'test': 'data'}, f)
      
      fixture = {
        'GET': {
          '/api/data': {
            'path': json_file
          }
        }
      }
      
      res = eval_fixtures(mitmproxy_request, response_fixtures=fixture)
      assert res is not None
      assert res.headers.get('content-type') == 'application/json'

    def test_html_file_content_type(self, mitmproxy_request: MitmproxyRequest):
      """Test that HTML files get correct content type."""
      tmp_dir_path = DataDir.instance().tmp_dir_path
      html_file = os.path.join(tmp_dir_path, 'test.html')
      
      with open(html_file, 'w') as f:
        f.write('<html><body>Test</body></html>')
      
      fixture = {
        'GET': {
          '/api/data': {
            'path': html_file
          }
        }
      }
      
      res = eval_fixtures(mitmproxy_request, response_fixtures=fixture)
      assert res is not None
      assert res.headers.get('content-type') == 'text/html'

    def test_unknown_extension_uses_accept_header(self, mitmproxy_request: MitmproxyRequest):
      """Test that files with unknown extensions use accept header for content type."""
      tmp_dir_path = DataDir.instance().tmp_dir_path
      unknown_file = os.path.join(tmp_dir_path, 'test.unknown')
      
      with open(unknown_file, 'w') as f:
        f.write('test content')
      
      fixture = {
        'GET': {
          '/api/data': {
            'path': unknown_file
          }
        }
      }
      
      res = eval_fixtures(mitmproxy_request, response_fixtures=fixture)
      assert res is not None
      # Should use highest priority from accept header (application/json)
      assert res.headers.get('content-type') == 'application/json'

    def test_wildcard_accept_header_defaults(self, mitmproxy_request: MitmproxyRequest):
      """Test that wildcard accept header gets reasonable defaults."""
      tmp_dir_path = DataDir.instance().tmp_dir_path
      test_file = os.path.join(tmp_dir_path, 'test_wildcard')
      
      with open(test_file, 'w') as f:
        f.write('test content')
      
      # Set accept header to */*
      mitmproxy_request.headers['accept'] = '*/*'
      
      fixture = {
        'GET': {
          '/api/data': {
            'path': test_file
          }
        }
      }
      
      res = eval_fixtures(mitmproxy_request, response_fixtures=fixture)
      assert res is not None
      # Should default to text/html based on the wildcard handling
      assert res.headers.get('content-type') == 'text/plain'

  class TestRegexPatternMatching():
    """Test regex pattern matching for fixture routes."""
    
    @pytest.fixture(scope='class')
    def request_method(self):
      return 'GET'

    @pytest.fixture(scope='class')
    def request_url(self):
      return 'https://example.com/api/users/123'
    
    @pytest.fixture(scope='class')
    def test_file_contents(self):
      return b'User 123 data'

    @pytest.fixture(scope='class')
    def test_file_path(self, test_file_contents: bytes):
      tmp_dir_path = DataDir.instance().tmp_dir_path
      file_path = os.path.join(tmp_dir_path, 'user_data.json')
      with open(file_path, 'wb') as f:
        f.write(test_file_contents)
      return file_path
    
    @pytest.fixture(scope='class')
    def created_request(self, settings: Settings, request_method: str, request_url: str):
      status = RequestBuilder(
        method=request_method,
        request_headers={'accept': 'application/json'},
        response_body='',
        status_code=200,
        url=request_url,
      ).with_settings(settings).build()[1]
      assert status == 200
      return Request.last()

    @pytest.fixture()
    def mitmproxy_request(self, created_request: Request) -> MitmproxyRequest:
      return MitmproxyRequestAdapter(created_request).adapt()

    def test_regex_pattern_matching(self, mitmproxy_request: MitmproxyRequest, test_file_path: str, test_file_contents: bytes):
      """Test that regex patterns work for matching routes."""
      fixture = {
        'GET': {
          r'/api/users/\d+': {  # Regex pattern to match user IDs
            'path': test_file_path
          }
        }
      }
      
      res = eval_fixtures(mitmproxy_request, response_fixtures=fixture)
      assert res is not None
      assert res.raw.read() == test_file_contents

    def test_exact_path_matching(self, mitmproxy_request: MitmproxyRequest, test_file_path: str, test_file_contents: bytes):
      """Test exact path matching."""
      fixture = {
        'GET': {
          '/api/users/123': {  # Exact path match
            'path': test_file_path
          }
        }
      }
      
      res = eval_fixtures(mitmproxy_request, response_fixtures=fixture)
      assert res is not None
      assert res.raw.read() == test_file_contents

    def test_non_matching_pattern(self, mitmproxy_request: MitmproxyRequest, test_file_path: str):
      """Test that non-matching patterns return None."""
      fixture = {
        'GET': {
          r'/api/posts/\d+': {  # Different pattern that shouldn't match
            'path': test_file_path
          }
        }
      }
      
      res = eval_fixtures(mitmproxy_request, response_fixtures=fixture)
      assert res is None

    def test_multiple_patterns_first_match_wins(self, mitmproxy_request: MitmproxyRequest, test_file_path: str):
      """Test that first matching pattern is used."""
      tmp_dir_path = DataDir.instance().tmp_dir_path
      second_file = os.path.join(tmp_dir_path, 'second_file.json')
      with open(second_file, 'w') as f:
        f.write('Second file content')
      
      fixture = {
        'GET': {
          r'/api/users/\d+': {  # First pattern - should match
            'path': test_file_path
          },
          r'/api/.*': {  # Second pattern - also matches but shouldn't be used
            'path': second_file
          }
        }
      }
      
      res = eval_fixtures(mitmproxy_request, response_fixtures=fixture)
      assert res is not None
      # Should use first matching pattern
      assert res.raw.read() == b'User 123 data'

  class TestMultipleResponseFixtures():
    @pytest.fixture(scope='class')
    def request_method(self):
      return 'GET'

    @pytest.fixture(scope='class')
    def api_request_url(self):
      return 'https://api.example.com/users'
    
    @pytest.fixture(scope='class')
    def main_request_url(self):
      return 'https://petstore.swagger.io/users'
    
    @pytest.fixture(scope='class')
    def api_created_request(self, settings: Settings, request_method: str, api_request_url: str):
      status = RequestBuilder(
        method=request_method,
        request_headers={'accept': 'application/json'},
        response_body='',
        status_code=200,
        url=api_request_url,
      ).with_settings(settings).build()[1]
      assert status == 200
      return Request.last()
    
    @pytest.fixture(scope='class')
    def main_created_request(self, settings: Settings, request_method: str, main_request_url: str):
      status = RequestBuilder(
        method=request_method,
        request_headers={'accept': 'application/json'},
        response_body='',
        status_code=200,
        url=main_request_url,
      ).with_settings(settings).build()[1]
      assert status == 200
      return Request.last()

    @pytest.fixture()
    def api_mitmproxy_request(self, api_created_request: Request) -> MitmproxyRequest:
      return MitmproxyRequestAdapter(api_created_request).adapt()
    
    @pytest.fixture()
    def main_mitmproxy_request(self, main_created_request: Request) -> MitmproxyRequest:
      return MitmproxyRequestAdapter(main_created_request).adapt()

    @pytest.fixture(scope='class')
    def api_fixture_file_path(self):
      tmp_dir_path = DataDir.instance().tmp_dir_path
      file_path = os.path.join(tmp_dir_path, 'api_users.json')
      with open(file_path, 'w') as fp:
        json.dump({"users": [{"id": 1, "name": "API User"}]}, fp)
      return file_path
    
    @pytest.fixture(scope='class')
    def main_fixture_file_path(self):
      tmp_dir_path = DataDir.instance().tmp_dir_path
      file_path = os.path.join(tmp_dir_path, 'main_users.json')
      with open(file_path, 'w') as fp:
        json.dump({"users": [{"id": 1, "name": "Main User"}]}, fp)
      return file_path
    
    @pytest.fixture(scope='class')
    def fallback_fixture_file_path(self):
      tmp_dir_path = DataDir.instance().tmp_dir_path
      file_path = os.path.join(tmp_dir_path, 'fallback_users.json')
      with open(file_path, 'w') as fp:
        json.dump({"users": [{"id": 1, "name": "Fallback User"}]}, fp)
      return file_path

    @pytest.fixture(scope='class')
    def origin_specific_fixtures(self, api_fixture_file_path: str, main_fixture_file_path: str):
      """Response fixtures with origin-specific routing."""
      return {
        '_origins': {
          'api.example.com': {
            'GET': {
              '/users': {
                'path': api_fixture_file_path,
                'status_code': 200
              }
            }
          },
          'petstore.swagger.io': {
            'GET': {
              '/users': {
                'path': main_fixture_file_path,
                'status_code': 200
              }
            }
          }
        }
      }
    
    @pytest.fixture(scope='class')
    def mixed_fixtures(self, api_fixture_file_path: str, fallback_fixture_file_path: str):
      """Response fixtures with both origin-specific and fallback routes."""
      return {
        '_origins': {
          'api.example.com': {
            'GET': {
              '/users': {
                'path': api_fixture_file_path,
                'status_code': 200
              }
            }
          }
        },
        'GET': {
          '/users': {
            'path': fallback_fixture_file_path,
            'status_code': 200
          }
        }
      }

    def test_origin_specific_routing(self, api_mitmproxy_request: MitmproxyRequest, 
                                   api_fixture_file_path: str, main_fixture_file_path: str):
      """Test that origin-specific fixtures are used when origin matches."""
      # Create separate fixture files for each origin
      tmp_dir_path = DataDir.instance().tmp_dir_path
      api_fixtures_file = os.path.join(tmp_dir_path, 'api_origin_fixtures.yml')
      main_fixtures_file = os.path.join(tmp_dir_path, 'main_origin_fixtures.yml')
      
      # API-specific fixtures
      api_fixtures_content = {
        'GET': {
          '/users': {
            'path': api_fixture_file_path,
            'status_code': 200
          }
        }
      }
      
      # Main-specific fixtures
      main_fixtures_content = {
        'GET': {
          '/users': {
            'path': main_fixture_file_path,
            'status_code': 200
          }
        }
      }
      
      with open(api_fixtures_file, 'w') as f:
        yaml.dump(api_fixtures_content, f)
      
      with open(main_fixtures_file, 'w') as f:
        yaml.dump(main_fixtures_content, f)
      
      # Use response_fixtures_path with origin specification
      fixtures_paths = f"{api_fixtures_file}:https://api\\.example\\.com,{main_fixtures_file}:https://petstore\\.swagger\\.io"
      
      res: requests.Response = eval_fixtures(api_mitmproxy_request, response_fixtures_path=fixtures_paths)
      assert res is not None
      assert res.status_code == 200
      
      # Check that API-specific content is returned
      content = json.loads(res.raw.read().decode())
      assert content['users'][0]['name'] == 'API User'

    def test_different_origin_routing(self, main_mitmproxy_request: MitmproxyRequest, 
                                     api_fixture_file_path: str, main_fixture_file_path: str):
      """Test that different origin gets different fixtures."""
      # Create separate fixture files for each origin
      tmp_dir_path = DataDir.instance().tmp_dir_path
      api_fixtures_file = os.path.join(tmp_dir_path, 'api_diff_fixtures.yml')
      main_fixtures_file = os.path.join(tmp_dir_path, 'main_diff_fixtures.yml')
      
      # API-specific fixtures
      api_fixtures_content = {
        'GET': {
          '/users': {
            'path': api_fixture_file_path,
            'status_code': 200
          }
        }
      }
      
      # Main-specific fixtures
      main_fixtures_content = {
        'GET': {
          '/users': {
            'path': main_fixture_file_path,
            'status_code': 200
          }
        }
      }
      
      with open(api_fixtures_file, 'w') as f:
        yaml.dump(api_fixtures_content, f, sort_keys=False)
      
      with open(main_fixtures_file, 'w') as f:
        yaml.dump(main_fixtures_content, f, sort_keys=False)
      
      # Use response_fixtures_path with origin specification
      fixtures_paths = f"{api_fixtures_file}:https://api\\.example\\.com,{main_fixtures_file}:https://petstore\\.swagger\\.io"
      
      res: requests.Response = eval_fixtures(main_mitmproxy_request, response_fixtures_path=fixtures_paths)
      assert res is not None
      assert res.status_code == 200
      
      # Check that main-specific content is returned
      content = json.loads(res.raw.read().decode())
      assert content['users'][0]['name'] == 'Main User'

    def test_fallback_routing(self, main_mitmproxy_request: MitmproxyRequest, fallback_fixture_file_path: str):
      """Test that fallback fixtures are used when no origin-specific match."""
      # Create a fallback-only fixtures file
      tmp_dir_path = DataDir.instance().tmp_dir_path
      fallback_fixtures_file = os.path.join(tmp_dir_path, 'fallback_only_fixtures.yml')
      
      fallback_fixtures_content = {
        'GET': {
          '/users': {
            'path': fallback_fixture_file_path,
            'status_code': 200
          }
        }
      }
      
      with open(fallback_fixtures_file, 'w') as f:
        yaml.dump(fallback_fixtures_content, f, sort_keys=False)
      
      # Use a fixture file without origin specification (fallback)
      res: requests.Response = eval_fixtures(main_mitmproxy_request, response_fixtures_path=fallback_fixtures_file)
      assert res is not None
      assert res.status_code == 200
      
      # Check that fallback content is returned
      content = json.loads(res.raw.read().decode())
      assert content['users'][0]['name'] == 'Fallback User'

    def test_origin_match_takes_precedence(self, api_mitmproxy_request: MitmproxyRequest, 
                                         api_fixture_file_path: str, fallback_fixture_file_path: str):
      """Test that origin-specific fixtures take precedence over fallback."""
      # Create separate fixture files
      tmp_dir_path = DataDir.instance().tmp_dir_path
      api_fixtures_file = os.path.join(tmp_dir_path, 'api_precedence_fixtures.yml')
      fallback_fixtures_file = os.path.join(tmp_dir_path, 'fallback_precedence_fixtures.yml')
      
      # API-specific fixtures
      api_fixtures_content = {
        'GET': {
          '/users': {
            'path': api_fixture_file_path,
            'status_code': 200
          }
        }
      }
      
      # Fallback fixtures
      fallback_fixtures_content = {
        'GET': {
          '/users': {
            'path': fallback_fixture_file_path,
            'status_code': 200
          }
        }
      }
      
      with open(api_fixtures_file, 'w') as f:
        yaml.dump(api_fixtures_content, f, sort_keys=False)
      
      with open(fallback_fixtures_file, 'w') as f:
        yaml.dump(fallback_fixtures_content, f, sort_keys=False)
      
      # Use response_fixtures_path with origin-specific first, fallback second
      fixtures_paths = f"{api_fixtures_file}:https://api\\.example\\.com,{fallback_fixtures_file}"
      
      res: requests.Response = eval_fixtures(api_mitmproxy_request, response_fixtures_path=fixtures_paths)
      assert res is not None
      assert res.status_code == 200
      
      # Check that API-specific content is returned, not fallback
      content = json.loads(res.raw.read().decode())
      assert content['users'][0]['name'] == 'API User'

    def test_wildcard_origin_matching(self, settings: Settings, api_fixture_file_path: str):
      """Test wildcard origin matching for subdomains."""
      # Create request for subdomain
      status = RequestBuilder(
        method='GET',
        request_headers={'accept': 'application/json'},
        response_body='',
        status_code=200,
        url='https://sub.example.com/users',
      ).with_settings(settings).build()[1]
      assert status == 200

      subdomain_request = Request.last()
      subdomain_mitmproxy_request = MitmproxyRequestAdapter(subdomain_request).adapt()
      
      # Create wildcard fixtures file
      tmp_dir_path = DataDir.instance().tmp_dir_path
      wildcard_fixtures_file = os.path.join(tmp_dir_path, 'wildcard_fixtures.yml')
      
      wildcard_fixtures_content = {
        'GET': {
          '/users': {
            'path': api_fixture_file_path,
            'status_code': 200
          }
        }
      }
      
      with open(wildcard_fixtures_file, 'w') as f:
        yaml.dump(wildcard_fixtures_content, f, sort_keys=False)
      
      # Use regex wildcard pattern in response_fixtures_path
      fixtures_paths = f"{wildcard_fixtures_file}:https://.*\\.example\\.com"
      
      res: requests.Response = eval_fixtures(subdomain_mitmproxy_request, response_fixtures_path=fixtures_paths)
      assert res is not None
      assert res.status_code == 200
      
      # Check that API content is returned for wildcard match
      content = json.loads(res.raw.read().decode())
      assert content['users'][0]['name'] == 'API User'

    def test_response_fixtures_path_loading(self, api_mitmproxy_request: MitmproxyRequest, api_fixture_file_path: str):
      """Test that response fixtures are loaded from response_fixtures_path parameter."""
      # Create a temporary fixtures file
      tmp_dir_path = DataDir.instance().tmp_dir_path
      fixtures_file_path = os.path.join(tmp_dir_path, 'test_fixtures.yml')
      
      fixtures_content = {
        'GET': {
          '/users': {
            'path': api_fixture_file_path,
            'status_code': 200
          }
        }
      }
      
      with open(fixtures_file_path, 'w') as fp:
        yaml.dump(fixtures_content, fp, sort_keys=False)
      
      # Test loading fixtures via response_fixtures_path
      res: requests.Response = eval_fixtures(api_mitmproxy_request, response_fixtures_path=fixtures_file_path)
      assert res is not None
      assert res.status_code == 200
      
      # Check that correct content is returned
      content = json.loads(res.raw.read().decode())
      assert content['users'][0]['name'] == 'API User'

    def test_response_fixtures_path_with_origin(self, api_mitmproxy_request: MitmproxyRequest, 
                                               main_mitmproxy_request: MitmproxyRequest,
                                               api_fixture_file_path: str, main_fixture_file_path: str):
      """Test that response_fixtures_path supports origin-specific routing."""
      # Create temporary fixtures files
      tmp_dir_path = DataDir.instance().tmp_dir_path
      api_fixtures_file = os.path.join(tmp_dir_path, 'api_fixtures.yml')
      main_fixtures_file = os.path.join(tmp_dir_path, 'main_fixtures.yml')
      
      api_fixtures_content = {
        'GET': {
          '/users': {
            'path': api_fixture_file_path,
            'status_code': 200
          }
        }
      }
      
      main_fixtures_content = {
        'GET': {
          '/users': {
            'path': main_fixture_file_path,
            'status_code': 200
          }
        }
      }
      
      with open(api_fixtures_file, 'w') as fp:
        yaml.dump(api_fixtures_content, fp, sort_keys=False)
      
      with open(main_fixtures_file, 'w') as fp:
        yaml.dump(main_fixtures_content, fp, sort_keys=False)
      
      # Test with comma-separated paths with origins
      fixtures_paths = f"{api_fixtures_file}:https://api\\.example\\.com,{main_fixtures_file}:https://petstore\\.swagger\\.io"
      
      # Test API request
      api_res: requests.Response = eval_fixtures(api_mitmproxy_request, response_fixtures_path=fixtures_paths)
      assert api_res is not None
      assert api_res.status_code == 200
      api_content = json.loads(api_res.raw.read().decode())
      assert api_content['users'][0]['name'] == 'API User'
      
      # Test main request
      main_res: requests.Response = eval_fixtures(main_mitmproxy_request, response_fixtures_path=fixtures_paths)
      assert main_res is not None
      assert main_res.status_code == 200
      main_content = json.loads(main_res.raw.read().decode())
      assert main_content['users'][0]['name'] == 'Main User'

    def test_lazy_evaluation_stops_at_first_match(self, api_mitmproxy_request: MitmproxyRequest, api_fixture_file_path: str):
      """Test that lazy evaluation stops at the first matching fixture and doesn't process subsequent files."""
      # Create multiple fixtures files
      tmp_dir_path = DataDir.instance().tmp_dir_path
      first_fixtures_file = os.path.join(tmp_dir_path, 'first_fixtures.yml')
      second_fixtures_file = os.path.join(tmp_dir_path, 'second_fixtures.yml')
      invalid_fixtures_file = os.path.join(tmp_dir_path, 'invalid_fixtures.yml')
      
      # First file - should match and be used
      first_fixtures_content = {
        'GET': {
          '/users': {
            'path': api_fixture_file_path,
            'status_code': 201  # Different status to verify this file is used
          }
        }
      }
      
      # Second file - should not be processed since first file matches
      second_fixtures_content = {
        'GET': {
          '/users': {
            'path': api_fixture_file_path,
            'status_code': 202
          }
        }
      }
      
      with open(first_fixtures_file, 'w') as fp:
        yaml.dump(first_fixtures_content, fp, sort_keys=False)
      
      with open(second_fixtures_file, 'w') as fp:
        yaml.dump(second_fixtures_content, fp, sort_keys=False)
      
      # Create an invalid YAML file that would cause an error if processed
      with open(invalid_fixtures_file, 'w') as fp:
        fp.write("invalid: yaml: content: [unclosed")
      
      # Test with multiple paths - first should match, others should be ignored
      fixtures_paths = f"{first_fixtures_file}:https://api\\.example\\.com,{second_fixtures_file}:https://api\\.example\\.com,{invalid_fixtures_file}:https://api\\.example\\.com"
      
      # Should use first file and return status 201
      res: requests.Response = eval_fixtures(api_mitmproxy_request, response_fixtures_path=fixtures_paths)
      assert res is not None
      assert res.status_code == 201  # Should be from first file, not second
      
      # Verify content is from the expected file
      content = json.loads(res.raw.read().decode())
      assert content['users'][0]['name'] == 'API User'

    def test_origin_mismatch_skips_file(self, api_mitmproxy_request: MitmproxyRequest, 
                                       main_mitmproxy_request: MitmproxyRequest,
                                       api_fixture_file_path: str, main_fixture_file_path: str):
      """Test that files with non-matching origins are skipped without being loaded."""
      # Create fixtures files
      tmp_dir_path = DataDir.instance().tmp_dir_path
      wrong_origin_file = os.path.join(tmp_dir_path, 'wrong_origin.yml')
      correct_origin_file = os.path.join(tmp_dir_path, 'correct_origin.yml')
      
      # File with wrong origin - should be skipped
      wrong_origin_content = {
        'GET': {
          '/users': {
            'path': main_fixture_file_path,  # Different content
            'status_code': 404  # Different status to verify this isn't used
          }
        }
      }
      
      # File with correct origin - should be used
      correct_origin_content = {
        'GET': {
          '/users': {
            'path': api_fixture_file_path,
            'status_code': 200
          }
        }
      }
      
      with open(wrong_origin_file, 'w') as fp:
        yaml.dump(wrong_origin_content, fp, sort_keys=False)
      
      with open(correct_origin_file, 'w') as fp:
        yaml.dump(correct_origin_content, fp, sort_keys=False)
      
      # Test with API request - wrong origin should be skipped, correct origin should be used
      fixtures_paths = f"{wrong_origin_file}:https://petstore\\.swagger\\.io,{correct_origin_file}:https://api\\.example\\.com"
      
      res: requests.Response = eval_fixtures(api_mitmproxy_request, response_fixtures_path=fixtures_paths)
      assert res is not None
      assert res.status_code == 200  # Should be from correct origin file, not wrong origin
      
      # Verify content is from the API file (correct origin), not main file (wrong origin)
      content = json.loads(res.raw.read().decode())
      assert content['users'][0]['name'] == 'API User'

  class TestFullOriginFormatParsing():
    @pytest.fixture(scope='class')
    def tmp_dir_path(self):
      return DataDir.instance().tmp_dir_path

    def test_full_url_origin_parsing_response_fixtures(self, settings: Settings, tmp_dir_path: str):
      """Test parsing of full URL origins for response fixtures."""
      # Create test fixture files
      api_fixture_file = os.path.join(tmp_dir_path, 'full_url_api_fixture.json')
      with open(api_fixture_file, 'w') as f:
        json.dump({"message": "Full URL API Response"}, f)
      
      api_fixtures_file = os.path.join(tmp_dir_path, 'full_url_api_fixtures.yml')
      fixtures_content = {
        'GET': {
          '/api/data': {
            'path': api_fixture_file,
            'status_code': 200
          }
        }
      }
      with open(api_fixtures_file, 'w') as f:
        yaml.dump(fixtures_content, f, sort_keys=False)
      
      # Test full URL with port
      status = RequestBuilder(
        method='GET',
        request_headers={'accept': 'application/json'},
        response_body='',
        status_code=200,
        url='https://api.example.com:8080/api/data',
      ).with_settings(settings).build()[1]
      assert status == 200
      
      request = Request.last()
      mitmproxy_request = MitmproxyRequestAdapter(request).adapt()
      
      # Test with regex pattern for scheme:hostname:port (request origin is https://api.example.com:8080)
      fixtures_paths = f"{api_fixtures_file}:https://api\\.example\\.com:8080"
      
      res: requests.Response = eval_fixtures(mitmproxy_request, response_fixtures_path=fixtures_paths)
      assert res is not None
      assert res.status_code == 200
      content = json.loads(res.raw.read().decode())
      assert content['message'] == 'Full URL API Response'

    def test_origin_matching_with_different_schemes(self, settings: Settings, tmp_dir_path: str):
      """Test that origin matching works regardless of scheme differences."""
      # Create test fixture files
      api_fixture_file = os.path.join(tmp_dir_path, 'scheme_test_fixture.json')
      with open(api_fixture_file, 'w') as f:
        json.dump({"message": "Scheme Test Response"}, f)
      
      api_fixtures_file = os.path.join(tmp_dir_path, 'scheme_test_fixtures.yml')
      fixtures_content = {
        'GET': {
          '/test': {
            'path': api_fixture_file,
            'status_code': 200
          }
        }
      }
      with open(api_fixtures_file, 'w') as f:
        yaml.dump(fixtures_content, f, sort_keys=False)
      
      # Test HTTP request
      status = RequestBuilder(
        method='GET',
        request_headers={'accept': 'application/json'},
        response_body='',
        status_code=200,
        url='http://api.example.com:8080/test',  # HTTP request
      ).with_settings(settings).build()[1]
      assert status == 200
      
      request = Request.last()
      mitmproxy_request = MitmproxyRequestAdapter(request).adapt()
      
      # Test with regex pattern for scheme:hostname:port (request origin is http://api.example.com:8080)
      fixtures_paths = f"{api_fixtures_file}:http://api\\.example\\.com:8080"
      
      res: requests.Response = eval_fixtures(mitmproxy_request, response_fixtures_path=fixtures_paths)
      assert res is not None
      assert res.status_code == 200
      content = json.loads(res.raw.read().decode())
      assert content['message'] == 'Scheme Test Response'

    def test_wildcard_matching_with_full_origins(self, settings: Settings, tmp_dir_path: str):
      """Test wildcard matching with full origin URLs."""
      # Create test fixture files
      wildcard_fixture_file = os.path.join(tmp_dir_path, 'wildcard_test_fixture.json')
      with open(wildcard_fixture_file, 'w') as f:
        json.dump({"message": "Wildcard Match Response"}, f)
      
      wildcard_fixtures_file = os.path.join(tmp_dir_path, 'wildcard_test_fixtures.yml')
      fixtures_content = {
        'GET': {
          '/wildcard': {
            'path': wildcard_fixture_file,
            'status_code': 200
          }
        }
      }
      with open(wildcard_fixtures_file, 'w') as f:
        yaml.dump(fixtures_content, f, sort_keys=False)
      
      # Test subdomain request
      status = RequestBuilder(
        method='GET',
        request_headers={'accept': 'application/json'},
        response_body='',
        status_code=200,
        url='https://sub.example.com:8080/wildcard',
      ).with_settings(settings).build()[1]
      assert status == 200
      
      request = Request.last()
      mitmproxy_request = MitmproxyRequestAdapter(request).adapt()
      
      # Test with regex wildcard origin pattern
      fixtures_paths = f"{wildcard_fixtures_file}:https://.*\\.example\\.com:8080"
      
      res: requests.Response = eval_fixtures(mitmproxy_request, response_fixtures_path=fixtures_paths)
      assert res is not None
      assert res.status_code == 200
      content = json.loads(res.raw.read().decode())
      assert content['message'] == 'Wildcard Match Response'