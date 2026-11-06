from unittest.mock import MagicMock, patch

from stoobly_agent.app.proxy.handle_record_service import handle_request_record, handle_response_record
from stoobly_agent.app.proxy.record.context import RecordContext
from stoobly_agent.app.proxy.replay.context import ReplayContext
from stoobly_agent.config.constants import custom_headers, lifecycle_hooks, record_policy


def build_replay_context():
  flow = MagicMock()
  flow.request = MagicMock()
  flow.response = None
  intercept_settings = MagicMock()
  intercept_settings.public_directory_path = '/tmp/public'
  intercept_settings.response_fixtures_path = '/tmp/fixtures.yml'
  intercept_settings.scenario_key = None
  intercept_settings.order_from_header = None
  intercept_settings.order = None
  intercept_settings.lifecycle_hooks = {}
  return ReplayContext(flow, intercept_settings)


def build_record_context(fixture_path=None):
  flow = MagicMock()
  flow.request = MagicMock()
  flow.response = MagicMock()
  headers = {}
  if fixture_path:
    headers[custom_headers.MOCK_FIXTURE_PATH] = fixture_path
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


class TestHandleResponseRecordFixtures:
  def test_delegates_to_mock_response_when_fixture_mocked(self):
    context = build_record_context(fixture_path='/tmp/fixtures/user.json')

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
