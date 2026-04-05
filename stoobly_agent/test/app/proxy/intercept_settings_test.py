import base64
import json
import os
import re
import pytest
from unittest.mock import MagicMock, Mock

from mitmproxy.http import Headers, Request as MitmproxyRequest

from stoobly_agent.app.proxy.intercept_settings import InterceptSettings
from stoobly_agent.app.settings import Settings
from stoobly_agent.app.settings.constants import request_component
from stoobly_agent.config.constants import custom_headers, env_vars
from stoobly_agent.lib.api.keys.project_key import ProjectKey
from stoobly_agent.lib.cache import Cache
from stoobly_agent.test.test_helper import reset
from pathlib import Path


@pytest.fixture(autouse=True)
def settings():
    return reset()


@pytest.fixture
def mock_settings():
    settings = MagicMock(spec=Settings)
    settings.proxy = MagicMock()
    settings.proxy.data = MagicMock()
    settings.proxy.intercept = MagicMock()
    settings.proxy.match = MagicMock()
    settings.proxy.rewrite = MagicMock()
    settings.proxy.firewall = MagicMock()
    # Use a properly encoded project key with id=1
    settings.proxy.intercept.project_key = ProjectKey.encode(1, 1).decode()
    settings.proxy.match.match_rules.return_value = []
    settings.proxy.rewrite.rewrite_rules.return_value = []
    settings.proxy.firewall.firewall_rules.return_value = []
    return settings


@pytest.fixture
def mock_data_rules():
    data_rules = MagicMock()
    data_rules.scenario_key = 'default_scenario_key'
    return data_rules


@pytest.fixture
def mock_request():
    """Create a mock mitmproxy request with headers."""
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
def cache():
    """Create a fresh cache instance."""
    Cache._instance = None
    return Cache.instance()


@pytest.fixture
def scenario_model():
    """Create a mock scenario model."""
    return MagicMock()


