import base64
import json
import os
import pdb
import pytest

from click.testing import CliRunner
from pathlib import Path

from stoobly_agent.test.test_helper import DETERMINISTIC_GET_REQUEST_URL, reset

from stoobly_agent.app.cli.config_cli import config
from stoobly_agent.app.settings.constants import request_component
from stoobly_agent.config.constants import mode, custom_headers
from stoobly_agent.cli import mock, record
from stoobly_agent.lib.orm.request import Request

@pytest.fixture(scope='module')
def runner():
  return CliRunner()

class TestMocking():
  class TestRewriting():

    @pytest.fixture(autouse=True, scope='class')
    def settings(self):
      return reset()

    class TestWhenHeaders():
      header_name = 'foo'
      header_value = 'bar'
      url = DETERMINISTIC_GET_REQUEST_URL

      @pytest.fixture(autouse=True, scope='class')
      def recorded_request(self, runner: CliRunner):
        record_result = runner.invoke(record, [self.url, '-H', f"{self.header_name}: {self.header_value}"])
        assert record_result.exit_code == 0
        return Request.last()

      def test_it_ignores_headers_default(self, runner: CliRunner):
        # Expect to fail since we have not set up rewrite rule for mock mode
        mock_result = runner.invoke(mock, [self.url])
        assert mock_result.exit_code == 0

      def test_it_fails_when_enabled(self, runner: CliRunner):
        # Enforce matching by headers only
        match_result = runner.invoke(config, [
          'match', 'set',
          '--method', 'GET', '--mode', mode.MOCK, '--pattern', '.*?', '--component', request_component.HEADER
        ])
        assert match_result.exit_code == 0
        
        # Expect to fail since we have not set up rewrite rule for mock mode
        mock_result = runner.invoke(mock, [self.url])
        assert mock_result.exit_code == 1

      def test_it_succeeds_after_rewrite(self, runner: CliRunner):
        rewrite_result = runner.invoke(config, [
            'rewrite', 'set', 
            '--method', 'GET', '--mode', mode.MOCK, '--name', self.header_name, '--value', self.header_value, '--pattern', '.*?', '--type', request_component.HEADER
          ]
        )
        assert rewrite_result.exit_code == 0

        mock_result = runner.invoke(mock, [self.url])
        assert mock_result.exit_code == 0

    class TestWhenQueryParams():
      query_param_name = 'foo'
      query_param_value = 'bar'
      url = DETERMINISTIC_GET_REQUEST_URL

      @pytest.fixture(autouse=True, scope='class')
      def recorded_request(self, runner: CliRunner):
        record_result = runner.invoke(record, [f"{self.url}?{self.query_param_name}={self.query_param_value}"])
        assert record_result.exit_code == 0
        return Request.last()

      def test_it_ignores_query_params_by_default(self, runner: CliRunner):
        mock_result = runner.invoke(mock, [self.url])
        assert mock_result.exit_code == 0

      def test_it_fails_when_enabled(self, runner: CliRunner):
        # Enforce matching by query params only
        match_result = runner.invoke(config, [
          'match', 'set',
          '--method', 'GET', '--mode', mode.MOCK, '--pattern', '.*?', '--component', request_component.QUERY_PARAM
        ])
        assert match_result.exit_code == 0

        # Expect to fail since we have not set up rewrite rule for mock mode
        mock_result = runner.invoke(mock, [self.url])
        assert mock_result.exit_code == 1

      def test_it_succeeds_after_rewrites(self, runner: CliRunner):
        rewrite_result = runner.invoke(config, [
            'rewrite', 'set', 
            '--method', 'GET', '--mode', mode.MOCK, '--name', self.query_param_name, '--value', self.query_param_value, '--pattern', '.*?', '--type', request_component.QUERY_PARAM
          ]
        )
        assert rewrite_result.exit_code == 0

        mock_result = runner.invoke(mock, [self.url])
        assert mock_result.exit_code == 0

    class TestWhenBodyParams():
      body_param_name = 'foo'
      body_param_value = 'bar'
      url = DETERMINISTIC_GET_REQUEST_URL

      @pytest.fixture(autouse=True, scope='class')
      def recorded_request(self, runner: CliRunner):
        content = {}
        content[self.body_param_name] = self.body_param_value
        body = json.dumps(content)

        url = DETERMINISTIC_GET_REQUEST_URL
        record_result = runner.invoke(record, [url, '-d', body, '-H', 'Content-Type: application/json'])
        assert record_result.exit_code == 0
        return Request.last()

      def test_it_ignores_body_params_by_default(self, runner: CliRunner):
        mock_result = runner.invoke(mock, [self.url])
        assert mock_result.exit_code == 0

      def test_it_fails_when_enabled(self, runner: CliRunner):
        # Enforce matching by bodyy params only
        match_result = runner.invoke(config, [
          'match', 'set',
          '--method', 'GET', '--mode', mode.MOCK, '--pattern', '.*?', '--component', request_component.BODY_PARAM
        ])
        assert match_result.exit_code == 0

        # Expect to fail since we have not set up rewrite rule for mock mode
        mock_result = runner.invoke(mock, [self.url])
        assert mock_result.exit_code == 1

      def test_it_succeeds_after_rewrites(self, runner: CliRunner):
        rewrite_result = runner.invoke(config, [
            'rewrite', 'set', 
            '--method', 'GET', '--mode', mode.MOCK, '--name', self.body_param_name, '--value', self.body_param_value, '--pattern', '.*?', '--type', request_component.BODY_PARAM
          ]
        )
        assert rewrite_result.exit_code == 0

        mock_result = runner.invoke(mock, [self.url])
        assert mock_result.exit_code == 0


