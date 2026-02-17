import json
import os
import shutil
import tempfile
from datetime import datetime
from unittest.mock import MagicMock, PropertyMock, patch

import pytest

from stoobly_agent.config.constants import custom_headers
from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.lib.intercepted_requests.logger import InterceptedRequestsLogger
from stoobly_agent.lib.intercepted_requests.scaffold_logger import ScaffoldInterceptedRequestsLogger
from stoobly_agent.lib.intercepted_requests.simple_logger import SimpleInterceptedRequestsLogger
from stoobly_agent.lib.logger import DEBUG, ERROR, INFO
from stoobly_agent.test.test_helper import reset


@pytest.fixture(autouse=True, scope='module')
def settings():
    return reset()


@pytest.fixture(autouse=True)
def reset_logger_state():
    """Reset class-level state before each test."""
    InterceptedRequestsLogger._file_path = None
    InterceptedRequestsLogger._previous_scenario_key = None
    InterceptedRequestsLogger._queue_listener = None
    InterceptedRequestsLogger._log_queue = None
    InterceptedRequestsLogger._file_handler = None
    InterceptedRequestsLogger._logger.handlers.clear()
    InterceptedRequestsLogger._logger.disabled = True
    yield
    InterceptedRequestsLogger.shutdown()


@pytest.fixture
def temp_log_dir():
    """Create a temporary directory for log files."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def mock_mitmproxy_request():
    """Create a mock mitmproxy request."""
    request = MagicMock()
    request.method = 'GET'
    request.pretty_url = 'https://example.com/api/test'
    request.headers = MagicMock()
    request.headers.get = MagicMock(return_value=None)
    request.timestamp_start = datetime.now().timestamp()
    return request


@pytest.fixture
def mock_mitmproxy_response():
    """Create a mock mitmproxy response."""
    response = MagicMock()
    response.status_code = 200
    response.headers = MagicMock()
    response.headers.get = MagicMock(return_value=None)
    return response


class TestLoggerSetup:
    """Tests for logger setup methods."""

    def test_set_file_path(self, temp_log_dir):
        """Verify custom file path is set."""
        custom_path = os.path.join(temp_log_dir, 'custom.log')
        InterceptedRequestsLogger.set_file_path(custom_path)

        assert InterceptedRequestsLogger._file_path == custom_path

    def test_enable_logger_file_creates_file(self, temp_log_dir):
        """Verify log file is created."""
        log_path = os.path.join(temp_log_dir, 'test.log')
        InterceptedRequestsLogger.set_file_path(log_path)
        ScaffoldInterceptedRequestsLogger.enable_logger_file()

        with patch('stoobly_agent.lib.intercepted_requests.logger.InterceptSettings') as mock_intercept:
            mock_intercept.return_value.scenario_key = None
            InterceptedRequestsLogger.info("Test message")

        assert os.path.exists(log_path)

    def test_set_log_level(self):
        """Verify log level can be set and retrieved."""
        InterceptedRequestsLogger.set_log_level(DEBUG)
        assert InterceptedRequestsLogger.get_log_level() == DEBUG

        InterceptedRequestsLogger.set_log_level(INFO)
        assert InterceptedRequestsLogger.get_log_level() == INFO

        InterceptedRequestsLogger.set_log_level(ERROR)
        assert InterceptedRequestsLogger.get_log_level() == ERROR


class TestLogMethods:
    """Tests for logging methods."""

    @pytest.fixture(autouse=True)
    def setup_logger(self, temp_log_dir):
        """Setup logger before each test."""
        log_path = os.path.join(temp_log_dir, 'test.log')
        InterceptedRequestsLogger.set_file_path(log_path)
        ScaffoldInterceptedRequestsLogger.enable_logger_file()
        InterceptedRequestsLogger.set_log_level(DEBUG)
        self.log_path = log_path
        yield
        InterceptedRequestsLogger.shutdown()

    def test_info_logs_message(self):
        """Basic info logging works."""
        with patch('stoobly_agent.lib.intercepted_requests.logger.InterceptSettings') as mock_intercept:
            mock_intercept.return_value.scenario_key = None
            InterceptedRequestsLogger.info("Test info message")

        InterceptedRequestsLogger.flush()

        with open(self.log_path, 'r') as f:
            content = f.read()
            assert "Test info message" in content

    def test_logs_with_request(self, mock_mitmproxy_request):
        """Request data extracted (method, URL)."""
        with patch('stoobly_agent.lib.intercepted_requests.logger.InterceptSettings') as mock_intercept:
            mock_intercept.return_value.scenario_key = None
            InterceptedRequestsLogger.info("Request log", request=mock_mitmproxy_request)

        InterceptedRequestsLogger.flush()

        with open(self.log_path, 'r') as f:
            lines = f.readlines()
            # Find the line with the actual request log (not delimiter)
            for line in lines:
                entry = json.loads(line.strip())
                if entry.get('message') == 'Request log':
                    assert entry['method'] == 'GET'
                    assert 'example.com' in entry['url']
                    return
            pytest.fail("Request log entry not found")

    def test_logs_with_response(self, mock_mitmproxy_request, mock_mitmproxy_response):
        """Response data extracted (status_code)."""
        with patch('stoobly_agent.lib.intercepted_requests.logger.InterceptSettings') as mock_intercept:
            mock_intercept.return_value.scenario_key = None
            InterceptedRequestsLogger.info(
                "Response log",
                request=mock_mitmproxy_request,
                response=mock_mitmproxy_response
            )

        InterceptedRequestsLogger.flush()

        with open(self.log_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                entry = json.loads(line.strip())
                if entry.get('message') == 'Response log':
                    assert entry['status_code'] == 200
                    return
            pytest.fail("Response log entry not found")

    def test_respects_log_level(self):
        """Log level filtering works."""
        InterceptedRequestsLogger.set_log_level(ERROR)

        with patch('stoobly_agent.lib.intercepted_requests.logger.InterceptSettings') as mock_intercept:
            mock_intercept.return_value.scenario_key = None
            InterceptedRequestsLogger.debug("Should not appear")
            InterceptedRequestsLogger.info("Should not appear")
            InterceptedRequestsLogger.error("Should appear")

        InterceptedRequestsLogger.flush()

        with open(self.log_path, 'r') as f:
            content = f.read()
            assert "Should not appear" not in content
            assert "Should appear" in content


class TestJSONFormatter:
    """Tests for JSON formatting."""

    @pytest.fixture(autouse=True)
    def setup_logger(self, temp_log_dir):
        """Setup logger before each test."""
        log_path = os.path.join(temp_log_dir, 'json_test.log')
        InterceptedRequestsLogger.set_file_path(log_path)
        ScaffoldInterceptedRequestsLogger.enable_logger_file()
        InterceptedRequestsLogger.set_log_level(DEBUG)
        self.log_path = log_path
        yield
        InterceptedRequestsLogger.shutdown()

    def test_formats_as_valid_json(self):
        """Output is valid JSON with required fields."""
        with patch('stoobly_agent.lib.intercepted_requests.logger.InterceptSettings') as mock_intercept:
            mock_intercept.return_value.scenario_key = None
            InterceptedRequestsLogger.info("JSON test message")

        InterceptedRequestsLogger.flush()

        with open(self.log_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                entry = json.loads(line.strip())
                if entry.get('message') == 'JSON test message':
                    assert 'timestamp' in entry
                    assert entry['level'] == 'INFO'
                    assert entry['message'] == 'JSON test message'
                    return
            pytest.fail("JSON test message entry not found")

    def test_truncates_long_urls(self, mock_mitmproxy_request):
        """URLs >100 chars are truncated."""
        mock_mitmproxy_request.pretty_url = 'https://example.com/' + 'a' * 200

        with patch('stoobly_agent.lib.intercepted_requests.logger.InterceptSettings') as mock_intercept:
            mock_intercept.return_value.scenario_key = None
            InterceptedRequestsLogger.info("Long URL test", request=mock_mitmproxy_request)

        InterceptedRequestsLogger.flush()

        with open(self.log_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                entry = json.loads(line.strip())
                if entry.get('message') == 'Long URL test':
                    assert len(entry['url']) == 103  # 100 + '...'
                    assert entry['url'].endswith('...')
                    return
            pytest.fail("Long URL test entry not found")

    def test_extracts_scenario_key_from_request_headers(self, mock_mitmproxy_request):
        """scenario_key is extracted from request headers."""
        expected_scenario_key = 'test-scenario-key-123'

        def mock_header_get(header_name, default=None):
            if header_name == custom_headers.SCENARIO_KEY:
                return expected_scenario_key
            return default

        mock_mitmproxy_request.headers.get = mock_header_get
        mock_mitmproxy_request.headers.__contains__ = lambda self, key: key == custom_headers.SCENARIO_KEY
        mock_mitmproxy_request.headers.__getitem__ = lambda self, key: expected_scenario_key if key == custom_headers.SCENARIO_KEY else None

        InterceptedRequestsLogger.info("Scenario key test", request=mock_mitmproxy_request)

        InterceptedRequestsLogger.flush()

        with open(self.log_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                entry = json.loads(line.strip())
                if entry.get('message') == 'Scenario key test':
                    assert entry['scenario_key'] == expected_scenario_key
                    return
            pytest.fail("Scenario key test entry not found")


class TestFileOperations:
    """Tests for file operations."""

    def test_dump_logs_prints_contents(self, temp_log_dir, capsys):
        """dump_logs() outputs file content."""
        log_path = os.path.join(temp_log_dir, 'dump_test.log')
        InterceptedRequestsLogger.set_file_path(log_path)
        ScaffoldInterceptedRequestsLogger.enable_logger_file()

        with patch('stoobly_agent.lib.intercepted_requests.logger.InterceptSettings') as mock_intercept:
            mock_intercept.return_value.scenario_key = None
            InterceptedRequestsLogger.info("Dump test message")

        InterceptedRequestsLogger.flush()
        InterceptedRequestsLogger.shutdown()
        ScaffoldInterceptedRequestsLogger.dump_logs()

        captured = capsys.readouterr()
        assert "Dump test message" in captured.out

    def test_truncate_clears_file(self, temp_log_dir):
        """truncate() clears log file."""
        log_path = os.path.join(temp_log_dir, 'truncate_test.log')
        InterceptedRequestsLogger.set_file_path(log_path)
        ScaffoldInterceptedRequestsLogger.enable_logger_file()

        with patch('stoobly_agent.lib.intercepted_requests.logger.InterceptSettings') as mock_intercept:
            mock_intercept.return_value.scenario_key = None
            InterceptedRequestsLogger.info("Before truncate")

        InterceptedRequestsLogger.flush()
        ScaffoldInterceptedRequestsLogger.truncate()

        with open(log_path, 'r') as f:
            content = f.read()
            assert "Before truncate" not in content

    def test_shutdown_clears_handlers(self, temp_log_dir):
        """shutdown() cleans up handlers."""
        log_path = os.path.join(temp_log_dir, 'shutdown_test.log')
        InterceptedRequestsLogger.set_file_path(log_path)
        ScaffoldInterceptedRequestsLogger.enable_logger_file()

        InterceptedRequestsLogger.shutdown()

        assert len(InterceptedRequestsLogger._logger.handlers) == 0
        assert InterceptedRequestsLogger._file_handler is None


class TestWorkflowNamespaceParameters:
    """Tests for workflow and namespace parameter handling."""

    @pytest.fixture(autouse=True)
    def setup_logger(self, temp_log_dir):
        """Setup logger before each test."""
        self.temp_dir = temp_log_dir
        yield
        InterceptedRequestsLogger.shutdown()

    def test_get_workflow_returns_env_var_when_set(self):
        """_get_workflow() returns WORKFLOW_NAME_ENV when set."""
        with patch.dict(os.environ, {'WORKFLOW_NAME': 'test-workflow'}):
            result = InterceptedRequestsLogger._get_workflow()
            assert result == 'test-workflow'

    def test_get_workflow_returns_default_when_env_not_set(self):
        """_get_workflow() falls back to intercept mode when env not set."""
        # Clear the env var if set, but don't clear all env vars
        env_copy = os.environ.copy()
        env_copy.pop('WORKFLOW_NAME', None)
        with patch.dict(os.environ, env_copy, clear=True):
            result = InterceptedRequestsLogger._get_workflow()
            # Assert it returns a value (the default intercept mode)
            assert result is not None

    def test_dump_logs_with_workflow_and_namespace(self, capsys):
        """dump_logs() reads from correct path when workflow/namespace specified."""
        # Create a log file at the expected path
        workflow = 'mock'
        namespace = 'test-ns'
        log_dir = os.path.join(self.temp_dir, namespace, 'logs')
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, f'{workflow}.requests.json')

        with open(log_file, 'w') as f:
            f.write('{"message": "test log entry"}\n')

        with patch.object(DataDir, 'instance') as mock_data_dir:
            mock_data_dir.return_value.tmp_dir_path = self.temp_dir
            ScaffoldInterceptedRequestsLogger.dump_logs(workflow=workflow, namespace=namespace)

        captured = capsys.readouterr()
        assert 'test log entry' in captured.out

    def test_truncate_with_workflow_and_namespace(self):
        """truncate() operates on correct file when workflow/namespace specified."""
        workflow = 'record'
        namespace = 'prod-ns'
        log_dir = os.path.join(self.temp_dir, namespace, 'logs')
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, f'{workflow}.requests.json')

        # Create file with content
        with open(log_file, 'w') as f:
            f.write('{"message": "should be cleared"}\n')

        with patch.object(DataDir, 'instance') as mock_data_dir:
            mock_data_dir.return_value.tmp_dir_path = self.temp_dir
            ScaffoldInterceptedRequestsLogger.truncate(workflow=workflow, namespace=namespace)

        # File should be empty or cleared
        with open(log_file, 'r') as f:
            content = f.read()
            assert 'should be cleared' not in content


class TestPathSanitization:
    """Tests for path traversal prevention."""

    def test_sanitize_removes_forward_slashes(self):
        """Path components with forward slashes are sanitized."""
        result = InterceptedRequestsLogger._sanitize_path_component('foo/bar')
        assert result == 'foobar'

    def test_sanitize_removes_backslashes(self):
        """Path components with backslashes are sanitized."""
        result = InterceptedRequestsLogger._sanitize_path_component('foo\\bar')
        assert result == 'foobar'

    def test_sanitize_removes_dot_dot_sequences(self):
        """Path components with .. sequences are sanitized."""
        result = InterceptedRequestsLogger._sanitize_path_component('../etc')
        assert result == 'etc'

    def test_sanitize_removes_complex_traversal(self):
        """Complex path traversal attempts are sanitized."""
        result = InterceptedRequestsLogger._sanitize_path_component('../../etc/passwd')
        assert result == 'etcpasswd'

    def test_sanitize_returns_none_for_none(self):
        """None input returns None."""
        result = InterceptedRequestsLogger._sanitize_path_component(None)
        assert result is None

    def test_sanitize_returns_none_for_only_traversal(self):
        """Input containing only traversal characters returns None."""
        result = InterceptedRequestsLogger._sanitize_path_component('../..')
        assert result is None

    def test_sanitize_preserves_valid_names(self):
        """Valid workflow/namespace names are preserved."""
        result = InterceptedRequestsLogger._sanitize_path_component('my-workflow_123')
        assert result == 'my-workflow_123'


class TestDumpLogsFiltering:
    """Tests for dump_logs filtering."""

    @pytest.fixture(autouse=True)
    def setup_log_file(self, temp_log_dir):
        """Create a log file with multiple entries for filtering tests."""
        log_path = os.path.join(temp_log_dir, 'filter_test.log')
        InterceptedRequestsLogger.set_file_path(log_path)

        entries = [
            {"timestamp": "2024-01-01T00:00:00", "level": "INFO", "message": "Mock success", "method": "GET", "url": "https://example.com/api/users", "status_code": 200, "scenario_key": "sk-1", "scenario_name": "User Scenario", "service_name": "user-api", "user_agent": "Mozilla/5.0 (X11; Linux x86_64) Chrome/120.0"},
            {"timestamp": "2024-01-01T00:00:01", "level": "ERROR", "message": "Mock failure", "method": "GET", "url": "https://example.com/api/orders", "status_code": 499, "scenario_key": "sk-1", "scenario_name": "User Scenario", "service_name": "order-api"},
            {"timestamp": "2024-01-01T00:00:02", "level": "INFO", "message": "Mock success", "method": "POST", "url": "https://example.com/api/users", "status_code": 201, "scenario_key": "sk-2", "scenario_name": "Admin Scenario", "service_name": "user-api", "request_key": "rk-1", "test_title": "Create User"},
            {"timestamp": "2024-01-01T00:00:03", "type": "----- Scenario change delimiter -----", "previous_scenario_key": "sk-1", "current_scenario_key": "sk-2"},
            {"timestamp": "2024-01-01T00:00:04", "level": "ERROR", "message": "Mock failure", "method": "POST", "url": "https://other.com/api/data", "status_code": 500, "scenario_key": "sk-2", "scenario_name": "Admin Scenario", "service_name": "data-api", "namespace": "prod-ns"},
        ]

        with open(log_path, 'w') as f:
            for entry in entries:
                f.write(json.dumps(entry) + '\n')

        self.log_path = log_path
        yield

    def test_no_filters_returns_all_entries(self, capsys):
        """dump_logs with no filters returns all entries."""
        SimpleInterceptedRequestsLogger.dump_logs(filters=None)
        captured = capsys.readouterr()
        lines = [line for line in captured.out.strip().split('\n') if line]
        assert len(lines) == 5

    def test_filter_by_method(self, capsys):
        """Filter by HTTP method."""
        SimpleInterceptedRequestsLogger.dump_logs(filters={'method': 'GET'})
        captured = capsys.readouterr()
        assert 'Mock success' in captured.out
        assert 'Mock failure' in captured.out
        assert captured.out.count('"method": "GET"') == 2
        assert '"method": "POST"' not in captured.out

    def test_filter_by_status_code(self, capsys):
        """Filter by status code."""
        SimpleInterceptedRequestsLogger.dump_logs(filters={'status_code': 200})
        captured = capsys.readouterr()
        lines = [line for line in captured.out.strip().split('\n') if line]
        assert len(lines) == 1
        assert '"status_code": 200' in captured.out

    def test_filter_by_level(self, capsys):
        """Filter by log level."""
        SimpleInterceptedRequestsLogger.dump_logs(filters={'level': 'ERROR'})
        captured = capsys.readouterr()
        lines = [line for line in captured.out.strip().split('\n') if line]
        assert len(lines) == 2
        assert '"level": "ERROR"' in captured.out
        assert '"level": "INFO"' not in captured.out

    def test_filter_by_message(self, capsys):
        """Filter by message."""
        SimpleInterceptedRequestsLogger.dump_logs(filters={'message': 'Mock failure'})
        captured = capsys.readouterr()
        lines = [line for line in captured.out.strip().split('\n') if line]
        assert len(lines) == 2
        assert 'Mock failure' in captured.out
        assert 'Mock success' not in captured.out

    def test_filter_by_scenario_key(self, capsys):
        """Filter by scenario key."""
        SimpleInterceptedRequestsLogger.dump_logs(filters={'scenario_key': 'sk-2'})
        captured = capsys.readouterr()
        lines = [line for line in captured.out.strip().split('\n') if line]
        assert len(lines) == 2
        assert '"scenario_key": "sk-2"' in captured.out
        assert '"scenario_key": "sk-1"' not in captured.out

    def test_filter_by_scenario_name(self, capsys):
        """Filter by scenario name."""
        SimpleInterceptedRequestsLogger.dump_logs(filters={'scenario_name': 'User Scenario'})
        captured = capsys.readouterr()
        lines = [line for line in captured.out.strip().split('\n') if line]
        assert len(lines) == 2
        assert '"scenario_name": "User Scenario"' in captured.out
        assert '"scenario_name": "Admin Scenario"' not in captured.out

    def test_filter_by_service_name(self, capsys):
        """Filter by service name."""
        SimpleInterceptedRequestsLogger.dump_logs(filters={'service_name': 'user-api'})
        captured = capsys.readouterr()
        lines = [line for line in captured.out.strip().split('\n') if line]
        assert len(lines) == 2
        assert '"service_name": "user-api"' in captured.out

    def test_filter_by_url_substring(self, capsys):
        """Filter by URL substring."""
        SimpleInterceptedRequestsLogger.dump_logs(filters={'url': '/api/users'})
        captured = capsys.readouterr()
        lines = [line for line in captured.out.strip().split('\n') if line]
        assert len(lines) == 2
        assert 'https://example.com/api/users' in captured.out

    def test_filter_by_message_substring(self, capsys):
        """Filter by message substring."""
        SimpleInterceptedRequestsLogger.dump_logs(filters={'message': 'success'})
        captured = capsys.readouterr()
        lines = [line for line in captured.out.strip().split('\n') if line]
        assert len(lines) == 2
        assert 'Mock success' in captured.out
        assert 'Mock failure' not in captured.out

    def test_filter_by_scenario_name_substring(self, capsys):
        """Filter by scenario name substring."""
        SimpleInterceptedRequestsLogger.dump_logs(filters={'scenario_name': 'User'})
        captured = capsys.readouterr()
        lines = [line for line in captured.out.strip().split('\n') if line]
        assert len(lines) == 2
        assert '"scenario_name": "User Scenario"' in captured.out
        assert '"scenario_name": "Admin Scenario"' not in captured.out

    def test_filter_by_service_name_substring(self, capsys):
        """Filter by service name substring."""
        SimpleInterceptedRequestsLogger.dump_logs(filters={'service_name': 'user'})
        captured = capsys.readouterr()
        lines = [line for line in captured.out.strip().split('\n') if line]
        assert len(lines) == 2
        assert '"service_name": "user-api"' in captured.out

    def test_filter_by_test_title_substring(self, capsys):
        """Filter by test title substring."""
        SimpleInterceptedRequestsLogger.dump_logs(filters={'test_title': 'Create'})
        captured = capsys.readouterr()
        lines = [line for line in captured.out.strip().split('\n') if line]
        assert len(lines) == 1
        assert '"test_title": "Create User"' in captured.out

    def test_filter_by_user_agent_substring(self, capsys):
        """Filter by user agent substring."""
        SimpleInterceptedRequestsLogger.dump_logs(filters={'user_agent': 'Chrome'})
        captured = capsys.readouterr()
        lines = [line for line in captured.out.strip().split('\n') if line]
        assert len(lines) == 1
        assert 'Chrome/120.0' in captured.out

    def test_filter_by_request_key(self, capsys):
        """Filter by request key."""
        SimpleInterceptedRequestsLogger.dump_logs(filters={'request_key': 'rk-1'})
        captured = capsys.readouterr()
        lines = [line for line in captured.out.strip().split('\n') if line]
        assert len(lines) == 1
        assert '"request_key": "rk-1"' in captured.out

    def test_filter_by_test_title(self, capsys):
        """Filter by test title."""
        SimpleInterceptedRequestsLogger.dump_logs(filters={'test_title': 'Create User'})
        captured = capsys.readouterr()
        lines = [line for line in captured.out.strip().split('\n') if line]
        assert len(lines) == 1
        assert '"test_title": "Create User"' in captured.out

    def test_filter_by_namespace(self, capsys):
        """Filter by namespace."""
        SimpleInterceptedRequestsLogger.dump_logs(filters={'namespace': 'prod-ns'})
        captured = capsys.readouterr()
        lines = [line for line in captured.out.strip().split('\n') if line]
        assert len(lines) == 1
        assert '"namespace": "prod-ns"' in captured.out

    def test_multiple_filters_and_combined(self, capsys):
        """Multiple filters are AND-combined."""
        SimpleInterceptedRequestsLogger.dump_logs(filters={'method': 'GET', 'level': 'ERROR'})
        captured = capsys.readouterr()
        lines = [line for line in captured.out.strip().split('\n') if line]
        assert len(lines) == 1
        assert '"method": "GET"' in captured.out
        assert '"level": "ERROR"' in captured.out
        assert '"status_code": 499' in captured.out

    def test_filter_excludes_delimiters(self, capsys):
        """Delimiter entries are excluded when filtering."""
        SimpleInterceptedRequestsLogger.dump_logs(filters={'level': 'INFO'})
        captured = capsys.readouterr()
        assert 'delimiter' not in captured.out
        assert 'Mock success' in captured.out

    def test_filter_no_matches_prints_nothing(self, capsys):
        """No matches prints empty output."""
        SimpleInterceptedRequestsLogger.dump_logs(filters={'method': 'DELETE'})
        captured = capsys.readouterr()
        assert captured.out == ''

    def test_filter_level_case_insensitive(self, capsys):
        """Level filter is case-insensitive."""
        SimpleInterceptedRequestsLogger.dump_logs(filters={'level': 'info'})
        captured = capsys.readouterr()
        lines = [line for line in captured.out.strip().split('\n') if line]
        assert len(lines) == 2
        assert '"level": "INFO"' in captured.out

    def test_filter_missing_file_returns_gracefully(self, temp_log_dir):
        """Missing file with filters doesn't crash."""
        InterceptedRequestsLogger.set_file_path(os.path.join(temp_log_dir, 'nonexistent.log'))
        SimpleInterceptedRequestsLogger.dump_logs(filters={'method': 'GET'})
        # Should not raise an exception


