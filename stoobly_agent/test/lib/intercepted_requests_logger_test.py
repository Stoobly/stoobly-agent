import json
import os
import shutil
import tempfile
from datetime import datetime
from unittest.mock import MagicMock, PropertyMock, patch

import pytest

from stoobly_agent.config.constants import custom_headers
from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.lib.intercepted_requests_logger import InterceptedRequestsLogger
from stoobly_agent.lib.logger import DEBUG, ERROR, INFO
from stoobly_agent.test.test_helper import reset


@pytest.fixture(autouse=True, scope='module')
def settings():
    return reset()


@pytest.fixture(autouse=True)
def reset_logger_state():
    """Reset class-level state before each test."""
    InterceptedRequestsLogger._InterceptedRequestsLogger__file_path = None
    InterceptedRequestsLogger._InterceptedRequestsLogger__previous_scenario_key = None
    InterceptedRequestsLogger._InterceptedRequestsLogger__queue_listener = None
    InterceptedRequestsLogger._InterceptedRequestsLogger__log_queue = None
    InterceptedRequestsLogger._InterceptedRequestsLogger__file_handler = None
    InterceptedRequestsLogger._InterceptedRequestsLogger__logger.handlers.clear()
    InterceptedRequestsLogger._InterceptedRequestsLogger__logger.disabled = True
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

        assert InterceptedRequestsLogger._InterceptedRequestsLogger__file_path == custom_path

    def test_enable_logger_file_creates_file(self, temp_log_dir):
        """Verify log file is created."""
        log_path = os.path.join(temp_log_dir, 'test.log')
        InterceptedRequestsLogger.set_file_path(log_path)
        InterceptedRequestsLogger.enable_logger_file()

        with patch('stoobly_agent.lib.intercepted_requests_logger.InterceptSettings') as mock_intercept:
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
        InterceptedRequestsLogger.enable_logger_file()
        InterceptedRequestsLogger.set_log_level(DEBUG)
        self.log_path = log_path
        yield
        InterceptedRequestsLogger.shutdown()

    def test_info_logs_message(self):
        """Basic info logging works."""
        with patch('stoobly_agent.lib.intercepted_requests_logger.InterceptSettings') as mock_intercept:
            mock_intercept.return_value.scenario_key = None
            InterceptedRequestsLogger.info("Test info message")

        InterceptedRequestsLogger.flush()

        with open(self.log_path, 'r') as f:
            content = f.read()
            assert "Test info message" in content

    def test_logs_with_request(self, mock_mitmproxy_request):
        """Request data extracted (method, URL)."""
        with patch('stoobly_agent.lib.intercepted_requests_logger.InterceptSettings') as mock_intercept:
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
        with patch('stoobly_agent.lib.intercepted_requests_logger.InterceptSettings') as mock_intercept:
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

        with patch('stoobly_agent.lib.intercepted_requests_logger.InterceptSettings') as mock_intercept:
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
        InterceptedRequestsLogger.enable_logger_file()
        InterceptedRequestsLogger.set_log_level(DEBUG)
        self.log_path = log_path
        yield
        InterceptedRequestsLogger.shutdown()

    def test_formats_as_valid_json(self):
        """Output is valid JSON with required fields."""
        with patch('stoobly_agent.lib.intercepted_requests_logger.InterceptSettings') as mock_intercept:
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

        with patch('stoobly_agent.lib.intercepted_requests_logger.InterceptSettings') as mock_intercept:
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
        InterceptedRequestsLogger.enable_logger_file()

        with patch('stoobly_agent.lib.intercepted_requests_logger.InterceptSettings') as mock_intercept:
            mock_intercept.return_value.scenario_key = None
            InterceptedRequestsLogger.info("Dump test message")

        InterceptedRequestsLogger.flush()
        InterceptedRequestsLogger.shutdown()
        InterceptedRequestsLogger.dump_logs()

        captured = capsys.readouterr()
        assert "Dump test message" in captured.out

    def test_truncate_clears_file(self, temp_log_dir):
        """truncate() clears log file."""
        log_path = os.path.join(temp_log_dir, 'truncate_test.log')
        InterceptedRequestsLogger.set_file_path(log_path)
        InterceptedRequestsLogger.enable_logger_file()

        with patch('stoobly_agent.lib.intercepted_requests_logger.InterceptSettings') as mock_intercept:
            mock_intercept.return_value.scenario_key = None
            InterceptedRequestsLogger.info("Before truncate")

        InterceptedRequestsLogger.flush()
        InterceptedRequestsLogger.truncate()

        with open(log_path, 'r') as f:
            content = f.read()
            assert "Before truncate" not in content

    def test_shutdown_clears_handlers(self, temp_log_dir):
        """shutdown() cleans up handlers."""
        log_path = os.path.join(temp_log_dir, 'shutdown_test.log')
        InterceptedRequestsLogger.set_file_path(log_path)
        InterceptedRequestsLogger.enable_logger_file()

        InterceptedRequestsLogger.shutdown()

        assert len(InterceptedRequestsLogger._InterceptedRequestsLogger__logger.handlers) == 0
        assert InterceptedRequestsLogger._InterceptedRequestsLogger__file_handler is None


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
        log_dir = os.path.join(self.temp_dir, 'tmp', workflow, namespace, 'logs')
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, f'{workflow}.json')

        with open(log_file, 'w') as f:
            f.write('{"message": "test log entry"}\n')

        with patch.object(DataDir, 'instance') as mock_data_dir:
            mock_data_dir.return_value.path = self.temp_dir
            InterceptedRequestsLogger.dump_logs(workflow=workflow, namespace=namespace)

        captured = capsys.readouterr()
        assert 'test log entry' in captured.out

    def test_truncate_with_workflow_and_namespace(self):
        """truncate() operates on correct file when workflow/namespace specified."""
        workflow = 'record'
        namespace = 'prod-ns'
        log_dir = os.path.join(self.temp_dir, 'tmp', workflow, namespace, 'logs')
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, f'{workflow}.json')

        # Create file with content
        with open(log_file, 'w') as f:
            f.write('{"message": "should be cleared"}\n')

        with patch.object(DataDir, 'instance') as mock_data_dir:
            mock_data_dir.return_value.path = self.temp_dir
            InterceptedRequestsLogger.truncate(workflow=workflow, namespace=namespace)

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
