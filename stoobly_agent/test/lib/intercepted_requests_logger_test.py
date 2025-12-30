import json
import os
import shutil
import tempfile
from datetime import datetime
from unittest.mock import MagicMock, PropertyMock, patch

import pytest

from stoobly_agent.lib.intercepted_requests_logger import InterceptedRequestsLogger
from stoobly_agent.lib.logger import DEBUG, ERROR, INFO
from stoobly_agent.test.test_helper import reset


@pytest.fixture(autouse=True, scope='module')
def settings():
    return reset('intercepted-requests-logger-test')


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

        with open(self.log_path, 'r') as f:
            content = f.read()
            assert "Test info message" in content

    def test_logs_with_request(self, mock_mitmproxy_request):
        """Request data extracted (method, URL)."""
        with patch('stoobly_agent.lib.intercepted_requests_logger.InterceptSettings') as mock_intercept:
            mock_intercept.return_value.scenario_key = None
            InterceptedRequestsLogger.info("Request log", request=mock_mitmproxy_request)

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

        with open(self.log_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                entry = json.loads(line.strip())
                if entry.get('message') == 'Long URL test':
                    assert len(entry['url']) == 103  # 100 + '...'
                    assert entry['url'].endswith('...')
                    return
            pytest.fail("Long URL test entry not found")


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
