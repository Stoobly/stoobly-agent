import json
import pdb
import pytest

from click.testing import CliRunner
from typing import List
from urllib.parse import parse_qs

from stoobly_agent.test.test_helper import DETERMINISTIC_GET_REQUEST_URL, NON_DETERMINISTIC_GET_REQUEST_URL, reset

from stoobly_agent.app.models.adapters.raw_http_request_adapter import RawHttpRequestAdapter
from stoobly_agent.app.settings.constants import firewall_action, request_component
from stoobly_agent.config.constants import custom_headers, mode, record_policy, request_origin
from stoobly_agent.cli import config, intercept, mock, record, scenario
from stoobly_agent.lib.api.keys.scenario_key import ScenarioKey
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.lib.orm.scenario import Scenario
from stoobly_agent.lib.utils.decode import decode

@pytest.fixture(scope='module')
def runner():
  return CliRunner()

class TestRecording():
  @pytest.fixture(scope='class', autouse=True)
  def settings(self):
    return reset()

  class TestMocking():

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

    def test_it_checks_mode(self, runner: CliRunner):
      header_name = 'foo'
      header_value = 'bar'

      rewrite_result = runner.invoke(config, [
          'rewrite', 'set', 
          '--method', 'GET', '--mode', mode.MOCK, '--name', header_name, '--value', header_value, '--pattern', '.*?', '--type', request_component.HEADER
        ]
      )
      assert rewrite_result.exit_code == 0

      record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
      assert record_result.exit_code == 0

      _request = Request.last()
      python_request = RawHttpRequestAdapter(_request.raw).to_request()

      assert python_request.headers.get(header_name.title()) == None

    class TestWhenHeaders():

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

        query_params = parse_qs(_request.get_raw_attribute('query'))
        values = query_params.get(query_param)
        assert values != None and len(values) == 1
        assert query_param_value in values

    class TestWhenBodyParams():

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

        body = decode(python_request.data)
        assert json.loads(body).get(body_param) == body_param_value

  class TestFirewall():
    @pytest.fixture(scope='function', autouse=True)
    def settings(self):
      return reset()

    class TestWhenCli():

      def test_it_does_not_exclude(self, runner: CliRunner):
        rewrite_result = runner.invoke(config, [
            'firewall', 'set', 
            '--method', 'GET', '--mode', mode.RECORD, '--pattern', '.*?', '--action', firewall_action.EXCLUDE
          ]
        )
        assert rewrite_result.exit_code == 0

        record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
        assert record_result.exit_code == 0

        assert Request.count() ==  1

      def test_it_includes(self, runner: CliRunner):
        rewrite_result = runner.invoke(config, [
            'firewall', 'set', 
            '--method', 'GET', '--mode', mode.RECORD, '--pattern', DETERMINISTIC_GET_REQUEST_URL, '--action', firewall_action.INCLUDE
          ]
        )
        assert rewrite_result.exit_code == 0

        record_result = runner.invoke(record, [NON_DETERMINISTIC_GET_REQUEST_URL])
        assert record_result.exit_code == 0

        assert Request.count() == 1, 'Request should be included'

        record_result = runner.invoke(record, ['--header', f"{custom_headers.REQUEST_ORIGIN}: {request_origin.WEB}", DETERMINISTIC_GET_REQUEST_URL])
        assert record_result.exit_code == 0

        assert Request.count() == 2, 'Request should be included'
    
    class TestWhenNotCli():

      def test_it_excludes(self, runner: CliRunner):
        rewrite_result = runner.invoke(config, [
            'firewall', 'set', 
            '--method', 'GET', '--mode', mode.RECORD, '--pattern', '.*?', '--action', firewall_action.EXCLUDE
          ]
        )
        assert rewrite_result.exit_code == 0

        record_result = runner.invoke(record, ['--header', f"{custom_headers.REQUEST_ORIGIN}: {request_origin.WEB}", DETERMINISTIC_GET_REQUEST_URL])
        assert record_result.exit_code == 0

        assert Request.count() == 0

      def test_it_checks_mode(self, runner: CliRunner):
        rewrite_result = runner.invoke(config, [
            'firewall', 'set', 
            '--method', 'GET', '--mode', mode.MOCK, '--pattern', '.*?', '--action', firewall_action.EXCLUDE
          ]
        )
        assert rewrite_result.exit_code == 0

        record_result = runner.invoke(record, ['--header', f"{custom_headers.REQUEST_ORIGIN}: {request_origin.WEB}", DETERMINISTIC_GET_REQUEST_URL])
        assert record_result.exit_code == 0

        assert Request.count() == 1

      def test_it_includes(self, runner: CliRunner):
        rewrite_result = runner.invoke(config, [
            'firewall', 'set', 
            '--method', 'GET', '--mode', mode.RECORD, '--pattern', DETERMINISTIC_GET_REQUEST_URL, '--action', firewall_action.INCLUDE
          ]
        )
        assert rewrite_result.exit_code == 0

        record_result = runner.invoke(record, ['--header', f"{custom_headers.REQUEST_ORIGIN}: {request_origin.WEB}", NON_DETERMINISTIC_GET_REQUEST_URL])
        assert record_result.exit_code == 0

        assert Request.count() == 0, 'Request should not be included'

        record_result = runner.invoke(record, ['--header', f"{custom_headers.REQUEST_ORIGIN}: {request_origin.WEB}", DETERMINISTIC_GET_REQUEST_URL])
        assert record_result.exit_code == 0

        assert Request.count() == 1, 'Request should be included'

  class TestScenario():

    @pytest.fixture()
    def scenario_key(self, runner: CliRunner):
      res = runner.invoke(scenario, ['create', '--select', 'key', '--without-headers', 'test-scenario'])
      assert res.exit_code == 0
      return ScenarioKey(res.stdout.strip())

    def test_it_sets_scenario_id(self, runner: CliRunner, scenario_key: ScenarioKey):
      record_result = runner.invoke(record, ['--scenario-key', scenario_key.raw, DETERMINISTIC_GET_REQUEST_URL])
      assert record_result.exit_code == 0

      _request = Request.last()
      assert _request.scenario.uuid == scenario_key.id

  class TestNotFoundPolicy():

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
    @pytest.fixture(scope='function', autouse=True)
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

  class TestOverwritePolicy():

    @pytest.fixture(scope='class', autouse=True)
    def created_scenario(self, runner: CliRunner):
      scenario_create_result = runner.invoke(scenario, ['create', 'test'])
      assert scenario_create_result.exit_code == 0

      return Scenario.last()

    @pytest.fixture(scope='class', autouse=True)
    def recorded_requests(self, runner: CliRunner, created_scenario: Scenario):
      record_result = runner.invoke(record, ['--scenario-key', created_scenario.key(), DETERMINISTIC_GET_REQUEST_URL])
      assert record_result.exit_code == 0
      record_result = runner.invoke(record, ['--scenario-key', created_scenario.key(), DETERMINISTIC_GET_REQUEST_URL])
      assert record_result.exit_code == 0
      return Request.all()

    @pytest.fixture(scope='class', autouse=True)
    def enable_overwrite_results(self, runner: CliRunner, created_scenario: Scenario, recorded_requests: List[Request]):
      _created_scenario = Scenario.find(created_scenario.id)
      assert _created_scenario.requests_count == len(recorded_requests)

      config_results = runner.invoke(intercept, ['configure', '--mode', mode.RECORD, '--policy', record_policy.OVERWRITE])
      assert config_results.exit_code == 0

      set_results = runner.invoke(config, ['scenario', 'set', created_scenario.key()])
      assert set_results.exit_code == 0
      return config_results

    @pytest.fixture(scope='class')
    def recorded_new_requests(self, runner: CliRunner, created_scenario: Scenario, recorded_requests: List[Request]):
      _created_scenario = Scenario.find(created_scenario.id)
      assert _created_scenario.requests_count == len(recorded_requests)
      assert _created_scenario.overwritable

      # Only on first request record do overwrite the scenario
      record_result = runner.invoke(record, ['--scenario-key', created_scenario.key(), NON_DETERMINISTIC_GET_REQUEST_URL])
      assert record_result.exit_code == 0

      _created_scenario = Scenario.find(created_scenario.id)
      return _created_scenario.requests

    def test_it_sets_scenario_not_overwritable(self, created_scenario: Scenario, recorded_new_requests: List[Request]):
      _created_scenario = Scenario.find(created_scenario.id)
      assert _created_scenario.requests_count == len(recorded_new_requests)
      assert _created_scenario.overwritable == False