class TestDumpLogsSelect:
    """Tests for dump_logs with --select flag."""

    @pytest.fixture(autouse=True)
    def setup_log_file(self, temp_log_dir):
        """Create a log file with multiple entries for select tests."""
        log_path = os.path.join(temp_log_dir, 'select_test.log')
        InterceptedRequestsLogger.set_file_path(log_path)

        entries = [
            {"timestamp": "2024-01-01T00:00:00", "level": "INFO", "message": "Mock success", "method": "GET", "url": "https://example.com/api/users", "status_code": 200, "scenario_key": "sk-1"},
            {"timestamp": "2024-01-01T00:00:01", "level": "ERROR", "message": "Mock failure", "method": "POST", "url": "https://example.com/api/orders", "status_code": 500, "scenario_key": "sk-2"},
            {"timestamp": "2024-01-01T00:00:02", "level": "INFO", "message": "Mock success", "method": "GET", "url": "https://example.com/api/products", "status_code": 200, "scenario_key": "sk-1"},
        ]

        with open(log_path, 'w') as f:
            for entry in entries:
                f.write(json.dumps(entry) + '\n')

        self.log_path = log_path
        yield

    def test_select_filters_fields(self, capsys):
        """Select parameter filters fields correctly."""
        SimpleInterceptedRequestsLogger.dump_logs(select=['timestamp', 'method', 'url'])
        captured = capsys.readouterr()

        # Should be table format (default when select is used)
        assert 'timestamp' in captured.out
        assert 'method' in captured.out
        assert 'url' in captured.out

        # Should NOT include other fields
        assert 'level' not in captured.out
        assert 'message' not in captured.out
        assert 'status_code' not in captured.out
        assert 'scenario_key' not in captured.out

    def test_select_with_format_json(self, capsys):
        """Select with format=json returns JSON array with selected fields."""
        SimpleInterceptedRequestsLogger.dump_logs(select=['method', 'url', 'status_code'], output_format='json')
        captured = capsys.readouterr()

        # Should be valid JSON array
        data = json.loads(captured.out)
        assert isinstance(data, list)
        assert len(data) == 3

        # Each entry should only have selected fields
        for entry in data:
            assert set(entry.keys()) == {'method', 'url', 'status_code'}

    def test_select_without_format_defaults_to_table(self, capsys):
        """Select without format defaults to table output."""
        SimpleInterceptedRequestsLogger.dump_logs(select=['method', 'status_code'])
        captured = capsys.readouterr()

        # Should be table format with headers
        lines = captured.out.strip().split('\n')
        assert len(lines) > 1  # Headers + data rows
        assert 'method' in lines[0]  # Header row
        assert 'status_code' in lines[0]  # Header row

    def test_select_with_format_simple(self, capsys):
        """Select with format=simple returns table."""
        SimpleInterceptedRequestsLogger.dump_logs(select=['timestamp', 'message'], output_format='simple')
        captured = capsys.readouterr()

        # Should be table format
        assert 'timestamp' in captured.out
        assert 'message' in captured.out
        assert 'Mock success' in captured.out
        assert 'Mock failure' in captured.out

    def test_select_with_without_headers(self, capsys):
        """Select with without_headers removes table headers."""
        SimpleInterceptedRequestsLogger.dump_logs(select=['method', 'url'], without_headers=True)
        captured = capsys.readouterr()

        lines = captured.out.strip().split('\n')
        # Should have data but first line should not be headers
        assert len(lines) == 3  # 3 data rows, no header
        assert 'method' not in lines[0]  # First line should be data, not headers
        assert 'GET' in lines[0] or 'POST' in lines[0]  # First line should be data

    def test_select_with_filters(self, capsys):
        """Select works with filters."""
        SimpleInterceptedRequestsLogger.dump_logs(
            select=['method', 'url', 'status_code'],
            filters={'method': 'GET'}
        )
        captured = capsys.readouterr()

        # Should be table with only GET requests
        assert 'GET' in captured.out
        assert 'POST' not in captured.out
        lines = captured.out.strip().split('\n')
        assert len(lines) == 3  # 1 header + 2 GET requests

    def test_select_nonexistent_field_ignored(self, capsys):
        """Non-existent fields in select are silently ignored."""
        SimpleInterceptedRequestsLogger.dump_logs(select=['timestamp', 'nonexistent_field', 'method'])
        captured = capsys.readouterr()

        # Should only show timestamp and method
        assert 'timestamp' in captured.out
        assert 'method' in captured.out
        assert 'nonexistent_field' not in captured.out

    def test_format_json_without_select_shows_all_fields(self, capsys):
        """Format=json without select shows all fields."""
        SimpleInterceptedRequestsLogger.dump_logs(output_format='json')
        captured = capsys.readouterr()

        data = json.loads(captured.out)
        assert isinstance(data, list)
        assert len(data) == 3

        # Should have all fields
        first_entry = data[0]
        assert 'timestamp' in first_entry
        assert 'level' in first_entry
        assert 'message' in first_entry
        assert 'method' in first_entry
        assert 'url' in first_entry
        assert 'status_code' in first_entry
        assert 'scenario_key' in first_entry

    def test_format_simple_without_select_shows_all_fields(self, capsys):
        """Format=simple without select shows all fields."""
        SimpleInterceptedRequestsLogger.dump_logs(output_format='simple')
        captured = capsys.readouterr()

        # Should be table with all fields
        assert 'timestamp' in captured.out
        assert 'level' in captured.out
        assert 'message' in captured.out
        assert 'method' in captured.out
        assert 'url' in captured.out
        assert 'status_code' in captured.out
        assert 'scenario_key' in captured.out

    def test_empty_select_shows_all_fields(self, capsys):
        """Empty select list shows all fields."""
        SimpleInterceptedRequestsLogger.dump_logs(select=[])
        captured = capsys.readouterr()

        # Should show all entries as JSON lines (backward compatible)
        lines = [line for line in captured.out.strip().split('\n') if line]
        assert len(lines) == 3
        for line in lines:
            entry = json.loads(line)
            assert 'timestamp' in entry
            assert 'method' in entry

    def test_backward_compatibility_no_select_no_format(self, capsys):
        """No select and no format maintains original JSON lines behavior."""
        SimpleInterceptedRequestsLogger.dump_logs()
        captured = capsys.readouterr()

        # Should be JSON lines format
        lines = [line for line in captured.out.strip().split('\n') if line]
        assert len(lines) == 3
        for line in lines:
            entry = json.loads(line)
            assert 'timestamp' in entry
            assert 'method' in entry
