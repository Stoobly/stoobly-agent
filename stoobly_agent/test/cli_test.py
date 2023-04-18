import json
import os
import pdb
import pytest

from click.testing import CliRunner
from urllib.parse import parse_qs

from stoobly_agent.test.test_helper import reset

from stoobly_agent.config.constants import mode
from stoobly_agent.app.settings import Settings
from stoobly_agent.app.settings.constants import request_component
from stoobly_agent.app.models.adapters.raw_http_request_adapter import RawHttpRequestAdapter
from stoobly_agent.cli import config, mock, record, scenario
from stoobly_agent.lib.api.keys.scenario_key import ScenarioKey
from stoobly_agent.lib.orm.request import Request

@pytest.fixture
def settings():
  return reset()

@pytest.fixture
def scenario_key() -> ScenarioKey:
  runner = CliRunner()
  res = runner.invoke(scenario, ['create', '--select', 'key', '--without-headers', 'test-scenario'])
  assert res.exit_code == 0
  return ScenarioKey(res.stdout.strip())

class TestCli():

  class TestWhenRecording():
    def test_it_mocks(self, settings):
      runner = CliRunner()

      url = 'www.google.com'
      record_result = runner.invoke(record, [url])
      assert record_result.exit_code == 0

      _request = Request.last()
      assert _request.host == url

      mock_result = runner.invoke(mock, [url])
      assert mock_result.exit_code == 0
      assert mock_result.stdout == record_result.stdout

    class TestWhenRewriting():
      def test_it_rewrites_header(self, settings):
        runner = CliRunner()
        header_name = 'foo'
        header_value = 'bar'

        rewrite_result = runner.invoke(config, [
            'rewrite', 'set', 
            '--method', 'GET', '--mode', mode.RECORD, '--name', header_name, '--value', header_value, '--pattern', '.*?', '--type', request_component.HEADER
          ]
        )
        assert rewrite_result.exit_code == 0

        url = 'www.google.com'
        record_result = runner.invoke(record, [url])
        assert record_result.exit_code == 0

        _request = Request.last()
        python_request = RawHttpRequestAdapter(_request.raw).to_request()

        assert python_request.headers.get(header_name.title()) == header_value

      def test_it_rewrites_query_param(self, settings):
        runner = CliRunner()
        query_param = 'foo'
        query_param_value = 'bar'

        rewrite_result = runner.invoke(config, [
            'rewrite', 'set', 
            '--method', 'GET', '--mode', mode.RECORD, '--name', query_param, '--value', query_param_value, '--pattern', '.*?', '--type', request_component.QUERY_PARAM
          ]
        )
        assert rewrite_result.exit_code == 0

        url = 'www.google.com'
        record_result = runner.invoke(record, [url])
        assert record_result.exit_code == 0

        _request = Request.last()

        query_params = parse_qs(_request.to_dict()['query'])
        values = query_params.get(query_param)
        assert values != None and len(values) == 1
        assert query_param_value in values

      def test_it_rewrites_body_param(self, settings):
        runner = CliRunner()
        body_param = 'foo'
        body_param_value = 'bar'

        rewrite_result = runner.invoke(config, [
            'rewrite', 'set', 
            '--method', 'GET', '--mode', mode.RECORD, '--name', body_param, '--value', body_param_value, '--pattern', '.*?', '--type', request_component.BODY_PARAM
          ]
        )
        assert rewrite_result.exit_code == 0

        url = 'www.google.com'
        record_result = runner.invoke(record, [url])
        assert record_result.exit_code == 0

        _request = Request.last()
        python_request = RawHttpRequestAdapter(_request.raw).to_request()

        # Since this request did not initially have a body, rewriting adds a body with header Content-Type: application/json
        assert python_request.headers.get('content-type'.title()) == 'application/json'

        body = python_request.data.decode()
        assert json.loads(body).get(body_param) == body_param_value

    class TestWhenToScenario():

      def test_it_sets_scenario_id(settings, scenario_key: ScenarioKey):
        runner = CliRunner()

        url = 'www.google.com'
        record_result = runner.invoke(record, ['--scenario-key', scenario_key.raw, url])
        assert record_result.exit_code == 0

        _request = Request.last()
        assert _request.scenario_id == int(scenario_key.id)

  class TestWhenMocking():

    class TestWhenRewriting():

      def test_it_rewrites_headers(self, settings):
        runner = CliRunner()
        header_name = 'foo'
        header_value = 'bar'

        url = 'www.google.com'
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

      def test_it_rewrites_query_params(self, settings):
        runner = CliRunner()
        query_param_name = 'foo'
        query_param_value = 'bar'

        url = 'www.google.com'
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

      def test_it_rewrites_body_params(self, settings):
        runner = CliRunner()
        body_param_name = 'foo'
        body_param_value = 'bar'

        content = {}
        content[body_param_name] = body_param_value
        body = json.dumps(content)

        url = 'www.google.com'
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