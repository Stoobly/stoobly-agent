import json
import os
import shutil
from pathlib import Path
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from stoobly_agent.app.cli.helpers.openapi_endpoint_adapter import (
  compute_openapi_endpoint_id,
  compute_openapi_service_id,
)
from stoobly_agent.app.cli.request_cli import request
from stoobly_agent.app.proxy.mock.endpoint_cache import endpoint_cache
from stoobly_agent.app.proxy.mock.search_open_api_endpoint import (
  inject_search_open_api_endpoint,
  search_open_api_endpoint,
)
import stoobly_agent.app.proxy.replay.replay_request_service as replay_request_service
from stoobly_agent.cli import record
from stoobly_agent.config.constants import custom_headers, test_strategy
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.lib.orm.transformers import ORMToRequestsResponseTransformer
from stoobly_agent.test.test_helper import DETERMINISTIC_GET_REQUEST_URL, reset

MOCK_DATA_DIR = Path(__file__).resolve().parents[3] / 'mock_data'
DOGS_OPENAPI_PATH = MOCK_DATA_DIR / 'dogs.ceo.openapi.yaml'
DOGS_OPENAPI_INVALID_STATUS_PATH = MOCK_DATA_DIR / 'dogs.ceo.openapi.invalid-status-type.yaml'
DOGS_OPENAPI_UNMATCHED_PATH = MOCK_DATA_DIR / 'dogs.ceo.openapi.unmatched-path.yaml'

EXPECTED_DOGS_ENDPOINT_ID = compute_openapi_endpoint_id(
  compute_openapi_service_id('dog.ceo', '443'),
  '/api/breeds/list/all',
  'GET',
)


@pytest.fixture(scope='module')
def runner():
  return CliRunner()


@pytest.fixture(autouse=True)
def reset_endpoint_cache():
  endpoint_cache.clear_cache()
  yield
  endpoint_cache.clear_cache()


