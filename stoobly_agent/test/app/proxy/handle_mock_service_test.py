from unittest.mock import MagicMock, patch

import pytest

from stoobly_agent.app.proxy.constants import custom_response_codes
from stoobly_agent.app.proxy.handle_mock_service import eval_request_with_retry
from stoobly_agent.app.proxy.mock.context import MockContext


def build_context():
  flow = MagicMock()
  flow.request = MagicMock()
  intercept_settings = MagicMock()
  intercept_settings.public_directory_path = '/tmp/public'
  intercept_settings.response_fixtures_path = '/tmp/fixtures.yml'
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