class TestScenarioKey:

    def test_returns_scenario_key_from_header_when_set(self, mock_settings, mock_data_rules, mock_request):
        """Test that scenario_key returns the value from SCENARIO_KEY header when set."""
        mock_request.headers = Headers(**{custom_headers.SCENARIO_KEY: 'header_scenario_key'})
        mock_settings.proxy.data.data_rules.return_value = mock_data_rules
        
        intercept_settings = InterceptSettings(mock_settings, mock_request)
        assert intercept_settings.scenario_key == 'header_scenario_key'

    def test_returns_data_rules_scenario_key_when_no_headers(self, mock_settings, mock_data_rules):
        """Test that scenario_key returns data_rules.scenario_key when no headers are set."""
        mock_settings.proxy.data.data_rules.return_value = mock_data_rules
        
        intercept_settings = InterceptSettings(mock_settings)
        assert intercept_settings.scenario_key == 'default_scenario_key'

    def test_returns_cached_scenario_key_when_scenario_name_header_set(self, mock_settings, mock_data_rules, mock_request, cache, scenario_model):
        """Test that scenario_key returns cached value when SCENARIO_NAME header is set and cache has the key."""
        scenario_name = 'Test Scenario'
        scenario_key = 'cached_scenario_key'
        
        # Set up cache with scenario name mapping (cache key now includes project_id)
        cache.write('scenario_name_index.1', {scenario_name: scenario_key}, timeout=None)
        
        mock_request.headers = Headers(**{custom_headers.SCENARIO_NAME: scenario_name})
        mock_settings.proxy.data.data_rules.return_value = mock_data_rules
        
        intercept_settings = InterceptSettings(mock_settings, mock_request, cache=cache, scenario_model=scenario_model)
        assert intercept_settings.scenario_key == scenario_key

    def test_queries_scenario_model_when_cache_miss(self, mock_settings, mock_data_rules, mock_request, cache, scenario_model):
        """Test that scenario_key queries ScenarioModel when cache miss occurs."""
        scenario_name = 'Test Scenario'
        scenario_key = 'found_scenario_key'
        
        # Mock scenario model response
        scenario_model.index.return_value = ({
            'list': [{'key': scenario_key, 'name': scenario_name}],
            'total': 1
        }, 200)
        
        mock_request.headers = Headers(**{custom_headers.SCENARIO_NAME: scenario_name})
        mock_settings.proxy.data.data_rules.return_value = mock_data_rules
        
        intercept_settings = InterceptSettings(mock_settings, mock_request, cache=cache, scenario_model=scenario_model)
        result = intercept_settings.scenario_key
        
        assert result == scenario_key
        scenario_model.index.assert_called_once_with(project_id='1', q=scenario_name, sort_by='requests_count')
        
        # Verify cache was updated (cache key now includes project_id)
        cache_data = cache.read('scenario_name_index.1')
        assert cache_data is not None
        assert cache_data['value'][scenario_name] == scenario_key

    def test_returns_none_when_scenario_not_found(self, mock_settings, mock_data_rules, mock_request, cache, scenario_model):
        """Test that scenario_key returns None when scenario is not found."""
        scenario_name = 'Non-existent Scenario'
        
        # Mock scenario model response with empty list
        scenario_model.index.return_value = ({
            'list': [],
            'total': 0
        }, 200)
        
        mock_request.headers = Headers(**{custom_headers.SCENARIO_NAME: scenario_name})
        mock_settings.proxy.data.data_rules.return_value = mock_data_rules
        
        intercept_settings = InterceptSettings(mock_settings, mock_request, cache=cache, scenario_model=scenario_model)
        result = intercept_settings.scenario_key
        
        assert result is None
        scenario_model.index.assert_called_once_with(project_id='1', q=scenario_name, sort_by='requests_count')
        
        # Verify cache was NOT updated when scenario not found (code only caches found scenarios)
        cache_data = cache.read('scenario_name_index.1')
        assert cache_data is None

    def test_does_not_cache_on_error(self, mock_settings, mock_data_rules, mock_request, cache, scenario_model):
        """Test that scenario_key does not cache when an error occurs during query."""
        scenario_name = 'Error Scenario'
        
        # Mock scenario model to raise an exception
        scenario_model.index.side_effect = Exception('Database error')
        
        mock_request.headers = Headers(**{custom_headers.SCENARIO_NAME: scenario_name})
        mock_settings.proxy.data.data_rules.return_value = mock_data_rules
        
        intercept_settings = InterceptSettings(mock_settings, mock_request, cache=cache, scenario_model=scenario_model)
        result = intercept_settings.scenario_key
        
        assert result is None
        
        # Verify cache was NOT updated on error (code only caches found scenarios)
        cache_data = cache.read('scenario_name_index.1')
        assert cache_data is None

    def test_uses_first_scenario_from_list(self, mock_settings, mock_data_rules, mock_request, cache, scenario_model):
        """Test that scenario_key uses the first scenario that exactly matches the name when multiple are found."""
        scenario_name = 'Test Scenario'
        first_scenario_key = 'first_scenario_key'
        second_scenario_key = 'second_scenario_key'
        
        # Mock scenario model response with multiple scenarios (including one that doesn't match exactly)
        scenario_model.index.return_value = ({
            'list': [
                {'key': first_scenario_key, 'name': scenario_name},
                {'key': 'other_key', 'name': 'Test Scenario Different'},
                {'key': second_scenario_key, 'name': scenario_name}
            ],
            'total': 3
        }, 200)
        
        mock_request.headers = Headers(**{custom_headers.SCENARIO_NAME: scenario_name})
        mock_settings.proxy.data.data_rules.return_value = mock_data_rules
        
        intercept_settings = InterceptSettings(mock_settings, mock_request, cache=cache, scenario_model=scenario_model)
        result = intercept_settings.scenario_key
        
        assert result == first_scenario_key
        scenario_model.index.assert_called_once_with(project_id='1', q=scenario_name, sort_by='requests_count')
        
        # Verify cache was updated with the first matching scenario
        cache_data = cache.read('scenario_name_index.1')
        assert cache_data is not None
        assert cache_data['value'][scenario_name] == first_scenario_key

    def test_returns_none_when_no_project_id(self, mock_settings, mock_data_rules, mock_request, cache, scenario_model):
        """Test that scenario_key returns None when project_id is not available."""
        scenario_name = 'Test Scenario'
        
        # Set project_key to None to simulate no project (project_id will default to 0)
        mock_settings.proxy.intercept.project_key = None
        
        # Mock scenario model to return empty list when queried with project_id=0
        scenario_model.index.return_value = ({
            'list': [],
            'total': 0
        }, 200)
        
        mock_request.headers = Headers(**{custom_headers.SCENARIO_NAME: scenario_name})
        mock_settings.proxy.data.data_rules.return_value = mock_data_rules
        
        intercept_settings = InterceptSettings(mock_settings, mock_request, cache=cache, scenario_model=scenario_model)
        result = intercept_settings.scenario_key
        
        assert result is None
        scenario_model.index.assert_not_called()

    def test_uses_fluent_interface_for_cache(self, mock_settings, mock_data_rules, mock_request, cache):
        """Test that with_cache method works with fluent interface."""
        scenario_name = 'Test Scenario'
        scenario_key = 'cached_scenario_key'
        
        # Cache key now includes project_id
        cache.write('scenario_name_index.1', {scenario_name: scenario_key}, timeout=None)
        
        mock_request.headers = Headers(**{custom_headers.SCENARIO_NAME: scenario_name})
        mock_settings.proxy.data.data_rules.return_value = mock_data_rules
        
        intercept_settings = InterceptSettings(mock_settings, mock_request)
        result = intercept_settings.with_cache(cache).scenario_key
        
        assert result == scenario_key

    def test_uses_fluent_interface_for_scenario_model(self, mock_settings, mock_data_rules, mock_request, cache, scenario_model):
        """Test that with_scenario_model method works with fluent interface."""
        scenario_name = 'Test Scenario'
        scenario_key = 'found_scenario_key'
        
        scenario_model.index.return_value = ({
            'list': [{'key': scenario_key, 'name': scenario_name}],
            'total': 1
        }, 200)
        
        mock_request.headers = Headers(**{custom_headers.SCENARIO_NAME: scenario_name})
        mock_settings.proxy.data.data_rules.return_value = mock_data_rules
        
        intercept_settings = InterceptSettings(mock_settings, mock_request, cache=cache)
        result = intercept_settings.with_scenario_model(scenario_model).scenario_key
        
        assert result == scenario_key
        scenario_model.index.assert_called_once_with(project_id='1', q=scenario_name, sort_by='requests_count')

    def test_prioritizes_scenario_key_header_over_scenario_name(self, mock_settings, mock_data_rules, mock_request, cache, scenario_model):
        """Test that SCENARIO_KEY header takes priority over SCENARIO_NAME header."""
        scenario_key_header = 'header_scenario_key'
        scenario_name = 'Test Scenario'
        
        mock_request.headers = Headers(**{
            custom_headers.SCENARIO_KEY: scenario_key_header,
            custom_headers.SCENARIO_NAME: scenario_name
        })
        mock_settings.proxy.data.data_rules.return_value = mock_data_rules
        
        intercept_settings = InterceptSettings(mock_settings, mock_request, cache=cache, scenario_model=scenario_model)
        result = intercept_settings.scenario_key
        
        assert result == scenario_key_header
        # ScenarioModel should not be called when SCENARIO_KEY header is present
        scenario_model.index.assert_not_called()

    def test_create_if_missing_creates_scenario_when_not_found(self, mock_settings, mock_data_rules, mock_request, cache, scenario_model):
        """Test that X-Stoobly-Scenario-Create-If-Missing creates a scenario when the name does not resolve."""
        scenario_name = 'Test Scenario'
        created_scenario_key = 'created_scenario_key'

        scenario_model.index.return_value = ({
            'list': [],
            'total': 0
        }, 200)

        scenario_model.create.return_value = ({
            'key': created_scenario_key,
            'name': scenario_name,
        }, 200)

        mock_request.headers = Headers(**{
            custom_headers.SCENARIO_NAME: scenario_name,
            custom_headers.SCENARIO_CREATE_IF_MISSING: '1',
        })
        mock_settings.proxy.data.data_rules.return_value = mock_data_rules

        intercept_settings = InterceptSettings(mock_settings, mock_request, cache=cache, scenario_model=scenario_model)
        result = intercept_settings.scenario_key

        assert result == created_scenario_key
        scenario_model.index.assert_called_once_with(project_id='1', q=scenario_name, sort_by='requests_count')
        scenario_model.create.assert_called_once_with(name=scenario_name, description='', priority=0)

        cache_data = cache.read('scenario_name_index.1')
        assert cache_data is not None
        assert cache_data['value'][scenario_name] == created_scenario_key

    def test_create_if_missing_not_called_when_scenario_found(self, mock_settings, mock_data_rules, mock_request, cache, scenario_model):
        """Test that scenario is not created when the name already resolves to an existing scenario."""
        scenario_name = 'Test Scenario'
        existing_scenario_key = 'existing_scenario_key'

        scenario_model.index.return_value = ({
            'list': [{'key': existing_scenario_key, 'name': scenario_name}],
            'total': 1
        }, 200)

        mock_request.headers = Headers(**{
            custom_headers.SCENARIO_NAME: scenario_name,
            custom_headers.SCENARIO_CREATE_IF_MISSING: '1',
        })
        mock_settings.proxy.data.data_rules.return_value = mock_data_rules

        intercept_settings = InterceptSettings(mock_settings, mock_request, cache=cache, scenario_model=scenario_model)
        result = intercept_settings.scenario_key

        assert result == existing_scenario_key
        scenario_model.create.assert_not_called()

    def test_create_if_missing_does_not_cache_on_create_failure(self, mock_settings, mock_data_rules, mock_request, cache, scenario_model):
        """Test that a failed create does not populate the scenario-name cache mapping."""
        scenario_name = 'Test Scenario'

        scenario_model.index.return_value = ({
            'list': [],
            'total': 0
        }, 200)

        scenario_model.create.return_value = ({}, 500)

        mock_request.headers = Headers(**{
            custom_headers.SCENARIO_NAME: scenario_name,
            custom_headers.SCENARIO_CREATE_IF_MISSING: '1',
        })
        mock_settings.proxy.data.data_rules.return_value = mock_data_rules

        intercept_settings = InterceptSettings(mock_settings, mock_request, cache=cache, scenario_model=scenario_model)
        result = intercept_settings.scenario_key

        assert result is None
        scenario_model.create.assert_called_once()

        cache_data = cache.read('scenario_name_index.1')
        assert cache_data is None

    def test_create_if_missing_uses_existing_scenario_when_create_conflicts(self, mock_settings, mock_data_rules, mock_request, cache, scenario_model):
        """Test that a 409 create conflict resolves and caches an existing scenario key by exact name."""
        scenario_name = 'Test Scenario'
        existing_scenario_key = 'existing_scenario_key'

        scenario_model.index.side_effect = [
            ({
                'list': [],
                'total': 0
            }, 200),
            ({
                'list': [{'key': existing_scenario_key, 'name': scenario_name}],
                'total': 1
            }, 200),
        ]
        scenario_model.create.return_value = ({'error': 'Scenario name already exists'}, 409)

        mock_request.headers = Headers(**{
            custom_headers.SCENARIO_NAME: scenario_name,
            custom_headers.SCENARIO_CREATE_IF_MISSING: '1',
        })
        mock_settings.proxy.data.data_rules.return_value = mock_data_rules

        intercept_settings = InterceptSettings(mock_settings, mock_request, cache=cache, scenario_model=scenario_model)
        result = intercept_settings.scenario_key

        assert result == existing_scenario_key
        scenario_model.create.assert_called_once_with(name=scenario_name, description='', priority=0)

        cache_data = cache.read('scenario_name_index.1')
        assert cache_data is not None
        assert cache_data['value'][scenario_name] == existing_scenario_key

    def test_create_if_missing_ignored_when_scenario_key_header_present(self, mock_settings, mock_data_rules, mock_request, cache, scenario_model):
        """Test that SCENARIO_KEY still takes priority over SCENARIO_NAME create-if-missing."""
        scenario_key_header = 'header_scenario_key'
        scenario_name = 'Test Scenario'

        mock_request.headers = Headers(**{
            custom_headers.SCENARIO_KEY: scenario_key_header,
            custom_headers.SCENARIO_NAME: scenario_name,
            custom_headers.SCENARIO_CREATE_IF_MISSING: '1',
        })
        mock_settings.proxy.data.data_rules.return_value = mock_data_rules

        intercept_settings = InterceptSettings(mock_settings, mock_request, cache=cache, scenario_model=scenario_model)
        result = intercept_settings.scenario_key

        assert result == scenario_key_header
        scenario_model.index.assert_not_called()
        scenario_model.create.assert_not_called()

    def test_create_if_missing_returns_none_when_no_project_id(self, mock_settings, mock_data_rules, mock_request, cache, scenario_model):
        """Test that create-if-missing does not attempt resolution/creation when project_id is not available."""
        scenario_name = 'Test Scenario'

        mock_settings.proxy.intercept.project_key = None
        scenario_model.index.return_value = ({
            'list': [],
            'total': 0
        }, 200)
        scenario_model.create.return_value = ({
            'key': 'created_key',
            'name': scenario_name,
        }, 200)

        mock_request.headers = Headers(**{
            custom_headers.SCENARIO_NAME: scenario_name,
            custom_headers.SCENARIO_CREATE_IF_MISSING: '1',
        })
        mock_settings.proxy.data.data_rules.return_value = mock_data_rules

        intercept_settings = InterceptSettings(mock_settings, mock_request, cache=cache, scenario_model=scenario_model)
        result = intercept_settings.scenario_key

        assert result is None
        scenario_model.index.assert_not_called()
        scenario_model.create.assert_not_called()


