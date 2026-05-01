from unittest.mock import MagicMock, patch

import pytest
from mitmproxy.http import Headers, Request as MitmproxyRequest

from stoobly_agent.app.proxy.handle_normalize_service import (
    handle_request_normalize,
    handle_response_normalize,
)
from stoobly_agent.app.proxy.intercept_settings import InterceptSettings
from stoobly_agent.app.proxy.replay.context import ReplayContext
from stoobly_agent.app.settings import Settings
from stoobly_agent.app.settings.constants import filter_action
from stoobly_agent.app.settings.filter_rule import FilterRule
from stoobly_agent.app.settings.rewrite_rule import RewriteRule
from stoobly_agent.config.constants import mode, normalize_policy
from stoobly_agent.lib.api.keys.project_key import ProjectKey


@pytest.fixture
def normalize_get_request():
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
def mock_settings_with_normalize_rewrite(normalize_get_request):
    settings = MagicMock(spec=Settings)
    settings.proxy = MagicMock()
    settings.proxy.data = MagicMock()
    settings.proxy.intercept = MagicMock()
    settings.proxy.match = MagicMock()
    settings.proxy.rewrite = MagicMock()
    settings.proxy.filter = MagicMock()

    settings.proxy.intercept.project_key = ProjectKey.encode(1, 1).decode()
    settings.proxy.match.match_rules.return_value = []

    request_url = normalize_get_request.url
    rewrite = RewriteRule(
        {
            'methods': ['GET'],
            'pattern': request_url,
            'url_rules': [{'modes': [mode.NORMALIZE], 'path': '/rewritten'}],
            'parameter_rules': [],
        }
    )
    settings.proxy.rewrite.rewrite_rules.return_value = [rewrite]

    data_rules = MagicMock()
    data_rules.scenario_key = 'default_scenario_key'
    data_rules.normalize_policy = normalize_policy.ALL
    settings.proxy.data.data_rules.return_value = data_rules

    return settings, request_url


class TestHandleNormalizeServiceExcludedRequest:
    @patch('stoobly_agent.app.proxy.handle_normalize_service.rewrite_response')
    @patch('stoobly_agent.app.proxy.handle_normalize_service.rewrite_request')
    def test_excluded_request_skips_request_and_response_rewrite(
        self,
        mock_rewrite_request,
        mock_rewrite_response,
        mock_settings_with_normalize_rewrite,
        normalize_get_request,
    ):
        settings, request_url = mock_settings_with_normalize_rewrite
        settings.proxy.filter.filter_rules.return_value = [
            FilterRule(
                {
                    'action': filter_action.EXCLUDE,
                    'methods': ['GET'],
                    'modes': [mode.NORMALIZE],
                    'pattern': request_url,
                }
            )
        ]

        flow = MagicMock()
        flow.request = normalize_get_request
        flow.response = MagicMock()

        intercept_settings = InterceptSettings(settings, normalize_get_request)
        context = ReplayContext(flow, intercept_settings)

        handle_request_normalize(context)
        handle_response_normalize(context)

        mock_rewrite_request.assert_not_called()
        mock_rewrite_response.assert_not_called()

    @patch('stoobly_agent.app.proxy.handle_normalize_service.rewrite_response')
    @patch('stoobly_agent.app.proxy.handle_normalize_service.rewrite_request')
    def test_allowed_request_runs_request_and_response_rewrite(
        self,
        mock_rewrite_request,
        mock_rewrite_response,
        mock_settings_with_normalize_rewrite,
        normalize_get_request,
    ):
        settings, _request_url = mock_settings_with_normalize_rewrite
        settings.proxy.filter.filter_rules.return_value = []

        flow = MagicMock()
        flow.request = normalize_get_request
        flow.response = MagicMock()

        intercept_settings = InterceptSettings(settings, normalize_get_request)
        context = ReplayContext(flow, intercept_settings)

        handle_request_normalize(context)
        handle_response_normalize(context)

        mock_rewrite_request.assert_called_once_with(flow, intercept_settings.normalize_rewrite_rules)
        mock_rewrite_response.assert_called_once_with(
            flow,
            intercept_settings.normalize_rewrite_rules,
        )
