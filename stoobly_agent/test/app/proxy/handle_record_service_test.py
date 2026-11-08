import os
import time

from mitmproxy.http import Headers, Request, Response
from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow
from unittest.mock import MagicMock, patch

from stoobly_agent.app.proxy.handle_record_service import handle_request_record, handle_response_record
from stoobly_agent.app.proxy.record.context import RecordContext
from stoobly_agent.app.proxy.replay.context import ReplayContext
from stoobly_agent.app.settings.constants import intercept_mode
from stoobly_agent.app.settings.constants.mode import TEST
from stoobly_agent.config.constants import custom_headers, lifecycle_hooks, record_policy, record_strategy
from stoobly_agent.config.constants.env_vars import ENV


def build_replay_context():
  flow = MagicMock()
  flow.request = MagicMock()
  flow.response = None
  flow.metadata = {}
  intercept_settings = MagicMock()
  intercept_settings.public_directory_path = '/tmp/public'
  intercept_settings.response_fixtures_path = '/tmp/fixtures.yml'
  intercept_settings.scenario_key = None
  intercept_settings.order_from_header = None
  intercept_settings.order = None
  intercept_settings.lifecycle_hooks = {}
  return ReplayContext(flow, intercept_settings)


def build_record_context(fixture_mocked=False, fixture_path=None):
  flow = MagicMock()
  flow.request = MagicMock()
  flow.response = MagicMock()
  flow.metadata = {}
  headers = {}
  if fixture_path:
    headers[custom_headers.MOCK_FIXTURE_PATH] = fixture_path
  if fixture_mocked:
    flow.metadata['stoobly_fixture_mocked'] = True
  flow.response.headers = headers
  intercept_settings = MagicMock()
  intercept_settings.lifecycle_hooks = {}
  intercept_settings.settings = MagicMock()
  return RecordContext(flow, intercept_settings)


class TestHandleRequestRecordFixtures:
  def test_applies_fixture_and_fires_before_mock(self):
    context = build_replay_context()
    before_mock = MagicMock()
    context.intercept_settings.lifecycle_hooks = {
      lifecycle_hooks.BEFORE_MOCK: before_mock,
    }
    fixture = MagicMock(status_code=200, content=b'fixture')

    with patch(
      'stoobly_agent.app.proxy.handle_record_service.handle_request_develop'
    ), patch(
      'stoobly_agent.app.proxy.handle_record_service.eval_fixtures',
      return_value=fixture,
    ) as eval_fixtures_mock, patch(
      'stoobly_agent.app.proxy.handle_record_service.apply_response'
    ) as apply_response_mock, patch(
      'stoobly_agent.app.proxy.handle_record_service.handle_mock_success'
    ) as handle_mock_success_mock:
      handle_request_record(context)

    eval_fixtures_mock.assert_called_once_with(
      context.flow.request,
      public_directory_path='/tmp/public',
      response_fixtures_path='/tmp/fixtures.yml',
      scenario_key=None,
    )
    before_mock.assert_called_once()
    apply_response_mock.assert_called_once_with(context.flow, fixture)
    handle_mock_success_mock.assert_called_once()
    assert context.flow.metadata.get('stoobly_fixture_mocked') is True

  def test_skips_mock_lifecycle_when_no_fixture(self):
    context = build_replay_context()
    before_mock = MagicMock()
    context.intercept_settings.lifecycle_hooks = {
      lifecycle_hooks.BEFORE_MOCK: before_mock,
    }

    with patch(
      'stoobly_agent.app.proxy.handle_record_service.handle_request_develop'
    ), patch(
      'stoobly_agent.app.proxy.handle_record_service.eval_fixtures',
      return_value=None,
    ), patch(
      'stoobly_agent.app.proxy.handle_record_service.apply_response'
    ) as apply_response_mock, patch(
      'stoobly_agent.app.proxy.handle_record_service.handle_mock_success'
    ) as handle_mock_success_mock:
      handle_request_record(context)

    before_mock.assert_not_called()
    apply_response_mock.assert_not_called()
    handle_mock_success_mock.assert_not_called()
    assert 'stoobly_fixture_mocked' not in context.flow.metadata