@pytest.mark.openapi
class TestRequestTestWithOpenapiSpecification:
  @pytest.fixture(scope='class', autouse=True)
  def settings(self):
    return reset()

  @pytest.fixture(scope='class')
  def recorded_request(self, runner: CliRunner):
    record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
    assert record_result.exit_code == 0, record_result.stdout
    return Request.last()

  class TestWhenContractStrategyMatches:
    def test_it_passes(self, runner: CliRunner, recorded_request: Request):
      result = runner.invoke(
        request,
        [
          'test',
          '--strategy', test_strategy.CONTRACT,
          '--openapi-specification-path', str(DOGS_OPENAPI_PATH),
          recorded_request.key(),
        ],
      )
      assert result.exit_code == 0, result.stdout

    def test_it_passes_with_json_output(self, runner: CliRunner, recorded_request: Request):
      result = runner.invoke(
        request,
        [
          'test',
          '--strategy', test_strategy.CONTRACT,
          '--format', 'json',
          '--openapi-specification-path', str(DOGS_OPENAPI_PATH),
          recorded_request.key(),
        ],
      )

      assert result.exit_code == 0, result.stdout
      payload = json.loads(result.stdout)
      assert payload['passed'] == payload['total']
      assert payload['total'] == 1

  class TestWhenContractStrategyFails:
    def test_it_fails_when_response_type_does_not_match_spec(
      self, runner: CliRunner, recorded_request: Request
    ):
      result = runner.invoke(
        request,
        [
          'test',
          '--strategy', test_strategy.CONTRACT,
          '--format', 'json',
          '--openapi-specification-path', str(DOGS_OPENAPI_INVALID_STATUS_PATH),
          recorded_request.key(),
        ],
      )
      assert result.exit_code == 1, result.stdout
      payload = json.loads(result.stdout)
      assert payload['passed'] == 0
      assert payload['total'] == 1
      assert payload['tests'][0]['passed'] is False
      assert 'status' in (payload['tests'][0].get('log') or '')

  class TestWhenOpenapiPathIsForwarded:
    def test_it_searches_openapi_endpoint(
      self, runner: CliRunner, recorded_request: Request
    ):
      with patch(
        'stoobly_agent.app.proxy.mock.eval_request_service.inject_search_open_api_endpoint',
        wraps=inject_search_open_api_endpoint,
      ) as inject_spy:
        result = runner.invoke(
          request,
          [
            'test',
            '--strategy', test_strategy.DIFF,
            '--openapi-specification-path', str(DOGS_OPENAPI_PATH),
            recorded_request.key(),
          ],
        )
        assert result.exit_code == 0, result.stdout
        assert inject_spy.call_count == 1
        assert inject_spy.call_args[0][0] == str(DOGS_OPENAPI_PATH)

    def test_it_absolutizes_relative_openapi_path(
      self, runner: CliRunner, recorded_request: Request
    ):
      relative_name = 'dogs.ceo.openapi.yaml'
      shutil.copyfile(DOGS_OPENAPI_PATH, os.path.join(os.getcwd(), relative_name))

      with patch(
        'stoobly_agent.app.proxy.mock.eval_request_service.inject_search_open_api_endpoint',
        wraps=inject_search_open_api_endpoint,
      ) as inject_spy:
        result = runner.invoke(
          request,
          [
            'test',
            '--strategy', test_strategy.DIFF,
            '--openapi-specification-path', relative_name,
            recorded_request.key(),
          ],
        )
        assert result.exit_code == 0, result.stdout
        assert inject_spy.call_count == 1
        forwarded_path = inject_spy.call_args[0][0]
        assert os.path.isabs(forwarded_path)
        assert forwarded_path.endswith(relative_name)

    def test_it_sets_openapi_specification_path_header(
      self, runner: CliRunner, recorded_request: Request
    ):
      captured = {}
      real_handle = getattr(replay_request_service, '__handle_path_header')

      def wrapping_handle(header_name, script_path, headers):
        if header_name == custom_headers.OPENAPI_SPECIFICATION_PATH:
          captured['header_name'] = header_name
          captured['path'] = script_path
        return real_handle(header_name, script_path, headers)

      with patch.object(
        replay_request_service,
        '__handle_path_header',
        side_effect=wrapping_handle,
      ):
        result = runner.invoke(
          request,
          [
            'test',
            '--strategy', test_strategy.DIFF,
            '--openapi-specification-path', str(DOGS_OPENAPI_PATH),
            recorded_request.key(),
          ],
        )

      assert result.exit_code == 0, result.stdout
      assert captured.get('header_name') == custom_headers.OPENAPI_SPECIFICATION_PATH
      assert captured.get('path') == str(DOGS_OPENAPI_PATH)

  class TestWhenOriginScopedPath:
    def test_it_passes_when_origin_matches(
      self, runner: CliRunner, recorded_request: Request
    ):
      scoped_path = f'{DOGS_OPENAPI_PATH}:https://dog.ceo'
      result = runner.invoke(
        request,
        [
          'test',
          '--strategy', test_strategy.CONTRACT,
          '--openapi-specification-path', scoped_path,
          recorded_request.key(),
        ],
      )
      assert result.exit_code == 0, result.stdout

    def test_it_does_not_apply_unmatched_origin_scoped_spec(
      self, runner: CliRunner, recorded_request: Request
    ):
      # Origin does not match dog.ceo, so the invalid-type spec must not be applied.
      scoped_path = f'{DOGS_OPENAPI_INVALID_STATUS_PATH}:https://example.com'
      result = runner.invoke(
        request,
        [
          'test',
          '--strategy', test_strategy.CONTRACT,
          '--format', 'json',
          '--openapi-specification-path', scoped_path,
          recorded_request.key(),
        ],
      )
      assert result.exit_code == 0, result.stdout
      payload = json.loads(result.stdout)
      assert payload['passed'] == payload['total']

  class TestWhenEndpointDoesNotMatch:
    def test_it_passes_contract_when_spec_has_no_matching_path(
      self, runner: CliRunner, recorded_request: Request
    ):
      result = runner.invoke(
        request,
        [
          'test',
          '--strategy', test_strategy.CONTRACT,
          '--format', 'json',
          '--openapi-specification-path', str(DOGS_OPENAPI_UNMATCHED_PATH),
          recorded_request.key(),
        ],
      )
      assert result.exit_code == 0, result.stdout
      payload = json.loads(result.stdout)
      assert payload['passed'] == payload['total']

  class TestWhenSpecFileIsInvalid:
    def test_it_passes_when_spec_file_is_missing(
      self, runner: CliRunner, recorded_request: Request
    ):
      missing_path = str(MOCK_DATA_DIR / 'does-not-exist.openapi.yaml')
      result = runner.invoke(
        request,
        [
          'test',
          '--strategy', test_strategy.CONTRACT,
          '--format', 'json',
          '--openapi-specification-path', missing_path,
          recorded_request.key(),
        ],
      )
      assert result.exit_code == 0, result.stdout
      payload = json.loads(result.stdout)
      assert payload['passed'] == payload['total']

    def test_it_passes_when_spec_file_is_invalid_yaml(
      self, runner: CliRunner, recorded_request: Request, tmp_path: Path
    ):
      bad_spec = tmp_path / 'bad.openapi.yaml'
      bad_spec.write_text(':\n  - this: is: not: valid: yaml: [[[')
      result = runner.invoke(
        request,
        [
          'test',
          '--strategy', test_strategy.CONTRACT,
          '--format', 'json',
          '--openapi-specification-path', str(bad_spec),
          recorded_request.key(),
        ],
      )
      assert result.exit_code == 0, result.stdout
      payload = json.loads(result.stdout)
      assert payload['passed'] == payload['total']

  class TestWhenOtherStrategies:
    def test_diff_strategy_still_passes_with_openapi(
      self, runner: CliRunner, recorded_request: Request
    ):
      result = runner.invoke(
        request,
        [
          'test',
          '--strategy', test_strategy.DIFF,
          '--openapi-specification-path', str(DOGS_OPENAPI_PATH),
          recorded_request.key(),
        ],
      )
      assert result.exit_code == 0, result.stdout

    def test_fuzzy_strategy_still_passes_with_openapi(
      self, runner: CliRunner, recorded_request: Request
    ):
      result = runner.invoke(
        request,
        [
          'test',
          '--strategy', test_strategy.FUZZY,
          '--openapi-specification-path', str(DOGS_OPENAPI_PATH),
          recorded_request.key(),
        ],
      )
      assert result.exit_code == 0, result.stdout

  class TestWhenEndpointIdIsAttached:
    def test_matching_spec_resolves_expected_endpoint_id(self):
      found = search_open_api_endpoint(
        str(DOGS_OPENAPI_PATH),
        'GET',
        DETERMINISTIC_GET_REQUEST_URL,
      )
      assert found is not None
      assert found['id'] == EXPECTED_DOGS_ENDPOINT_ID

    def test_it_attaches_openapi_endpoint_id_on_expected_response(
      self, runner: CliRunner, recorded_request: Request
    ):
      attached_ids = []
      real_with_headers = ORMToRequestsResponseTransformer.with_headers

      def wrapping_with_headers(self, headers, merge=False):
        if custom_headers.MOCK_REQUEST_ENDPOINT_ID in headers:
          attached_ids.append(headers[custom_headers.MOCK_REQUEST_ENDPOINT_ID])
        return real_with_headers(self, headers, merge=merge)

      with patch.object(ORMToRequestsResponseTransformer, 'with_headers', wrapping_with_headers):
        result = runner.invoke(
          request,
          [
            'test',
            '--strategy', test_strategy.CONTRACT,
            '--openapi-specification-path', str(DOGS_OPENAPI_PATH),
            recorded_request.key(),
          ],
        )

      assert result.exit_code == 0, result.stdout
      assert EXPECTED_DOGS_ENDPOINT_ID in attached_ids
