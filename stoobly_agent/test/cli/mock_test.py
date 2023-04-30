import json
import pdb
import pytest

from click.testing import CliRunner

from stoobly_agent.test.test_helper import DETERMINISTIC_GET_REQUEST_URL, reset

from stoobly_agent.config.constants import mode
from stoobly_agent.app.settings.constants import request_component
from stoobly_agent.cli import config, mock, record, scenario
from stoobly_agent.lib.api.keys.scenario_key import ScenarioKey

@pytest.fixture()
def runner():
  return CliRunner()

class TestMocking():
  class TestRewriting():

    @pytest.fixture(autouse=True, scope='class')
    def settings(self):
      return reset()

    class TestWhenHeaders():

      def test_it_rewrites(self, runner: CliRunner):
        header_name = 'foo'
        header_value = 'bar'

        url = DETERMINISTIC_GET_REQUEST_URL
        record_result = runner.invoke(record, [url, '-H', f"{header_name}: {header_value}"])
        assert record_result.exit_code == 0

        # Enforce matching by headers only
        match_result = runner.invoke(config, [
          'match', 'set',
          '--method', 'GET', '--mode', mode.MOCK, '--pattern', '.*?', '--component', request_component.HEADER
        ])
        assert match_result.exit_code == 0

        # Expect to fail since we have not set up rewrite rule for mock mode
        mock_result = runner.invoke(mock, [url])
        assert mock_result.exit_code == 1

        rewrite_result = runner.invoke(config, [
            'rewrite', 'set', 
            '--method', 'GET', '--mode', mode.MOCK, '--name', header_name, '--value', header_value, '--pattern', '.*?', '--type', request_component.HEADER
          ]
        )
        assert rewrite_result.exit_code == 0

        mock_result = runner.invoke(mock, [url])
        assert mock_result.exit_code == 0

    class TestWhenQueryParams():

      def test_it_rewrites(self, runner: CliRunner):
        query_param_name = 'foo'
        query_param_value = 'bar'

        url = DETERMINISTIC_GET_REQUEST_URL
        record_result = runner.invoke(record, [f"{url}?{query_param_name}={query_param_value}"])
        assert record_result.exit_code == 0

        # Enforce matching by query params only
        match_result = runner.invoke(config, [
          'match', 'set',
          '--method', 'GET', '--mode', mode.MOCK, '--pattern', '.*?', '--component', request_component.QUERY_PARAM
        ])
        assert match_result.exit_code == 0

        # Expect to fail since we have not set up rewrite rule for mock mode
        mock_result = runner.invoke(mock, [url])
        assert mock_result.exit_code == 1

        rewrite_result = runner.invoke(config, [
            'rewrite', 'set', 
            '--method', 'GET', '--mode', mode.MOCK, '--name', query_param_name, '--value', query_param_value, '--pattern', '.*?', '--type', request_component.QUERY_PARAM
          ]
        )
        assert rewrite_result.exit_code == 0

        mock_result = runner.invoke(mock, [url])
        assert mock_result.exit_code == 0

    class TestWhenBodyParams():

      def test_it_rewrites(self, runner: CliRunner):
        body_param_name = 'foo'
        body_param_value = 'bar'

        content = {}
        content[body_param_name] = body_param_value
        body = json.dumps(content)

        url = DETERMINISTIC_GET_REQUEST_URL
        record_result = runner.invoke(record, [url, '-d', body, '-H', 'Content-Type: application/json'])
        assert record_result.exit_code == 0

        # Enforce matching by query params only
        match_result = runner.invoke(config, [
          'match', 'set',
          '--method', 'GET', '--mode', mode.MOCK, '--pattern', '.*?', '--component', request_component.BODY_PARAM
        ])
        assert match_result.exit_code == 0

        # Expect to fail since we have not set up rewrite rule for mock mode
        mock_result = runner.invoke(mock, [url])
        assert mock_result.exit_code == 1

        rewrite_result = runner.invoke(config, [
            'rewrite', 'set', 
            '--method', 'GET', '--mode', mode.MOCK, '--name', body_param_name, '--value', body_param_value, '--pattern', '.*?', '--type', request_component.BODY_PARAM
          ]
        )
        assert rewrite_result.exit_code == 0

        mock_result = runner.invoke(mock, [url])
        assert mock_result.exit_code == 0

  class TestScenario():

    @pytest.fixture
    def scenario_key(self, runner: CliRunner):
      res = runner.invoke(scenario, ['create', '--select', 'key', '--without-headers', 'test-scenario'])
      assert res.exit_code == 0
      return ScenarioKey(res.stdout.strip())