from unittest.mock import MagicMock, PropertyMock, patch

import pytest
from mitmproxy.http import Headers, Request as MitmproxyRequest

from stoobly_agent.app.proxy.handle_develop_service import (
    handle_request_develop,
    handle_request_develop_without_rewrite,
    handle_response_develop,
)
from stoobly_agent.config.constants import lifecycle_hooks as lc_hooks
from stoobly_agent.app.proxy.intercept_settings import InterceptSettings
from stoobly_agent.app.proxy.replay.context import ReplayContext
from stoobly_agent.app.settings import Settings
from stoobly_agent.app.settings.constants import filter_action
from stoobly_agent.app.settings.filter_rule import FilterRule
from stoobly_agent.app.settings.rewrite_rule import RewriteRule
from stoobly_agent.config.constants import mode, develop_policy
from stoobly_agent.lib.api.keys.project_key import ProjectKey


@pytest.fixture
def develop_get_request():
    return MitmproxyRequest(
        'example.com',
        443,
        b'GET',
        b'https',
        b'example.com:443',
        b'/test',
        b'HTTP/1.1',
        Headers(),
        b'',
        Headers(),
        0,
        0,
    )


@pytest.fixture
def mock_settings_with_develop_rewrite(develop_get_request):
    settings = MagicMock(spec=Settings)
    settings.proxy = MagicMock()
    settings.proxy.data = MagicMock()
    settings.proxy.intercept = MagicMock()
    settings.proxy.match = MagicMock()
    settings.proxy.rewrite = MagicMock()
    settings.proxy.filter = MagicMock()

    settings.proxy.intercept.project_key = ProjectKey.encode(1, 1).decode()
    settings.proxy.match.match_rules.return_value = []

    request_url = develop_get_request.url
    rewrite = RewriteRule(
        {
            'methods': ['GET'],
            'pattern': request_url,
            'url_rules': [{'modes': [mode.DEVELOP], 'path': '/rewritten'}],
            'parameter_rules': [],
        }
    )
    settings.proxy.rewrite.rewrite_rules.return_value = [rewrite]

    data_rules = MagicMock()
    data_rules.scenario_key = 'default_scenario_key'
    data_rules.develop_policy = develop_policy.ALL
    settings.proxy.data.data_rules.return_value = data_rules

    return settings, request_url


class TestHandleDevelopServiceExcludedRequest:
    @patch('stoobly_agent.app.proxy.handle_develop_service.rewrite_response')
    @patch('stoobly_agent.app.proxy.handle_develop_service.rewrite_request')
    def test_excluded_request_skips_request_and_response_rewrite(
        self,
        mock_rewrite_request,
        mock_rewrite_response,
        mock_settings_with_develop_rewrite,
        develop_get_request,
    ):
        settings, request_url = mock_settings_with_develop_rewrite
        settings.proxy.filter.filter_rules.return_value = [
            FilterRule(
                {
                    'action': filter_action.EXCLUDE,
                    'methods': ['GET'],
                    'modes': [mode.DEVELOP],
                    'pattern': request_url,
                }
            )
        ]

        flow = MagicMock()
        flow.request = develop_get_request
        flow.response = MagicMock()

        intercept_settings = InterceptSettings(settings, develop_get_request)
        context = ReplayContext(flow, intercept_settings)

        handle_request_develop(context)
        handle_response_develop(context)

        mock_rewrite_request.assert_not_called()
        mock_rewrite_response.assert_not_called()

    @patch('stoobly_agent.app.proxy.handle_develop_service.rewrite_response')
    @patch('stoobly_agent.app.proxy.handle_develop_service.rewrite_request')
    def test_allowed_request_runs_request_and_response_rewrite(
        self,
        mock_rewrite_request,
        mock_rewrite_response,
        mock_settings_with_develop_rewrite,
        develop_get_request,
    ):
        settings, _request_url = mock_settings_with_develop_rewrite
        settings.proxy.filter.filter_rules.return_value = []

        flow = MagicMock()
        flow.request = develop_get_request
        flow.response = MagicMock()

        intercept_settings = InterceptSettings(settings, develop_get_request)
        context = ReplayContext(flow, intercept_settings)

        handle_request_develop(context)
        handle_response_develop(context)

        mock_rewrite_request.assert_called_once_with(
            flow,
            intercept_settings.develop_rewrite_rules,
            mode=mode.DEVELOP,
        )
        mock_rewrite_response.assert_called_once_with(
            flow,
            intercept_settings.develop_rewrite_rules,
            mode=mode.DEVELOP,
        )


