import json
from unittest.mock import MagicMock, patch

import pytest
from mitmproxy.http import Headers, Request as MitmproxyRequest

from stoobly_agent.app.proxy.mock.eval_request_service import eval_request
from stoobly_agent.app.settings.constants import request_component
from stoobly_agent.app.settings.match_rule import MatchRule
from stoobly_agent.config.constants import custom_headers, mode, query_params as request_query_params


def build_request(
  method: bytes = b'GET',
  path: bytes = b'/v1/items?role=user',
  headers: Headers = None,
  content: bytes = b'',
  host: str = 'example.com',
  port: int = 443,
  scheme: bytes = b'https',
):
  headers = headers if headers is not None else Headers(Accept='application/json')
  authority = f'{host}:{port}'.encode()
  return MitmproxyRequest(
    host,
    port,
    method,
    scheme,
    authority,
    path,
    b'HTTP/1.1',
    headers,
    content,
    Headers(),
    0,
    0,
  )


def build_match_rule(components, pattern='.*', methods=None):
  return MatchRule({
    'components': components,
    'methods': methods or ['GET', 'POST'],
    'modes': [mode.MOCK],
    'pattern': pattern,
  })


def build_intercept_settings(match_rules=None, openapi_specification_path=None):
  intercept_settings = MagicMock()
  intercept_settings.scenario_key = None
  intercept_settings.request_id = None
  intercept_settings.project_key = None
  intercept_settings.mock_match_rules = match_rules or []
  intercept_settings.is_remote = False
  intercept_settings.parsed_remote_project_key = None
  intercept_settings.openapi_specification_path = openapi_specification_path
  return intercept_settings


def build_request_model(response_mock=None):
  request_model = MagicMock()
  request_model.is_local = True
  request_model.response = response_mock or MagicMock(return_value=MagicMock(status_code=200))
  return request_model


def response_kwargs(request_model: MagicMock) -> dict:
  assert request_model.response.called
  return request_model.response.call_args.kwargs


