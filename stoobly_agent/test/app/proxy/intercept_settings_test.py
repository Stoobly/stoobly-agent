import pytest
from unittest.mock import MagicMock, Mock

from mitmproxy.http import Headers, Request as MitmproxyRequest

from stoobly_agent.app.proxy.intercept_settings import InterceptSettings
from stoobly_agent.app.settings import Settings
from stoobly_agent.config.constants import custom_headers
from stoobly_agent.lib.api.keys.project_key import ProjectKey
from stoobly_agent.lib.cache import Cache
from stoobly_agent.test.test_helper import reset


@pytest.fixture(autouse=True)
def settings():
    return reset()


@pytest.fixture
def mock_settings():
    settings = MagicMock(spec=Settings)
    settings.proxy = MagicMock()
    settings.proxy.data = MagicMock()
    settings.proxy.intercept = MagicMock()
    # Use a properly encoded project key with id=1
    settings.proxy.intercept.project_key = ProjectKey.encode(1, 1).decode()
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