class TestHandleDevelopServiceLifecycleHooks:

    def _make_context(self, settings, develop_get_request, lifecycle_hooks_dict):
        flow = MagicMock()
        flow.request = develop_get_request
        flow.response = MagicMock()
        intercept_settings = InterceptSettings(settings, develop_get_request)
        with patch.object(type(intercept_settings), 'lifecycle_hooks', new_callable=PropertyMock) as mock_lc:
            mock_lc.return_value = lifecycle_hooks_dict
            return ReplayContext(flow, intercept_settings), intercept_settings, mock_lc

    @patch.object(InterceptSettings, 'lifecycle_hooks', new_callable=PropertyMock)
    def test_before_develop_hook_called_for_allowed_request(self, mock_lc, mock_settings_with_develop_rewrite, develop_get_request):
        settings, _ = mock_settings_with_develop_rewrite
        settings.proxy.filter.filter_rules.return_value = []

        mock_hook = MagicMock()
        mock_lc.return_value = {lc_hooks.BEFORE_DEVELOP: mock_hook}

        flow = MagicMock()
        flow.request = develop_get_request
        intercept_settings = InterceptSettings(settings, develop_get_request)
        context = ReplayContext(flow, intercept_settings)

        handle_request_develop(context)

        mock_hook.assert_called_once_with(context)

    @patch.object(InterceptSettings, 'lifecycle_hooks', new_callable=PropertyMock)
    def test_after_develop_hook_called_for_allowed_response(self, mock_lc, mock_settings_with_develop_rewrite, develop_get_request):
        settings, _ = mock_settings_with_develop_rewrite
        settings.proxy.filter.filter_rules.return_value = []

        mock_hook = MagicMock()
        mock_lc.return_value = {lc_hooks.AFTER_DEVELOP: mock_hook}

        flow = MagicMock()
        flow.request = develop_get_request
        flow.response = MagicMock()
        intercept_settings = InterceptSettings(settings, develop_get_request)
        context = ReplayContext(flow, intercept_settings)

        handle_response_develop(context)

        mock_hook.assert_called_once_with(context)

    @patch.object(InterceptSettings, 'lifecycle_hooks', new_callable=PropertyMock)
    def test_hooks_not_called_for_excluded_request(self, mock_lc, mock_settings_with_develop_rewrite, develop_get_request):
        settings, request_url = mock_settings_with_develop_rewrite
        settings.proxy.filter.filter_rules.return_value = [
            FilterRule({
                'action': filter_action.EXCLUDE,
                'methods': ['GET'],
                'modes': [mode.DEVELOP],
                'pattern': request_url,
            })
        ]

        before_hook = MagicMock()
        after_hook = MagicMock()
        mock_lc.return_value = {
            lc_hooks.BEFORE_DEVELOP: before_hook,
            lc_hooks.AFTER_DEVELOP: after_hook,
        }

        flow = MagicMock()
        flow.request = develop_get_request
        flow.response = MagicMock()
        intercept_settings = InterceptSettings(settings, develop_get_request)
        context = ReplayContext(flow, intercept_settings)

        handle_request_develop(context)
        handle_response_develop(context)

        before_hook.assert_not_called()
        after_hook.assert_not_called()

    @patch.object(InterceptSettings, 'lifecycle_hooks', new_callable=PropertyMock)
    def test_unregistered_hook_is_silently_skipped(self, mock_lc, mock_settings_with_develop_rewrite, develop_get_request):
        settings, _ = mock_settings_with_develop_rewrite
        settings.proxy.filter.filter_rules.return_value = []

        mock_lc.return_value = {}  # no hooks registered

        flow = MagicMock()
        flow.request = develop_get_request
        flow.response = MagicMock()
        intercept_settings = InterceptSettings(settings, develop_get_request)
        context = ReplayContext(flow, intercept_settings)

        # should not raise
        handle_request_develop(context)
        handle_response_develop(context)


class TestHandleRequestDevelopWithoutRewrite:

    @patch('stoobly_agent.app.proxy.handle_develop_service.rewrite_request')
    @patch.object(InterceptSettings, 'lifecycle_hooks', new_callable=PropertyMock)
    def test_skips_rewrite_but_fires_before_develop_hook(self, mock_lc, mock_rewrite_request, mock_settings_with_develop_rewrite, develop_get_request):
        settings, _ = mock_settings_with_develop_rewrite
        settings.proxy.filter.filter_rules.return_value = []

        mock_hook = MagicMock()
        mock_lc.return_value = {lc_hooks.BEFORE_DEVELOP: mock_hook}

        flow = MagicMock()
        flow.request = develop_get_request
        intercept_settings = InterceptSettings(settings, develop_get_request)
        context = ReplayContext(flow, intercept_settings)

        handle_request_develop_without_rewrite(context)

        mock_rewrite_request.assert_not_called()
        mock_hook.assert_called_once_with(context)


class TestHandleDevelopServiceNoRewriteRules:

    @patch('stoobly_agent.app.proxy.handle_develop_service.rewrite_response')
    @patch('stoobly_agent.app.proxy.handle_develop_service.rewrite_request')
    def test_rewrite_not_called_when_rules_empty(self, mock_rewrite_request, mock_rewrite_response, mock_settings_with_develop_rewrite, develop_get_request):
        settings, _ = mock_settings_with_develop_rewrite
        settings.proxy.filter.filter_rules.return_value = []
        settings.proxy.rewrite.rewrite_rules.return_value = []

        flow = MagicMock()
        flow.request = develop_get_request
        flow.response = MagicMock()
        intercept_settings = InterceptSettings(settings, develop_get_request)
        context = ReplayContext(flow, intercept_settings)

        handle_request_develop(context)
        handle_response_develop(context)

        mock_rewrite_request.assert_not_called()
        mock_rewrite_response.assert_not_called()
