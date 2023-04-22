import json
import pdb
import pytest

from click.testing import CliRunner
from urllib.parse import parse_qs

from stoobly_agent.test.test_helper import reset

from stoobly_agent.config.constants import mode, record_policy
from stoobly_agent.app.settings import Settings
from stoobly_agent.app.settings.constants import request_component
from stoobly_agent.app.models.adapters.raw_http_request_adapter import RawHttpRequestAdapter
from stoobly_agent.cli import config, intercept, mock, record, scenario
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

      def test_it_sets_scenario_id(self, settings, scenario_key: ScenarioKey):
        runner = CliRunner()

        url = 'www.google.com'
        record_result = runner.invoke(record, ['--scenario-key', scenario_key.raw, url])
        assert record_result.exit_code == 0

        _request = Request.last()
        assert _request.scenario_id == int(scenario_key.id)

    class TestWhenNotFoundPolicy():

      def test_it_records_only_not_found_requests(self, settings: Settings):
        runner = CliRunner()

        intercept_result = runner.invoke(intercept, ['configure', '--policy', record_policy.NOT_FOUND])
        assert intercept_result.exit_code == 0

        url = 'www.google.com'
        record_result = runner.invoke(record, [url])
        assert record_result.exit_code == 0

        assert Request.count() == 1

        url = 'www.google.com'
        record_result = runner.invoke(record, [url])
        assert record_result.exit_code == 0

        assert Request.count() == 1

        url = 'www.facebook.com'
        record_result = runner.invoke(record, [url])
        assert record_result.exit_code == 0

        assert Request.count() == 2

    class TestWhenNotFoundPolicy():

      def test_it_does_not_record_any_requests(self, settings: Settings):
        runner = CliRunner()

        intercept_result = runner.invoke(intercept, ['configure', '--policy', record_policy.FOUND])
        assert intercept_result.exit_code == 0

        url = 'www.google.com'
        record_result = runner.invoke(record, [url])
        assert record_result.exit_code == 0

        assert Request.count() == 0

        url = 'www.facebook.com'
        record_result = runner.invoke(record, [url])
        assert record_result.exit_code == 0

        assert Request.count() == 0

      def test_it_records_only_found_requests(self, settings: Settings):
        runner = CliRunner()

        url = 'www.google.com'
        record_result = runner.invoke(record, [url])
        assert record_result.exit_code == 0

        assert Request.count() == 1

        intercept_result = runner.invoke(intercept, ['configure', '--policy', record_policy.FOUND])
        assert intercept_result.exit_code == 0

        url = 'www.facebook.com'
        record_result = runner.invoke(record, [url])
        assert record_result.exit_code == 0

        assert Request.count() == 1

        url = 'www.google.com'
        record_result = runner.invoke(record, [url])
        assert record_result.exit_code == 0

        assert Request.count() == 2