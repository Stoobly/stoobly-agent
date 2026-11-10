from unittest.mock import MagicMock, patch

import pytest

from stoobly_agent.app.proxy import handle_test_service as handle_test_service_module
from stoobly_agent.app.proxy.handle_test_service import handle_request_test, handle_response_test
from stoobly_agent.config.constants import mock_policy, test_policy, test_strategy

append_test_report = getattr(handle_test_service_module, '__append_test_report')


class TestAppendTestReport:
    @patch('stoobly_agent.app.proxy.handle_test_service.InterceptedRequestsLogger.append_test_report', return_value=7)
    def test_omits_expected_fields_for_contract_failure(self, mock_append_test_report):
        test_context = MagicMock()
        test_context.flow.request = MagicMock()
        test_context.flow.response = MagicMock()

        append_test_report(
            test_context,
            passed=False,
            skipped=False,
            strategy=test_strategy.CONTRACT,
            log='missing required property',
            expected={'a': 1},
            expected_latency=10,
            expected_status_code=200,
        )

        kwargs = mock_append_test_report.call_args.kwargs
        assert kwargs['passed'] is False
        assert kwargs['strategy'] == test_strategy.CONTRACT
        assert 'expected_response' not in kwargs
        assert 'expected_latency' not in kwargs
        assert 'expected_status_code' not in kwargs
        test_context.with_request_log_row_id.assert_called_once_with(7)

    @patch('stoobly_agent.app.proxy.handle_test_service.InterceptedRequestsLogger.append_test_report', return_value=8)
    def test_includes_expected_fields_for_diff_failure(self, mock_append_test_report):
        test_context = MagicMock()
        test_context.flow.request = MagicMock()
        test_context.flow.response = MagicMock()

        append_test_report(
            test_context,
            passed=False,
            skipped=False,
            strategy=test_strategy.DIFF,
            log='mismatch',
            expected={'a': 1},
            expected_latency=10,
            expected_status_code=200,
        )

        kwargs = mock_append_test_report.call_args.kwargs
        assert kwargs['expected_response'] == {'format': 'json', 'data': {'a': 1}}
        assert kwargs['expected_latency'] == 10
        assert kwargs['expected_status_code'] == 200


class TestHandleTestService:
    @pytest.mark.parametrize('mock_policy_value', [mock_policy.NONE, mock_policy.FOUND, mock_policy.ALL])
    @patch('stoobly_agent.app.proxy.handle_test_service.handle_request_develop')
    @patch('stoobly_agent.app.proxy.handle_test_service.handle_request_mock')
    def test_handle_request_test_policy_none_uses_mock_path(self, mock_handle_request_mock, mock_handle_request_develop, mock_policy_value):
        context = MagicMock()
        context.intercept_settings.policy = test_policy.NONE
        context.intercept_settings.mock_policy = mock_policy_value

        handle_request_test(context)

        mock_handle_request_mock.assert_called_once()
        mock_handle_request_develop.assert_not_called()

    @pytest.mark.parametrize('mock_policy_value', [mock_policy.NONE, mock_policy.FOUND, mock_policy.ALL])
    @patch('stoobly_agent.app.proxy.handle_test_service.handle_request_develop')
    @patch('stoobly_agent.app.proxy.handle_test_service.handle_request_mock')
    def test_handle_request_test_policy_found_uses_develop_path(self, mock_handle_request_mock, mock_handle_request_develop, mock_policy_value):
        context = MagicMock()
        context.intercept_settings.policy = test_policy.FOUND
        context.intercept_settings.mock_policy = mock_policy_value

        handle_request_test(context)

        mock_handle_request_develop.assert_called_once_with(context)
        mock_handle_request_mock.assert_not_called()

    @patch('stoobly_agent.app.proxy.handle_test_service.handle_response_develop')
    @patch('stoobly_agent.app.proxy.handle_test_service.handle_response_mock')
    @patch('stoobly_agent.app.proxy.handle_test_service.get_intercept_mode_policy')
    def test_handle_response_test_policy_none_uses_mock_path(
        self,
        mock_get_intercept_mode_policy,
        mock_handle_response_mock,
        mock_handle_response_develop,
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
        mock_handle_response_develop.assert_not_called()

    @pytest.mark.parametrize('mock_policy_value', [mock_policy.NONE, mock_policy.FOUND, mock_policy.ALL])
    @patch('stoobly_agent.app.proxy.handle_test_service.disable_transfer_encoding')
    @patch('stoobly_agent.app.proxy.handle_test_service.handle_response_develop')
    @patch('stoobly_agent.app.proxy.handle_test_service.handle_request_mock_generic')
    @patch('stoobly_agent.app.proxy.handle_test_service.get_intercept_mode_policy')
    def test_handle_response_test_policy_found_forces_mock_all(
        self,
        mock_get_intercept_mode_policy,
        mock_handle_request_mock_generic,
        mock_handle_response_develop,
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
        mock_handle_response_develop.assert_called_once_with(context)
        mock_handle_request_mock_generic.assert_called_once()

        passed_mock_context = mock_handle_request_mock_generic.call_args.args[0]
        assert passed_mock_context.flow is flow_copy
