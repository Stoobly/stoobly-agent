import pytest
from unittest.mock import MagicMock

from mitmproxy.http import Headers

from stoobly_agent.app.proxy import settings as proxy_settings
from stoobly_agent.app.settings import Settings
from stoobly_agent.config.constants import custom_headers, mock_policy, mode, record_policy


class TestGetProjectKey:
    def test_returns_project_key_from_header(self):
        headers = Headers(**{custom_headers.PROJECT_KEY: 'header-project-key'})
        settings = {'project_key': 'settings-project-key'}

        assert proxy_settings.get_project_key(headers, settings) == 'header-project-key'

    def test_returns_project_key_from_settings_when_header_missing(self):
        headers = Headers()
        settings = {'project_key': 'settings-project-key'}

        assert proxy_settings.get_project_key(headers, settings) == 'settings-project-key'


class TestGetReportKey:
    def test_returns_report_key_from_header(self):
        headers = Headers(**{custom_headers.REPORT_KEY: 'report-key'})

        assert proxy_settings.get_report_key(headers) == 'report-key'

    def test_returns_none_when_header_missing(self):
        headers = Headers()

        assert proxy_settings.get_report_key(headers) is None


class TestGetScenarioKey:
    def test_returns_scenario_key_from_header(self):
        headers = Headers(**{custom_headers.SCENARIO_KEY: 'header-scenario-key'})
        settings = {'scenario_key': 'settings-scenario-key'}

        assert proxy_settings.get_scenario_key(headers, settings) == 'header-scenario-key'

    def test_returns_scenario_key_from_settings_when_header_missing(self):
        headers = Headers()
        settings = {'scenario_key': 'settings-scenario-key'}

        assert proxy_settings.get_scenario_key(headers, settings) == 'settings-scenario-key'


class TestIsProxyEnabled:
    def test_returns_true_when_settings_enabled(self):
        headers = Headers()
        settings = {'enabled': True}

        assert proxy_settings.is_proxy_enabled(headers, settings) is True

    def test_returns_true_when_proxy_mode_header_present(self):
        headers = Headers(**{custom_headers.PROXY_MODE: mode.MOCK})
        settings = {'enabled': False}

        assert proxy_settings.is_proxy_enabled(headers, settings) is True

    def test_returns_false_when_disabled_and_no_header(self):
        headers = Headers()
        settings = {'enabled': False}

        assert proxy_settings.is_proxy_enabled(headers, settings) is False


class TestGetProxyMode:
    def test_returns_none_for_access_control_request_with_intercept_active(self):
        headers = Headers(**{
            'Access-Control-Request-Headers': custom_headers.INTERCEPT_ACTIVE.lower(),
        })
        settings = MagicMock(spec=Settings)
        settings.proxy.intercept.active = mode.RECORD

        assert proxy_settings.get_proxy_mode(headers, settings) == mode.NONE

    def test_returns_none_when_intercept_active_header_is_zero(self):
        headers = Headers(**{custom_headers.INTERCEPT_ACTIVE: '0'})
        settings = MagicMock(spec=Settings)
        settings.proxy.intercept.active = mode.RECORD

        assert proxy_settings.get_proxy_mode(headers, settings) == mode.NONE

    def test_returns_proxy_mode_from_header(self):
        headers = Headers(**{custom_headers.PROXY_MODE: mode.MOCK})
        settings = MagicMock(spec=Settings)
        settings.proxy.intercept.active = mode.RECORD

        assert proxy_settings.get_proxy_mode(headers, settings) == mode.MOCK

    def test_returns_settings_proxy_mode_when_no_headers(self):
        headers = Headers()
        settings = MagicMock(spec=Settings)
        settings.proxy.intercept.active = mode.TEST

        assert proxy_settings.get_proxy_mode(headers, settings) == mode.TEST


class TestGetMockPolicy:
    def test_returns_mock_policy_from_header(self):
        headers = Headers(**{custom_headers.MOCK_POLICY: mock_policy.ALL})
        settings = {'policy': mock_policy.FOUND}

        assert proxy_settings.get_mock_policy(headers, settings) == mock_policy.ALL

    def test_returns_mock_policy_from_settings_when_header_missing(self):
        headers = Headers()
        settings = {'policy': mock_policy.NONE}

        assert proxy_settings.get_mock_policy(headers, settings) == mock_policy.NONE

    def test_defaults_to_found_when_header_and_settings_missing(self):
        headers = Headers()
        settings = {}

        assert proxy_settings.get_mock_policy(headers, settings) == mock_policy.FOUND


class TestGetRecordPolicy:
    def test_returns_record_policy_from_header(self):
        headers = Headers(**{custom_headers.RECORD_POLICY: record_policy.API})
        settings = {'policy': record_policy.ALL}

        assert proxy_settings.get_record_policy(headers, settings) == record_policy.API

    def test_returns_record_policy_from_settings_when_header_missing(self):
        headers = Headers()
        settings = {'policy': record_policy.NONE}

        assert proxy_settings.get_record_policy(headers, settings) == record_policy.NONE

    def test_defaults_to_all_when_header_and_settings_missing(self):
        headers = Headers()
        settings = {}

        assert proxy_settings.get_record_policy(headers, settings) == record_policy.ALL