class TestRequestMatchRules:

    def test_appends_rule_from_header_when_valid_base64_json(self, mock_settings, mock_data_rules, mock_request):
        """Test that match_rules appends a rule from X-Stoobly-Request-Match-Rules header when valid base64 JSON."""
        match_rules = [
            {'components': request_component.BODY_PARAM, 'modes': ['mock']},
            {'components': request_component.HEADER, 'modes': ['mock']},
        ]
        header_value = base64.b64encode(json.dumps(match_rules).encode('utf-8')).decode('ascii')

        mock_request.headers = Headers(**{
            custom_headers.REQUEST_MATCH_RULES: header_value,
            custom_headers.PROXY_MODE: 'mock',
        })
        mock_settings.proxy.data.data_rules.return_value = mock_data_rules

        intercept_settings = InterceptSettings(mock_settings, mock_request)
        rules = intercept_settings.match_rules

        assert len(rules) == 2
        assert rules[0].components == [request_component.BODY_PARAM]
        assert rules[0].methods == ['GET']
        assert rules[0].modes == ['mock']
        assert rules[1].components == [request_component.HEADER]
        assert rules[1].methods == ['GET']
        assert rules[1].modes == ['mock']

    def test_uses_request_method_and_url_for_header_rule(self, mock_settings, mock_data_rules, mock_request):
        """Test that header rule uses request method and URL as pattern."""
        match_rules = [{'components': request_component.QUERY_PARAM}]
        header_value = base64.b64encode(json.dumps(match_rules).encode('utf-8')).decode('ascii')

        mock_request.headers = Headers(**{
            custom_headers.REQUEST_MATCH_RULES: header_value,
            custom_headers.PROXY_MODE: 'mock',
        })
        mock_settings.proxy.data.data_rules.return_value = mock_data_rules

        intercept_settings = InterceptSettings(mock_settings, mock_request)
        rules = intercept_settings.match_rules

        assert len(rules) == 1
        assert rules[0].methods == ['GET']
        assert rules[0].pattern == re.escape(mock_request.url)

    def test_ignores_invalid_header(self, mock_settings, mock_data_rules, mock_request):
        """Test that match_rules ignores invalid base64 or JSON in header."""
        mock_request.headers = Headers(**{
            custom_headers.REQUEST_MATCH_RULES: 'not-valid-base64!!!',
            custom_headers.PROXY_MODE: 'mock',
        })
        mock_settings.proxy.data.data_rules.return_value = mock_data_rules

        intercept_settings = InterceptSettings(mock_settings, mock_request)
        rules = intercept_settings.match_rules

        assert len(rules) == 0

    def test_returns_settings_rules_when_header_not_set(self, mock_settings, mock_data_rules, mock_request):
        """Test that match_rules returns only settings rules when header is not set."""
        from stoobly_agent.app.settings.match_rule import MatchRule

        settings_rule = MatchRule({
            'components': [request_component.BODY_PARAM],
            'methods': ['GET'],
            'modes': ['mock'],
            'pattern': r'.*',
        })
        mock_settings.proxy.match.match_rules.return_value = [settings_rule]

        mock_request.headers = Headers(**{custom_headers.PROXY_MODE: 'mock'})
        mock_settings.proxy.data.data_rules.return_value = mock_data_rules

        intercept_settings = InterceptSettings(mock_settings, mock_request)
        rules = intercept_settings.match_rules

        assert len(rules) == 1
        assert rules[0].components == [request_component.BODY_PARAM]

    def test_returns_empty_when_request_is_none(self, mock_settings, mock_data_rules):
        """Test that match_rules does not append header rule when request is None."""
        components = [request_component.BODY_PARAM]
        header_value = base64.b64encode(json.dumps(components).encode('utf-8')).decode('ascii')

        intercept_settings = InterceptSettings(mock_settings)
        intercept_settings._InterceptSettings__headers = Headers(**{custom_headers.REQUEST_MATCH_RULES: header_value})
        intercept_settings._InterceptSettings__request = None

        rules = intercept_settings.match_rules

        assert len(rules) == 0