class TestRequestRulesHeaders():
  """Integration tests for X-Stoobly-Request-Match-Rules and X-Stoobly-Request-Rewrite-Rules headers."""

  @pytest.fixture(autouse=True, scope='class')
  def settings(self):
    return reset()

  class TestMatchRulesHeader():
    """Test X-Stoobly-Request-Match-Rules header integration."""
    
    header_name = 'Authorization'
    header_value = 'Bearer token123'
    url = DETERMINISTIC_GET_REQUEST_URL

    @pytest.fixture(autouse=True, scope='class')
    def recorded_request(self, runner: CliRunner):
      """Record a request with a specific header."""
      record_result = runner.invoke(record, [self.url, '-H', f"{self.header_name}: {self.header_value}"])
      assert record_result.exit_code == 0
      return Request.last()

    def test_it_fails_without_match_header_when_mismatch(self, runner: CliRunner):
      """Test that mock fails when headers don't match and no match rules header is provided."""
      # Set up strict header matching via config
      match_result = runner.invoke(config, [
        'match', 'set',
        '--method', 'GET', '--mode', mode.MOCK, '--pattern', '.*?', '--component', request_component.HEADER
      ])
      assert match_result.exit_code == 0
      
      # Request without the required header should fail
      mock_result = runner.invoke(mock, [self.url])
      assert mock_result.exit_code == 1

    def test_it_succeeds_with_match_rules_header(self, runner: CliRunner):
      """Test that mock succeeds when X-Stoobly-Request-Match-Rules header specifies components to match."""
      # Create match rules: only match on query params (ignore headers)
      match_rules = [
        {'components': request_component.QUERY_PARAM, 'modes': [mode.MOCK]}
      ]
      encoded_match_rules = base64.b64encode(json.dumps(match_rules).encode('utf-8')).decode('ascii')
      
      # Mock should succeed because we're only matching on query params (which are empty)
      mock_result = runner.invoke(mock, [
        self.url,
        '-H', f"{custom_headers.REQUEST_MATCH_RULES}: {encoded_match_rules}"
      ])
      assert mock_result.exit_code == 0

  class TestRewriteRulesHeader():
    """Test X-Stoobly-Request-Rewrite-Rules header integration."""
    
    header_name = 'X-Custom-Header'
    header_value = 'custom-value'
    url = DETERMINISTIC_GET_REQUEST_URL

    @pytest.fixture(autouse=True, scope='class')
    def recorded_request(self, runner: CliRunner):
      """Record a request with a specific header."""
      record_result = runner.invoke(record, [self.url, '-H', f"{self.header_name}: {self.header_value}"])
      assert record_result.exit_code == 0
      return Request.last()

    def test_it_fails_without_rewrite_header_when_mismatch(self, runner: CliRunner):
      """Test that mock fails when headers don't match and no rewrite rules header is provided."""
      # Set up strict header matching
      match_result = runner.invoke(config, [
        'match', 'set',
        '--method', 'GET', '--mode', mode.MOCK, '--pattern', '.*?', '--component', request_component.HEADER
      ])
      assert match_result.exit_code == 0
      
      # Request without the required header should fail
      mock_result = runner.invoke(mock, [self.url])
      assert mock_result.exit_code == 1

    def test_it_succeeds_with_rewrite_rules_header(self, runner: CliRunner):
      """Test that mock succeeds when X-Stoobly-Request-Rewrite-Rules header adds missing headers."""
      # Create rewrite rules: add the required header
      rewrite_rules = [
        {
          'parameter_rules': [
            {'type': request_component.HEADER, 'name': self.header_name, 'value': self.header_value}
          ]
        }
      ]
      encoded_rewrite_rules = base64.b64encode(json.dumps(rewrite_rules).encode('utf-8')).decode('ascii')
      
      # Mock should succeed because rewrite rules will add the required header
      mock_result = runner.invoke(mock, [
        self.url,
        '-H', f"{custom_headers.REQUEST_REWRITE_RULES}: {encoded_rewrite_rules}"
      ])
      assert mock_result.exit_code == 0