class TestHandleResponseRecordFixtures:
  def test_delegates_to_mock_response_when_fixture_mocked(self):
    context = build_record_context(fixture_mocked=True)

    with patch(
      'stoobly_agent.app.proxy.handle_record_service.handle_response_mock'
    ) as handle_response_mock_mock, patch(
      'stoobly_agent.app.proxy.handle_record_service.handle_response_develop'
    ) as handle_response_develop_mock, patch(
      'stoobly_agent.app.proxy.handle_record_service.__record_request'
    ) as record_request_mock:
      handle_response_record(context)

    handle_response_mock_mock.assert_called_once()
    handle_response_develop_mock.assert_not_called()
    record_request_mock.assert_not_called()

  def test_records_when_upstream_sets_fixture_path_header(self):
    """Upstream (e.g. chained mock agent) may set X-Stoobly-Fixture-Path; still record."""
    context = build_record_context(fixture_path='/tmp/fixtures/user.json')

    with patch(
      'stoobly_agent.app.proxy.handle_record_service.disable_transfer_encoding'
    ), patch(
      'stoobly_agent.app.proxy.handle_record_service.handle_response_develop'
    ), patch(
      'stoobly_agent.app.proxy.handle_record_service.handle_response_mock'
    ) as handle_response_mock_mock, patch(
      'stoobly_agent.app.proxy.handle_record_service.RequestModel'
    ), patch(
      'stoobly_agent.app.proxy.handle_record_service.get_intercept_mode_policy',
      return_value=record_policy.ALL,
    ), patch(
      'stoobly_agent.app.proxy.handle_record_service.__record_request'
    ) as record_request_mock:
      handle_response_record(context)

    handle_response_mock_mock.assert_not_called()
    record_request_mock.assert_called_once()

  def test_records_when_not_fixture_mocked(self):
    context = build_record_context()

    with patch(
      'stoobly_agent.app.proxy.handle_record_service.disable_transfer_encoding'
    ), patch(
      'stoobly_agent.app.proxy.handle_record_service.handle_response_develop'
    ), patch(
      'stoobly_agent.app.proxy.handle_record_service.handle_response_mock'
    ) as handle_response_mock_mock, patch(
      'stoobly_agent.app.proxy.handle_record_service.RequestModel'
    ), patch(
      'stoobly_agent.app.proxy.handle_record_service.get_intercept_mode_policy',
      return_value=record_policy.ALL,
    ), patch(
      'stoobly_agent.app.proxy.handle_record_service.__record_request'
    ) as record_request_mock:
      handle_response_record(context)

    handle_response_mock_mock.assert_not_called()
    record_request_mock.assert_called_once()


def build_real_record_context(strategy: str):
  flow = MitmproxyHTTPFlow(client_conn=None, server_conn=None)
  flow.request = Request(
    host="api.example.com",
    port=443,
    method="POST",
    scheme="https",
    authority="api.example.com",
    path="/api/v1/data",
    http_version="HTTP/1.1",
    headers=Headers([
      (b"Host", b"api.example.com"),
      (b"Origin", b"https://example.com"),
      (b"Content-Type", b"application/json"),
      (b"Authorization", b"Bearer token123"),
      (b"Cookie", b"session=abc123"),
      (b"Access-Control-Request-Method", b"POST"),
    ]),
    content=b'{"data": "test"}',
    trailers=None,
    timestamp_start=time.time(),
    timestamp_end=time.time() + 1,
  )
  flow.response = Response(
    http_version="HTTP/1.1",
    status_code=200,
    reason="OK",
    headers=Headers([
      (b"Content-Type", b"application/json"),
      (b"Access-Control-Allow-Origin", b"https://example.com"),
      (b"Access-Control-Allow-Credentials", b"true"),
      (b"Set-Cookie", b"session=new"),
    ]),
    content=b'{"ok": true}',
    trailers=None,
    timestamp_start=time.time(),
    timestamp_end=time.time() + 1,
  )

  intercept_settings = MagicMock()
  intercept_settings.mode = intercept_mode.RECORD
  intercept_settings.record_strategy = strategy
  intercept_settings.record_rewrite_rules = []
  intercept_settings.lifecycle_hooks = {}
  return RecordContext(flow, intercept_settings)


def record_and_capture_uploaded_flow(context: RecordContext):
  """Runs the real record path and returns the flow handed to the upload step."""
  upload = MagicMock()

  with patch.dict(os.environ, {ENV: TEST}), patch(
    'stoobly_agent.app.proxy.handle_record_service.disable_transfer_encoding'
  ), patch(
    'stoobly_agent.app.proxy.handle_record_service.handle_response_develop'
  ), patch(
    'stoobly_agent.app.proxy.handle_record_service.RequestModel'
  ), patch(
    'stoobly_agent.app.proxy.handle_record_service.get_intercept_mode_policy',
    return_value=record_policy.ALL,
  ), patch(
    'stoobly_agent.app.proxy.handle_record_service.inject_upload_request',
    return_value=upload,
  ):
    handle_response_record(context)

  upload.assert_called_once()
  return upload.call_args.args[0]


class TestHandleResponseRecordStrategy:
  def test_minimal_strategy_minimizes_recorded_request_headers_only(self):
    context = build_real_record_context(record_strategy.MINIMAL)
    original_request_headers = list(context.flow.request.headers.items())
    original_response_headers = list(context.flow.response.headers.items())

    recorded_flow = record_and_capture_uploaded_flow(context)

    # Request headers are reduced to the allowlist
    assert list(recorded_flow.request.headers.keys()) == ["Host", "Origin", "Content-Type"]
    assert "Authorization" not in recorded_flow.request.headers
    assert "Cookie" not in recorded_flow.request.headers
    assert "Access-Control-Request-Method" not in recorded_flow.request.headers

    # Response headers, including access control, are recorded as-is
    assert list(recorded_flow.response.headers.items()) == original_response_headers
    assert "Access-Control-Allow-Origin" in recorded_flow.response.headers
    assert "Access-Control-Allow-Credentials" in recorded_flow.response.headers

    # Only the recorded copy is minimized, not the flow returned to the client
    assert list(context.flow.request.headers.items()) == original_request_headers

  def test_full_strategy_records_all_headers(self):
    context = build_real_record_context(record_strategy.FULL)
    original_request_headers = list(context.flow.request.headers.items())
    original_response_headers = list(context.flow.response.headers.items())

    recorded_flow = record_and_capture_uploaded_flow(context)

    assert list(recorded_flow.request.headers.items()) == original_request_headers
    assert list(recorded_flow.response.headers.items()) == original_response_headers
