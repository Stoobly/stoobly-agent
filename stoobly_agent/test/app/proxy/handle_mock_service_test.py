from unittest.mock import MagicMock, patch

import pytest
from mitmproxy.http import Response as MitmproxyResponse

from stoobly_agent.app.proxy.constants import custom_response_codes
from stoobly_agent.app.proxy.handle_mock_service import eval_request_with_retry, handle_mock_failure
from stoobly_agent.app.proxy.mock.context import MockContext
from stoobly_agent.app.proxy.mock.custom_not_found_response_builder import CustomNotFoundResponseBuilder
from stoobly_agent.app.proxy.utils.response_handler import CORS_HEADERS, cors_headers


def build_context():
  flow = MagicMock()
  flow.request = MagicMock()
  intercept_settings = MagicMock()
  intercept_settings.public_directory_path = '/tmp/public'
  intercept_settings.response_fixtures_path = '/tmp/fixtures.yml'
  intercept_settings.scenario_key = None
  return MockContext(flow, intercept_settings)


class TestEvalRequestWithRetry:
  def test_retries_after_ignore_components_with_appended_content(self):
    context = build_context()
    ignore_body = b'[{"type":3,"name":"b"}]'
    first = MagicMock(status_code=custom_response_codes.IGNORE_COMPONENTS, content=ignore_body)
    second = MagicMock(status_code=200, content=b'ok')
    seen = []

    def eval_request(request, ignored_components, **kwargs):
      seen.append((request, list(ignored_components), dict(kwargs)))
      return first if len(seen) == 1 else second

    res = eval_request_with_retry(context, eval_request, ignored_components=[], infer=True)

    assert res is second
    assert len(seen) == 2
    assert seen[0][0] is context.flow.request
    assert seen[0][1] == []
    assert seen[0][2] == {}
    assert seen[1][0] is context.flow.request
    assert seen[1][1] == [ignore_body]
    assert seen[1][2] == {'infer': True, 'retry': 1}

  def test_replaces_not_found_with_fixture(self):
    context = build_context()
    not_found = MagicMock(status_code=custom_response_codes.NOT_FOUND)
    fixture = MagicMock(status_code=200, content=b'fixture')
    eval_request = MagicMock(return_value=not_found)

    with patch(
      'stoobly_agent.app.proxy.handle_mock_service.eval_fixtures',
      return_value=fixture,
    ) as eval_fixtures:
      res = eval_request_with_retry(context, eval_request)

    assert res is fixture
    eval_fixtures.assert_called_once_with(
      context.flow.request,
      public_directory_path='/tmp/public',
      response_fixtures_path='/tmp/fixtures.yml',
      scenario_key=context.intercept_settings.scenario_key,
    )

  def test_keeps_not_found_when_no_fixture(self):
    context = build_context()
    not_found = MagicMock(status_code=custom_response_codes.NOT_FOUND)
    eval_request = MagicMock(return_value=not_found)

    with patch(
      'stoobly_agent.app.proxy.handle_mock_service.eval_fixtures',
      return_value=None,
    ):
      res = eval_request_with_retry(context, eval_request)

    assert res is not_found


class TestCustomNotFoundResponseBuilder:
  def test_includes_cors_headers(self):
    res = CustomNotFoundResponseBuilder().build()

    assert res.status_code == custom_response_codes.NOT_FOUND
    for header, value in CORS_HEADERS.items():
      assert res.headers[header] == value

  def test_includes_cors_headers_with_origin(self):
    origin = 'https://app.example.com'
    res = CustomNotFoundResponseBuilder().build(origin)

    assert res.status_code == custom_response_codes.NOT_FOUND
    for header, value in cors_headers(origin).items():
      assert res.headers[header] == value


class TestHandleMockFailureCors:
  def test_applies_cors_headers_to_not_found_response(self):
    origin = 'https://app.example.com'
    flow = MagicMock()
    flow.request = MagicMock()
    flow.request.method = 'GET'
    flow.request.headers = {'Origin': origin}
    flow.response = MitmproxyResponse.make(
      custom_response_codes.NOT_FOUND,
      b'Request not found',
      {'Content-Type': 'text/plain'},
    )
    context = MockContext(flow, MagicMock())

    with patch('stoobly_agent.app.proxy.handle_mock_service.InterceptedRequestsLogger'):
      handle_mock_failure(context)

    for header, value in cors_headers(origin).items():
      assert flow.response.headers[header] == value
    assert flow.response.status_code == custom_response_codes.NOT_FOUND

  def test_options_replaces_response_with_cors_200(self):
    origin = 'https://app.example.com'
    requested_headers = 'content-type, authorization, x-custom'
    flow = MagicMock()
    flow.request = MagicMock()
    flow.request.method = 'OPTIONS'
    flow.request.headers = {
      'Origin': origin,
      'Access-Control-Request-Headers': requested_headers,
    }
    flow.response = MitmproxyResponse.make(
      custom_response_codes.NOT_FOUND,
      b'Request not found',
      {'Content-Type': 'text/plain'},
    )
    context = MockContext(flow, MagicMock())

    with patch('stoobly_agent.app.proxy.handle_mock_service.InterceptedRequestsLogger'):
      handle_mock_failure(context)

    assert flow.response.status_code == 200
    for header, value in cors_headers(origin, flow.request.headers).items():
      assert flow.response.headers[header] == value
    assert flow.response.headers['Access-Control-Allow-Headers'] == requested_headers