class TestPathHeaders():
  """Integration tests for path headers using actual mock_data files."""
  
  url = DETERMINISTIC_GET_REQUEST_URL
  fixtures_url = 'https://httpbin.org/get'
  public_file_url = 'http://localhost:8080/index.html'

  @pytest.fixture(autouse=True, scope='class')
  def settings(self):
    return reset()

  @pytest.fixture(autouse=True, scope='class')
  def recorded_request(self, runner: CliRunner, settings):
    """Record a request for mocking."""
    record_result = runner.invoke(record, [self.url])
    assert record_result.exit_code == 0
    return Request.last()

  @pytest.fixture(scope='class')
  def mock_data_dir(self):
    """Get path to mock_data directory."""
    return Path(__file__).parent.parent / 'mock_data'

  @pytest.fixture(scope='class')
  def lifecycle_hooks_path(self, mock_data_dir):
    """Get path to lifecycle hooks file."""
    return str(mock_data_dir / 'lifecycle_hooks.py')

  @pytest.fixture(scope='class')
  def response_fixtures_path(self, mock_data_dir):
    """Get path to response fixtures file."""
    return str(mock_data_dir / 'test_fixtures.yaml')

  @pytest.fixture(scope='class')
  def public_dir_path(self, mock_data_dir):
    """Get path to public directory."""
    return str(mock_data_dir / 'scaffold')

  def test_it_uses_response_fixtures_from_specified_file(self, runner: CliRunner, response_fixtures_path, mock_data_dir):
    """Test that mock uses actual response fixtures from the specified file and returns fixture data."""
    # Mock request matching the fixture URL
    mock_result = runner.invoke(mock, [
      self.fixtures_url,
      '-H', f"{custom_headers.RESPONSE_FIXTURES_PATH}: {response_fixtures_path}"
    ])
    
    # Should succeed
    assert mock_result.exit_code == 0, \
           f"Command failed. Output: {mock_result.output}"
    
    # Read the actual test_response.json file and verify the response matches
    test_response_path = mock_data_dir / 'test_response.json'
    with open(test_response_path, 'r') as f:
      expected_json = f.read().strip()
    
    output = mock_result.output
    # Verify the response contains the exact content from the fixture file
    assert expected_json in output, \
           f"Expected fixture content not found. Expected: {expected_json}, Output: {output}"

  def test_it_serves_static_file_from_public_directory(self, runner: CliRunner, public_dir_path, mock_data_dir):
    """Test that mock serves actual static files from public directory and returns file content."""
    # Mock request for index.html from public directory
    mock_result = runner.invoke(mock, [
      self.public_file_url,
      '-H', f"{custom_headers.PUBLIC_DIRECTORY_PATH}: {public_dir_path}"
    ])
    
    # Should succeed
    assert mock_result.exit_code == 0
    
    # Read the actual index.html file and verify the response contains its content
    index_html_path = mock_data_dir / 'scaffold' / 'index.html'
    with open(index_html_path, 'r') as f:
      expected_content = f.read()
    
    output = mock_result.output
    assert output == expected_content

  def test_it_executes_lifecycle_hooks_from_specified_file(self, runner: CliRunner, recorded_request, lifecycle_hooks_path):
    """Test that mock executes actual lifecycle hooks from the specified file and verifies behavior."""
    # Mock request with the lifecycle hooks path header pointing to actual file
    mock_result = runner.invoke(mock, [
      self.url,
      '-H', f"{custom_headers.LIFECYCLE_HOOKS_PATH}: {lifecycle_hooks_path}"
    ])
    
    # Should succeed
    assert mock_result.exit_code == 0
    
    # Verify lifecycle hooks from mock_data/lifecycle_hooks.py were actually executed
    # The file contains functions that print specific messages:
    # - handle_before_request prints 'before_request'
    # - handle_before_mock prints 'before_mock'  
    # - handle_after_mock prints 'after_mock'
    # - handle_before_response prints 'before_response'
    output = mock_result.output
    
    # Check that at least one of the mock-related hooks was called
    # This verifies the actual file content is being loaded and executed
    assert ('before_request' in output or 
            'before_mock' in output or 
            'after_mock' in output or 
            'before_response' in output), \
            f"Expected lifecycle hook output not found. Output was: {output}"