class TestRequestRewriteRules:

    def test_appends_rule_from_header_when_valid_base64_json(self, mock_settings, mock_data_rules, mock_request):
        """Test that rewrite_rules appends a rule from X-Stoobly-Request-Rewrite-Rules header when valid base64 JSON."""
        rewrite_rules = [
            {
                'parameter_rules': [
                    {'type': 'Header', 'name': 'Authorization', 'value': 'Bearer xyz'},
                    {'type': 'Query Param', 'name': 'api_key', 'value': 'secret'},
                ]
            }
        ]
        header_value = base64.b64encode(json.dumps(rewrite_rules).encode('utf-8')).decode('ascii')

        mock_request.headers = Headers(**{
            custom_headers.REQUEST_REWRITE_RULES: header_value,
            custom_headers.PROXY_MODE: 'mock',
        })
        mock_settings.proxy.data.data_rules.return_value = mock_data_rules

        intercept_settings = InterceptSettings(mock_settings, mock_request)
        rules = intercept_settings.rewrite_rules

        assert len(rules) == 1
        assert len(rules[0].parameter_rules) == 2
        assert rules[0].parameter_rules[0].name == 'Authorization'
        assert rules[0].parameter_rules[0].type == 'Header'
        assert rules[0].parameter_rules[0].value == 'Bearer xyz'
        assert rules[0].parameter_rules[1].name == 'api_key'
        assert rules[0].parameter_rules[1].type == 'Query Param'
        assert rules[0].parameter_rules[1].value == 'secret'

    def test_uses_request_method_and_url_for_header_rule(self, mock_settings, mock_data_rules, mock_request):
        """Test that header rewrite rule uses request method and URL as pattern."""
        rewrite_rules = [
            {
                'parameter_rules': [
                    {'type': 'Header', 'name': 'X-Custom', 'value': 'value'}
                ]
            }
        ]
        header_value = base64.b64encode(json.dumps(rewrite_rules).encode('utf-8')).decode('ascii')

        mock_request.headers = Headers(**{
            custom_headers.REQUEST_REWRITE_RULES: header_value,
            custom_headers.PROXY_MODE: 'mock',
        })
        mock_settings.proxy.data.data_rules.return_value = mock_data_rules

        intercept_settings = InterceptSettings(mock_settings, mock_request)
        rules = intercept_settings.rewrite_rules

        assert len(rules) == 1
        assert rules[0].methods == ['GET']
        assert rules[0].pattern == re.escape(mock_request.url)

    def test_ignores_invalid_header(self, mock_settings, mock_data_rules, mock_request):
        """Test that rewrite_rules ignores invalid base64 or JSON in header."""
        mock_request.headers = Headers(**{
            custom_headers.REQUEST_REWRITE_RULES: 'not-valid-base64!!!',
            custom_headers.PROXY_MODE: 'mock',
        })
        mock_settings.proxy.data.data_rules.return_value = mock_data_rules

        intercept_settings = InterceptSettings(mock_settings, mock_request)
        rules = intercept_settings.rewrite_rules

        assert len(rules) == 0

    def test_ignores_malformed_parameter_rules(self, mock_settings, mock_data_rules, mock_request):
        """Test that rewrite_rules ignores parameter rules missing type, name, or value."""
        rewrite_rules = [
            {
                'parameter_rules': [
                    {'type': 'Header', 'name': 'Valid', 'value': 'ok'},
                    {'name': 'MissingType', 'value': 'x'},
                    {'type': 'Header', 'value': 'MissingName'},
                    {'type': 'Header', 'name': 'MissingValue'},
                ]
            }
        ]
        header_value = base64.b64encode(json.dumps(rewrite_rules).encode('utf-8')).decode('ascii')

        mock_request.headers = Headers(**{
            custom_headers.REQUEST_REWRITE_RULES: header_value,
            custom_headers.PROXY_MODE: 'mock',
        })
        mock_settings.proxy.data.data_rules.return_value = mock_data_rules

        intercept_settings = InterceptSettings(mock_settings, mock_request)
        rules = intercept_settings.rewrite_rules

        assert len(rules) == 1
        assert len(rules[0].parameter_rules) == 1
        assert rules[0].parameter_rules[0].name == 'Valid'

    def test_returns_empty_when_request_is_none(self, mock_settings, mock_data_rules):
        """Test that rewrite_rules does not append header rule when request is None."""
        rewrite_rules = [
            {
                'parameter_rules': [
                    {'type': 'Header', 'name': 'X-Custom', 'value': 'value'}
                ]
            }
        ]
        header_value = base64.b64encode(json.dumps(rewrite_rules).encode('utf-8')).decode('ascii')

        intercept_settings = InterceptSettings(mock_settings)
        intercept_settings._InterceptSettings__headers = Headers(**{custom_headers.REQUEST_REWRITE_RULES: header_value})
        intercept_settings._InterceptSettings__request = None

        rules = intercept_settings.rewrite_rules

        assert len(rules) == 0


