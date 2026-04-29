from unittest.mock import MagicMock, patch

import pytest

from stoobly_agent.app.proxy.handle_test_service import handle_request_test, handle_response_test
from stoobly_agent.config.constants import mock_policy, test_policy


class TestHandleTestService:
    @pytest.mark.parametrize('mock_policy_value', [mock_policy.NONE, mock_policy.FOUND, mock_policy.ALL])
    @patch('stoobly_agent.app.proxy.handle_test_service.handle_request_replay')
    @patch('stoobly_agent.app.proxy.handle_test_service.handle_request_mock')
    def test_handle_request_test_policy_none_uses_mock_path(self, mock_handle_request_mock, mock_handle_request_replay, mock_policy_value):
        context = MagicMock()
        context.intercept_settings.policy = test_policy.NONE
        context.intercept_settings.mock_policy = mock_policy_value

        handle_request_test(context)

        mock_handle_request_mock.assert_called_once()
        mock_handle_request_replay.assert_not_called()

    @pytest.mark.parametrize('mock_policy_value', [mock_policy.NONE, mock_policy.FOUND, mock_policy.ALL])
    @patch('stoobly_agent.app.proxy.handle_test_service.handle_request_replay')
    @patch('stoobly_agent.app.proxy.handle_test_service.handle_request_mock')
    def test_handle_request_test_policy_found_uses_replay_path(self, mock_handle_request_mock, mock_handle_request_replay, mock_policy_value):
        context = MagicMock()
        context.intercept_settings.policy = test_policy.FOUND
        context.intercept_settings.mock_policy = mock_policy_value

        handle_request_test(context)

        mock_handle_request_replay.assert_called_once_with(context)
        mock_handle_request_mock.assert_not_called()

    @patch('stoobly_agent.app.proxy.handle_test_service.handle_response_replay')
    @patch('stoobly_agent.app.proxy.handle_test_service.handle_response_mock')
    @patch('stoobly_agent.app.proxy.handle_test_service.get_intercept_mode_policy')
    def test_handle_response_test_policy_none_uses_mock_path(
        self,
        mock_get_intercept_mode_policy,
        mock_handle_response_mock,
        mock_handle_response_replay,
    ):
        flow = MagicMock()
        flow.response = MagicMock()

        intercept_settings = MagicMock()
        intercept_settings.policy = test_policy.NONE

        context = MagicMock()
        context.flow = flow
        context.intercept_settings = intercept_settings

        mock_get_intercept_mode_policy.return_value = test_policy.NONE
        handle_response_test(context)

        mock_handle_response_mock.assert_called_once()
        mock_handle_response_replay.assert_not_called()

    @pytest.mark.parametrize('mock_policy_value', [mock_policy.NONE, mock_policy.FOUND, mock_policy.ALL])
    @patch('stoobly_agent.app.proxy.handle_test_service.disable_transfer_encoding')
    @patch('stoobly_agent.app.proxy.handle_test_service.handle_response_replay')
    @patch('stoobly_agent.app.proxy.handle_test_service.handle_request_mock_generic')
    @patch('stoobly_agent.app.proxy.handle_test_service.get_intercept_mode_policy')
    def test_handle_response_test_policy_found_forces_mock_all(
        self,
        mock_get_intercept_mode_policy,
        mock_handle_request_mock_generic,
        mock_handle_response_replay,
        mock_disable_transfer_encoding,
        mock_policy_value,
    ):
        flow = MagicMock()
        flow.response = MagicMock()
        original_response = flow.response
        flow.request = MagicMock()
        flow.request.headers = {}

        flow_copy = MagicMock()
        flow_copy.request = MagicMock()
        flow_copy.request.headers = {}
        flow.copy.return_value = flow_copy

        intercept_settings = MagicMock()
        mock_get_intercept_mode_policy.side_effect = [test_policy.FOUND, mock_policy_value]

        context = MagicMock()
        context.flow = flow
        context.intercept_settings = intercept_settings

        handle_response_test(context)

        mock_disable_transfer_encoding.assert_called_once_with(original_response)
        mock_handle_response_replay.assert_called_once_with(context)
        mock_handle_request_mock_generic.assert_called_once()

        passed_mock_context = mock_handle_request_mock_generic.call_args.args[0]
        assert passed_mock_context.flow is flow_copy
