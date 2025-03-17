import json
import pdb
import pytest

from click.testing import CliRunner

from stoobly_agent.test.test_helper import DETERMINISTIC_GET_REQUEST_URL, reset

from stoobly_agent.config.constants import mode
from stoobly_agent.app.settings.constants import request_component
from stoobly_agent.cli import config, mock, record, scenario
from stoobly_agent.lib.api.keys.scenario_key import ScenarioKey
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

  class TestScenario():

    @pytest.fixture
    def scenario_key(self, runner: CliRunner):
      res = runner.invoke(scenario, ['create', '--select', 'key', '--without-headers', 'test-scenario'])
      assert res.exit_code == 0
      return ScenarioKey(res.stdout.strip())