class TestPublicDirectoryPath:

    def test_returns_path_from_header_when_set(self, mock_settings, mock_data_rules, mock_request):
        """Test that public_directory_path returns the value from X-Stoobly-Public-Directory-Path header when set."""
        public_dir = '/path/to/public'
        mock_request.headers = Headers(**{custom_headers.PUBLIC_DIRECTORY_PATH: public_dir})
        mock_settings.proxy.data.data_rules.return_value = mock_data_rules
        
        intercept_settings = InterceptSettings(mock_settings, mock_request)
        assert intercept_settings.public_directory_path == public_dir

    def test_returns_path_from_env_when_header_not_set(self, mock_settings, mock_data_rules, mock_request, monkeypatch):
        """Test that public_directory_path returns environment variable when header is not set."""
        public_dir = '/env/public'
        monkeypatch.setenv(env_vars.AGENT_PUBLIC_DIRECTORY_PATH, public_dir)
        
        mock_settings.proxy.data.data_rules.return_value = mock_data_rules
        
        intercept_settings = InterceptSettings(mock_settings, mock_request)
        assert intercept_settings.public_directory_path == public_dir

    def test_returns_none_when_neither_header_nor_env_set(self, mock_settings, mock_data_rules, mock_request, monkeypatch):
        """Test that public_directory_path returns None when neither header nor environment variable is set."""
        # Ensure env var is not set
        monkeypatch.delenv(env_vars.AGENT_PUBLIC_DIRECTORY_PATH, raising=False)
        
        mock_settings.proxy.data.data_rules.return_value = mock_data_rules
        
        intercept_settings = InterceptSettings(mock_settings, mock_request)
        assert intercept_settings.public_directory_path is None

    def test_prioritizes_header_over_env(self, mock_settings, mock_data_rules, mock_request, monkeypatch):
        """Test that header value takes priority over environment variable."""
        header_dir = '/header/public'
        env_dir = '/env/public'
        
        monkeypatch.setenv(env_vars.AGENT_PUBLIC_DIRECTORY_PATH, env_dir)
        mock_request.headers = Headers(**{custom_headers.PUBLIC_DIRECTORY_PATH: header_dir})
        mock_settings.proxy.data.data_rules.return_value = mock_data_rules
        
        intercept_settings = InterceptSettings(mock_settings, mock_request)
        assert intercept_settings.public_directory_path == header_dir

