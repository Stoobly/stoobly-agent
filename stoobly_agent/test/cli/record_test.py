import json
import pdb
from telnetlib import DET
import pytest

from click.testing import CliRunner
from urllib.parse import parse_qs

from stoobly_agent.test.test_helper import DETERMINISTIC_GET_REQUEST_URL, NON_DETERMINISTIC_GET_REQUEST_URL, reset

from stoobly_agent.config.constants import mode, record_policy
from stoobly_agent.app.settings.constants import request_component
from stoobly_agent.app.models.adapters.raw_http_request_adapter import RawHttpRequestAdapter
from stoobly_agent.cli import config, intercept, mock, record, scenario
from stoobly_agent.lib.api.keys.scenario_key import ScenarioKey
from stoobly_agent.lib.orm.request import Request

@pytest.fixture()
def runner():
  return CliRunner()

class TestRecording():
      
  class TestMocking():
    @pytest.fixture(autouse=True)
    def settings(self):
      return reset()

    def test_it_mocks(self, runner: CliRunner):
      url = DETERMINISTIC_GET_REQUEST_URL
      record_result = runner.invoke(record, [url])
      assert record_result.exit_code == 0

      _request = Request.last()
      assert _request.url == url

      mock_result = runner.invoke(mock, [url])
      assert mock_result.exit_code == 0
      assert mock_result.stdout == record_result.stdout

  class TestRewriting():
    class TestWhenHeaders():
      @pytest.fixture(autouse=True)
      def settings(self):
        return reset()

      def test_it_rewrites(self, runner: CliRunner):
        header_name = 'foo'
        header_value = 'bar'

        rewrite_result = runner.invoke(config, [
            'rewrite', 'set', 
            '--method', 'GET', '--mode', mode.RECORD, '--name', header_name, '--value', header_value, '--pattern', '.*?', '--type', request_component.HEADER
          ]
        )
        assert rewrite_result.exit_code == 0

        record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
        assert record_result.exit_code == 0

        _request = Request.last()
        python_request = RawHttpRequestAdapter(_request.raw).to_request()

        assert python_request.headers.get(header_name.title()) == header_value

    class TestWhenQueryParams():
      @pytest.fixture(autouse=True)
      def settings(self):
        return reset()

      def test_it_rewrites(self, runner: CliRunner):
        query_param = 'foo'
        query_param_value = 'bar'

        rewrite_result = runner.invoke(config, [
            'rewrite', 'set', 
            '--method', 'GET', '--mode', mode.RECORD, '--name', query_param, '--value', query_param_value, '--pattern', '.*?', '--type', request_component.QUERY_PARAM
          ]
        )
        assert rewrite_result.exit_code == 0

        record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
        assert record_result.exit_code == 0

        _request = Request.last()

        query_params = parse_qs(_request.to_dict()['query'])
        values = query_params.get(query_param)
        assert values != None and len(values) == 1
        assert query_param_value in values

    class TestWhenBodyParams():
      @pytest.fixture(autouse=True)
      def settings(self):
        return reset()

      def test_it_rewrites(self, runner: CliRunner):
        body_param = 'foo'
        body_param_value = 'bar'

        rewrite_result = runner.invoke(config, [
            'rewrite', 'set', 
            '--method', 'GET', '--mode', mode.RECORD, '--name', body_param, '--value', body_param_value, '--pattern', '.*?', '--type', request_component.BODY_PARAM
          ]
        )
        assert rewrite_result.exit_code == 0

        record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
        assert record_result.exit_code == 0

        _request = Request.last()
        python_request = RawHttpRequestAdapter(_request.raw).to_request()

        # Since this request did not initially have a body, rewriting adds a body with header Content-Type: application/json
        assert python_request.headers.get('content-type'.title()) == 'application/json'

        body = python_request.data.decode()
        assert json.loads(body).get(body_param) == body_param_value

  class TestScenario():
    @pytest.fixture(autouse=True)
    def settings(self):
      return reset()

    @pytest.fixture()
    def scenario_key(self, runner: CliRunner):
      res = runner.invoke(scenario, ['create', '--select', 'key', '--without-headers', 'test-scenario'])
      assert res.exit_code == 0
      return ScenarioKey(res.stdout.strip())

    def test_it_sets_scenario_id(self, runner: CliRunner, scenario_key: ScenarioKey):
      record_result = runner.invoke(record, ['--scenario-key', scenario_key.raw, DETERMINISTIC_GET_REQUEST_URL])
      assert record_result.exit_code == 0

      _request = Request.last()
      assert _request.scenario_id == int(scenario_key.id)

  class TestNotFoundPolicy():
    @pytest.fixture(autouse=True)
    def settings(self):
      return reset()

    def test_it_records_only_not_found_requests(self, runner: CliRunner):
      intercept_result = runner.invoke(intercept, ['configure', '--policy', record_policy.NOT_FOUND])
      assert intercept_result.exit_code == 0

      record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
      assert record_result.exit_code == 0

      assert Request.count() == 1

      record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
      assert record_result.exit_code == 0

      assert Request.count() == 1

      record_result = runner.invoke(record, [NON_DETERMINISTIC_GET_REQUEST_URL])
      assert record_result.exit_code == 0

      assert Request.count() == 2

  class TestFoundPolicy():
    @pytest.fixture(autouse=True)
    def settings(self):
      return reset()

    def test_it_does_not_record_any_requests(self, runner: CliRunner):
      intercept_result = runner.invoke(intercept, ['configure', '--policy', record_policy.FOUND])
      assert intercept_result.exit_code == 0

      record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
      assert record_result.exit_code == 0

      assert Request.count() == 0

      record_result = runner.invoke(record, [NON_DETERMINISTIC_GET_REQUEST_URL])
      assert record_result.exit_code == 0

      assert Request.count() == 0

    def test_it_records_only_found_requests(self, runner: CliRunner):
      record_result = runner.invoke(record, [NON_DETERMINISTIC_GET_REQUEST_URL])
      assert record_result.exit_code == 0

      assert Request.count() == 1

      intercept_result = runner.invoke(intercept, ['configure', '--policy', record_policy.FOUND])
      assert intercept_result.exit_code == 0

      record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
      assert record_result.exit_code == 0

      assert Request.count() == 1

      record_result = runner.invoke(record, [NON_DETERMINISTIC_GET_REQUEST_URL])
      assert record_result.exit_code == 0

      assert Request.count() == 2