class TestEvalRequest:
  def test_no_match_rules_drops_hashes_and_attaches_live_query_params(self):
    request = build_request()
    request_model = build_request_model()
    intercept_settings = build_intercept_settings([])

    eval_request(request_model, intercept_settings, request, [])

    kwargs = response_kwargs(request_model)
    assert 'headers_hash' not in kwargs
    assert 'query_params_hash' not in kwargs
    assert 'body_params_hash' not in kwargs
    assert 'body_text_hash' not in kwargs
    assert kwargs[request_query_params.QUERY_PARAMS] == {'role': 'user'}
    assert request_query_params.SEQUENCE_ID not in kwargs
    assert kwargs['host'] == 'example.com'
    assert kwargs['path'] == '/v1/items'
    assert kwargs['method'] == 'GET'

  def test_allowlist_query_param_keeps_query_hash_without_live_query_params(self):
    request = build_request()
    request_model = build_request_model()
    intercept_settings = build_intercept_settings([
      build_match_rule([request_component.QUERY_PARAM]),
    ])

    eval_request(request_model, intercept_settings, request, [])

    kwargs = response_kwargs(request_model)
    assert 'query_params_hash' in kwargs
    assert kwargs['query_params_hash']
    assert 'headers_hash' not in kwargs
    assert 'body_params_hash' not in kwargs
    assert 'body_text_hash' not in kwargs
    assert request_query_params.QUERY_PARAMS not in kwargs

  def test_allowlist_header_keeps_header_hash_and_live_query_params(self):
    request = build_request()
    request_model = build_request_model()
    intercept_settings = build_intercept_settings([
      build_match_rule([request_component.HEADER]),
    ])

    eval_request(request_model, intercept_settings, request, [])

    kwargs = response_kwargs(request_model)
    assert 'headers_hash' in kwargs
    assert kwargs['headers_hash']
    assert 'query_params_hash' not in kwargs
    assert kwargs[request_query_params.QUERY_PARAMS] == {'role': 'user'}

  def test_allowlist_body_param_keeps_body_hash_without_body_tiebreak(self):
    body = json.dumps({'name': 'fido'}).encode()
    request = build_request(
      method=b'POST',
      path=b'/v1/pets',
      headers=Headers(**{'Content-Type': 'application/json', 'Accept': 'application/json'}),
      content=body,
    )
    request_model = build_request_model()
    intercept_settings = build_intercept_settings([
      build_match_rule([request_component.BODY_PARAM], methods=['POST']),
    ])

    eval_request(request_model, intercept_settings, request, [])

    kwargs = response_kwargs(request_model)
    assert 'body_params_hash' in kwargs
    assert kwargs['body_params_hash']
    assert 'body_text_hash' not in kwargs
    assert 'headers_hash' not in kwargs
    assert 'query_params_hash' not in kwargs
    assert request_query_params.QUERY_PARAMS not in kwargs
    # Body is never passed as a live tiebreak param
    assert 'body' not in kwargs
    assert 'body_params' not in kwargs

  def test_overlapping_rules_last_wins(self):
    request = build_request()
    request_model = build_request_model()
    intercept_settings = build_intercept_settings([
      build_match_rule([request_component.QUERY_PARAM]),
      build_match_rule([request_component.HEADER]),
    ])

    eval_request(request_model, intercept_settings, request, [])

    kwargs = response_kwargs(request_model)
    assert 'headers_hash' in kwargs
    assert 'query_params_hash' not in kwargs
    assert kwargs[request_query_params.QUERY_PARAMS] == {'role': 'user'}

  def test_non_matching_pattern_behaves_like_no_rules(self):
    request = build_request()
    request_model = build_request_model()
    intercept_settings = build_intercept_settings([
      build_match_rule([request_component.HEADER, request_component.QUERY_PARAM], pattern='https://other\\.com/.*'),
    ])

    eval_request(request_model, intercept_settings, request, [])

    kwargs = response_kwargs(request_model)
    assert 'headers_hash' not in kwargs
    assert 'query_params_hash' not in kwargs
    assert kwargs[request_query_params.QUERY_PARAMS] == {'role': 'user'}

  def test_request_sequence_id_header_attaches_sequence_id(self):
    request = build_request(
      headers=Headers(**{
        'Accept': 'application/json',
        custom_headers.REQUEST_SEQUENCE_ID: '7',
      }),
    )
    request_model = build_request_model()
    intercept_settings = build_intercept_settings([])

    eval_request(request_model, intercept_settings, request, [])

    kwargs = response_kwargs(request_model)
    assert kwargs[request_query_params.SEQUENCE_ID] == 7

  def test_compute_attached_on_retry_with_ignored_components_and_endpoint(self):
    request = build_request()
    request_model = build_request_model()
    intercept_settings = build_intercept_settings(
      match_rules=[build_match_rule([request_component.QUERY_PARAM])],
      openapi_specification_path='/tmp/openapi.yaml',
    )
    ignored = [{'type': 3, 'name': 'role'}]
    search = MagicMock(return_value={'id': 'ep-1', 'ignored_components': ignored})

    with patch(
      'stoobly_agent.app.proxy.mock.eval_request_service.inject_search_open_api_endpoint',
      return_value=search,
    ):
      eval_request(request_model, intercept_settings, request, ignored, retry=1)

    kwargs = response_kwargs(request_model)
    assert kwargs[request_query_params.COMPUTE] == '1'
    assert request_query_params.ENDPOINT_PROMISE in kwargs
    assert kwargs['retry'] == 1

  def test_compute_not_attached_without_retry(self):
    request = build_request()
    request_model = build_request_model()
    intercept_settings = build_intercept_settings(
      match_rules=[build_match_rule([request_component.QUERY_PARAM])],
      openapi_specification_path='/tmp/openapi.yaml',
    )
    ignored = [{'type': 3, 'name': 'role'}]
    search = MagicMock(return_value={'id': 'ep-1', 'ignored_components': ignored})

    with patch(
      'stoobly_agent.app.proxy.mock.eval_request_service.inject_search_open_api_endpoint',
      return_value=search,
    ):
      eval_request(request_model, intercept_settings, request, ignored)

    kwargs = response_kwargs(request_model)
    assert request_query_params.COMPUTE not in kwargs
    assert request_query_params.ENDPOINT_PROMISE in kwargs