class TestResponseFixturesPath:

    def test_returns_path_from_header_when_set(self, mock_settings, mock_data_rules, mock_request):
        """Test that response_fixtures_path returns the value from X-Stoobly-Response-Fixtures-Path header when set."""
        fixtures_path = '/path/to/fixtures.json'
        mock_request.headers = Headers(**{custom_headers.RESPONSE_FIXTURES_PATH: fixtures_path})
        mock_settings.proxy.data.data_rules.return_value = mock_data_rules
        
        intercept_settings = InterceptSettings(mock_settings, mock_request)
        assert intercept_settings.response_fixtures_path == fixtures_path

    def test_returns_path_from_env_when_header_not_set(self, mock_settings, mock_data_rules, mock_request, monkeypatch):
        """Test that response_fixtures_path returns environment variable when header is not set."""
        fixtures_path = '/env/fixtures.json'
        monkeypatch.setenv(env_vars.AGENT_RESPONSE_FIXTURES_PATH, fixtures_path)
        
        mock_settings.proxy.data.data_rules.return_value = mock_data_rules
        
        intercept_settings = InterceptSettings(mock_settings, mock_request)
        assert intercept_settings.response_fixtures_path == fixtures_path

    def test_returns_none_when_neither_header_nor_env_set(self, mock_settings, mock_data_rules, mock_request, monkeypatch):
        """Test that response_fixtures_path returns None when neither header nor environment variable is set."""
        # Ensure env var is not set
        monkeypatch.delenv(env_vars.AGENT_RESPONSE_FIXTURES_PATH, raising=False)
        
        mock_settings.proxy.data.data_rules.return_value = mock_data_rules
        
        intercept_settings = InterceptSettings(mock_settings, mock_request)
        assert intercept_settings.response_fixtures_path is None

    def test_prioritizes_header_over_env(self, mock_settings, mock_data_rules, mock_request, monkeypatch):
        """Test that header value takes priority over environment variable."""
        header_path = '/header/fixtures.json'
        env_path = '/env/fixtures.json'
        
        monkeypatch.setenv(env_vars.AGENT_RESPONSE_FIXTURES_PATH, env_path)
        mock_request.headers = Headers(**{custom_headers.RESPONSE_FIXTURES_PATH: header_path})
        mock_settings.proxy.data.data_rules.return_value = mock_data_rules
        
        intercept_settings = InterceptSettings(mock_settings, mock_request)
        assert intercept_settings.response_fixtures_path == header_path


class TestLifecycleHooksPath:
    def _base_settings(self, mock_settings, mock_data_rules):
        mock_settings.proxy.data.data_rules.return_value = mock_data_rules
        return mock_settings

    def test_header_takes_precedence_over_env_single_value(self, mock_settings, mock_data_rules, mock_request, monkeypatch):
        """Header value should override env var for single simple path."""
        header_path = '/header/lifecycle_hooks.py'
        env_path = '/env/lifecycle_hooks.py'
        monkeypatch.setenv(env_vars.AGENT_LIFECYCLE_HOOKS_PATH, env_path)

        mock_request.headers = Headers(**{custom_headers.LIFECYCLE_HOOKS_PATH: header_path})
        self._base_settings(mock_settings, mock_data_rules)

        intercept_settings = InterceptSettings(mock_settings, mock_request)
        assert intercept_settings.lifecycle_hooks_path == header_path

    def test_env_used_when_header_not_set_single_value(self, mock_settings, mock_data_rules, mock_request, monkeypatch):
        """Env var used when header not present for single simple path."""
        env_path = '/env/lifecycle_hooks.py'
        monkeypatch.setenv(env_vars.AGENT_LIFECYCLE_HOOKS_PATH, env_path)
        self._base_settings(mock_settings, mock_data_rules)

        intercept_settings = InterceptSettings(mock_settings, mock_request)
        assert intercept_settings.lifecycle_hooks_path == env_path

    def test_returns_none_when_neither_header_nor_env(self, mock_settings, mock_data_rules, mock_request, monkeypatch):
        """Returns None when no header or env provided."""
        monkeypatch.delenv(env_vars.AGENT_LIFECYCLE_HOOKS_PATH, raising=False)
        self._base_settings(mock_settings, mock_data_rules)

        intercept_settings = InterceptSettings(mock_settings, mock_request)
        assert intercept_settings.lifecycle_hooks_path is None

    def test_multi_without_request_prefers_first_without_origin(self, mock_settings, mock_data_rules, monkeypatch):
        """When no request provided, prefer first item without origin; else first item."""
        raw = '/path/with-origin.py:https://a.example.com,/preferred/no-origin.py,/other.py:https://b.example.com'
        monkeypatch.setenv(env_vars.AGENT_LIFECYCLE_HOOKS_PATH, raw)
        self._base_settings(mock_settings, mock_data_rules)

        intercept_settings = InterceptSettings(mock_settings)
        assert intercept_settings.lifecycle_hooks_path == '/preferred/no-origin.py'

    def test_multi_without_request_fallback_first_item_when_all_have_origin(self, mock_settings, mock_data_rules, monkeypatch):
        raw = '/first.py:https://a.example.com,/second.py:https://b.example.com'
        monkeypatch.setenv(env_vars.AGENT_LIFECYCLE_HOOKS_PATH, raw)
        self._base_settings(mock_settings, mock_data_rules)

        intercept_settings = InterceptSettings(mock_settings)
        assert intercept_settings.lifecycle_hooks_path == '/first.py'

    def test_multi_with_request_matches_regex_origin_first(self, mock_settings, mock_data_rules, mock_request, monkeypatch):
        """With request, select item whose origin regex matches request origin."""
        # mock_request fixture yields https://example.com:443/test => origin 'https://example.com:443'
        raw = '/match.py:https://example\\.com(:443)?,/fallback.py'
        monkeypatch.setenv(env_vars.AGENT_LIFECYCLE_HOOKS_PATH, raw)
        self._base_settings(mock_settings, mock_data_rules)

        # Ensure PROXY_MODE is set so InterceptSettings doesn't default to NONE path influences
        mock_request.headers = Headers(**{custom_headers.PROXY_MODE: 'mock'})
        intercept_settings = InterceptSettings(mock_settings, mock_request)
        assert intercept_settings.lifecycle_hooks_path == '/match.py'

    def test_multi_with_request_fallback_to_first_without_origin_when_no_match(self, mock_settings, mock_data_rules, mock_request, monkeypatch):
        raw = '/unmatched1.py:https://a.example.com,/no-origin.py,/unmatched2.py:https://b.example.com'
        monkeypatch.setenv(env_vars.AGENT_LIFECYCLE_HOOKS_PATH, raw)
        self._base_settings(mock_settings, mock_data_rules)

        mock_request.headers = Headers(**{custom_headers.PROXY_MODE: 'mock'})
        intercept_settings = InterceptSettings(mock_settings, mock_request)
        assert intercept_settings.lifecycle_hooks_path == '/no-origin.py'

    def test_multi_with_request_final_fallback_first_item_when_all_have_origin_and_no_match(self, mock_settings, mock_data_rules, mock_request, monkeypatch):
        raw = '/first.py:https://a.example.com,/second.py:https://b.example.com'
        monkeypatch.setenv(env_vars.AGENT_LIFECYCLE_HOOKS_PATH, raw)
        self._base_settings(mock_settings, mock_data_rules)

        mock_request.headers = Headers(**{custom_headers.PROXY_MODE: 'mock'})
        intercept_settings = InterceptSettings(mock_settings, mock_request)
        assert intercept_settings.lifecycle_hooks_path == '/first.py'

    def test_initialize_lifecycle_hooks_loads_when_file_exists(self, mock_settings, mock_data_rules, mock_request, tmp_path):
        """Verify __initialize_lifecycle_hooks loads module dict from script path."""
        # Create a temporary hooks script
        script_path = tmp_path / 'lifecycle_hooks.py'
        script_path.write_text('VALUE = 42\n')

        mock_request.headers = Headers(**{custom_headers.LIFECYCLE_HOOKS_PATH: str(script_path)})
        self._base_settings(mock_settings, mock_data_rules)

        intercept_settings = InterceptSettings(mock_settings, mock_request)
        # Access lifecycle_hooks to ensure it loaded
        hooks = intercept_settings.lifecycle_hooks
        assert isinstance(hooks, dict)
        assert hooks.get('VALUE') == 42

    def test_initialize_lifecycle_hooks_silent_when_file_missing(self, mock_settings, mock_data_rules, mock_request, tmp_path):
        """Missing file should not raise and lifecycle_hooks should be empty dict."""
        missing_path = tmp_path / 'does_not_exist.py'
        mock_request.headers = Headers(**{custom_headers.LIFECYCLE_HOOKS_PATH: str(missing_path)})
        self._base_settings(mock_settings, mock_data_rules)

        intercept_settings = InterceptSettings(mock_settings, mock_request)
        assert intercept_settings.lifecycle_hooks == {}
