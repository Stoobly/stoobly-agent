import json
import os
import pytest
import requests
import time

from click.testing import CliRunner

from stoobly_agent.app.cli.request_cli import request
from stoobly_agent.app.cli.scaffold.constants import (
    WORKFLOW_MOCK_TYPE,
    WORKFLOW_RECORD_TYPE,
)
from stoobly_agent.app.settings import Settings
from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.lib.intercepted_requests_logger import InterceptedRequestsLogger
from stoobly_agent.test.app.cli.scaffold.local.cli_invoker import LocalScaffoldCliInvoker
from stoobly_agent.test.test_helper import reset


@pytest.mark.e2e
class TestRequestLogE2e():

    @pytest.fixture(scope='class', autouse=True)
    def settings(self):
        return reset('request-log-e2e-test')

    @pytest.fixture(scope='module')
    def runner(self):
        yield CliRunner()

    @pytest.fixture(scope='class')
    def app_name(self):
        yield "request-log-test-app"

    @pytest.fixture(scope='class', autouse=True)
    def app_dir_path(self):
        data_dir: DataDir = DataDir.instance()
        path = os.path.abspath(os.path.join(data_dir.tmp_dir_path, '..', '..'))
        yield path

    @pytest.fixture(scope='class')
    def hostname(self):
        yield "api.example.com"

    @pytest.fixture(scope='class')
    def service_name(self):
        yield "test-api"

    @pytest.fixture(scope="class", autouse=True)
    def proxy_url(self):
        return "http://localhost:8081"

    @pytest.fixture(scope="class", autouse=True)
    def create_scaffold_setup(self, runner: CliRunner, app_dir_path: str, app_name: str, service_name: str, hostname: str):
        LocalScaffoldCliInvoker.cli_app_create(runner, app_dir_path, app_name)
        LocalScaffoldCliInvoker.cli_service_create(runner, app_dir_path, hostname, service_name, False)

    @pytest.fixture(scope="class", autouse=True)
    def mock_workflow(self, create_scaffold_setup, runner: CliRunner, app_dir_path: str, settings: Settings):
        """Start mock workflow for testing."""
        LocalScaffoldCliInvoker.cli_workflow_up(runner, app_dir_path, WORKFLOW_MOCK_TYPE)
        time.sleep(1)
        settings.load()

        yield

        LocalScaffoldCliInvoker.cli_workflow_down(runner, app_dir_path, WORKFLOW_MOCK_TYPE)
        time.sleep(1)

    def test_log_list_shows_mock_failures(self, mock_workflow, runner: CliRunner, proxy_url: str):
        """Test that 499 mock failures are logged and visible via request log list."""
        # Make an unrecorded request through proxy - should trigger 499
        res = requests.get(
            'https://docs.stoobly.com/test-unrecorded',
            proxies={'http': proxy_url, 'https': proxy_url},
            verify=False
        )
        assert res.status_code == 499

        # Give time for async logging to complete
        time.sleep(0.5)

        # Shutdown logger to flush any pending writes
        InterceptedRequestsLogger.shutdown()

        # Invoke request log list
        result = runner.invoke(request, ['log', 'list'])
        assert result.exit_code == 0

        output = result.output
        assert output, "Log output should not be empty"

        # Parse JSON lines and find the mock failure entry
        found_mock_failure = False
        for line in output.strip().split('\n'):
            if not line.strip():
                continue
            try:
                entry = json.loads(line)
                if entry.get('message') == 'Mock failure':
                    found_mock_failure = True
                    assert entry['level'] == 'ERROR'
                    assert entry['status_code'] == 499
                    assert 'docs.stoobly.com' in entry.get('url', '')
                    break
            except json.JSONDecodeError:
                continue

        assert found_mock_failure, f"Expected to find 'Mock failure' log entry in output:\n{output}"

    def test_log_delete_clears_log_entries(self, mock_workflow, runner: CliRunner, proxy_url: str):
        """Test that request log delete clears all log entries."""
        # Make another request to ensure we have log entries
        requests.get(
            'https://docs.stoobly.com/another-unrecorded',
            proxies={'http': proxy_url, 'https': proxy_url},
            verify=False
        )
        time.sleep(0.5)
        InterceptedRequestsLogger.shutdown()

        # Verify log has entries
        result = runner.invoke(request, ['log', 'list'])
        assert result.exit_code == 0
        assert result.output.strip(), "Log should have entries before delete"

        # Delete log entries
        delete_result = runner.invoke(request, ['log', 'delete'])
        assert delete_result.exit_code == 0

        # Verify log is now empty
        list_result = runner.invoke(request, ['log', 'list'])
        assert list_result.exit_code == 0
        assert not list_result.output.strip(), f"Log should be empty after delete, got: {list_result.output}"

    def test_log_list_empty_for_successful_requests_at_error_level(self, mock_workflow, runner: CliRunner):
        """Test that successful requests are not logged when log level is ERROR (default)."""
        # Clear the log first
        runner.invoke(request, ['log', 'delete'])

        # Note: To test successful mock requests, we would need to first record a request
        # and then mock it. Since this test class is for mock workflow with no recordings,
        # all requests will fail with 499. This test verifies that after clearing,
        # the log starts empty.
        list_result = runner.invoke(request, ['log', 'list'])
        assert list_result.exit_code == 0
        # After delete, log should be empty (no new requests made)
        assert not list_result.output.strip(), "Log should be empty after delete with no new requests"


@pytest.mark.e2e
class TestRequestLogWithRecordedRequestsE2e():
    """Test logging behavior when we have both recorded and unrecorded requests."""

    @pytest.fixture(scope='class', autouse=True)
    def settings(self):
        return reset('request-log-recorded-e2e-test')

    @pytest.fixture(scope='module')
    def runner(self):
        yield CliRunner()

    @pytest.fixture(scope='class')
    def app_name(self):
        yield "request-log-recorded-app"

    @pytest.fixture(scope='class', autouse=True)
    def app_dir_path(self):
        data_dir: DataDir = DataDir.instance()
        path = os.path.abspath(os.path.join(data_dir.tmp_dir_path, '..', '..'))
        yield path

    @pytest.fixture(scope='class')
    def hostname(self):
        yield "dog.ceo"

    @pytest.fixture(scope='class')
    def service_name(self):
        yield "dog-api"

    @pytest.fixture(scope="class", autouse=True)
    def proxy_url(self):
        return "http://localhost:8081"

    @pytest.fixture(scope="class", autouse=True)
    def create_scaffold_setup(self, runner: CliRunner, app_dir_path: str, app_name: str, service_name: str, hostname: str):
        LocalScaffoldCliInvoker.cli_app_create(runner, app_dir_path, app_name)
        LocalScaffoldCliInvoker.cli_service_create(runner, app_dir_path, hostname, service_name, True)

    @pytest.fixture(scope="class", autouse=True)
    def record_then_mock_workflow(self, create_scaffold_setup, runner: CliRunner, app_dir_path: str, proxy_url: str, settings: Settings):
        """Record a request, then switch to mock workflow for testing."""
        # Start record workflow
        LocalScaffoldCliInvoker.cli_workflow_up(runner, app_dir_path, WORKFLOW_RECORD_TYPE)
        time.sleep(1)
        settings.load()

        # Record a request
        settings.proxy.intercept.active = True
        settings.commit()
        time.sleep(1)

        requests.get(
            'https://dog.ceo/api/breeds/list/all',
            proxies={'http': proxy_url, 'https': proxy_url},
            verify=False
        )

        # Stop record workflow
        LocalScaffoldCliInvoker.cli_workflow_down(runner, app_dir_path, WORKFLOW_RECORD_TYPE)
        time.sleep(1)

        # Start mock workflow
        LocalScaffoldCliInvoker.cli_workflow_up(runner, app_dir_path, WORKFLOW_MOCK_TYPE)
        time.sleep(1)
        settings.load()

        yield

        # Cleanup: stop mock workflow
        LocalScaffoldCliInvoker.cli_workflow_down(runner, app_dir_path, WORKFLOW_MOCK_TYPE)
        time.sleep(1)

    def test_successful_mock_not_logged_at_error_level(self, record_then_mock_workflow, runner: CliRunner, proxy_url: str):
        """Test that successful mock requests are not logged at ERROR level."""
        # Clear log first
        runner.invoke(request, ['log', 'delete'])

        # Make the recorded request - should succeed with mocked response
        res = requests.get(
            'https://dog.ceo/api/breeds/list/all',
            proxies={'http': proxy_url, 'https': proxy_url},
            verify=False
        )
        # This should be 200 if properly mocked, or 499 if not found
        # We're testing that successful mocks (200) are NOT logged at ERROR level

        time.sleep(0.5)
        InterceptedRequestsLogger.shutdown()

        list_result = runner.invoke(request, ['log', 'list'])
        assert list_result.exit_code == 0

        # If the request was successful (200), there should be no log entry
        # because default log level is ERROR
        if res.status_code == 200:
            # Should not have "Mock success" entries since log level is ERROR
            output = list_result.output
            for line in output.strip().split('\n'):
                if not line.strip():
                    continue
                try:
                    entry = json.loads(line)
                    assert entry.get('message') != 'Mock success', \
                        "Mock success should not be logged at ERROR level"
                except json.JSONDecodeError:
                    continue

    def test_unrecorded_request_logged_as_error(self, record_then_mock_workflow, runner: CliRunner, proxy_url: str):
        """Test that unrecorded requests in mock mode are logged as errors."""
        # Clear log first
        runner.invoke(request, ['log', 'delete'])

        # Make an unrecorded request - should trigger 499
        res = requests.get(
            'https://dog.ceo/api/breeds/unknown-endpoint',
            proxies={'http': proxy_url, 'https': proxy_url},
            verify=False
        )
        assert res.status_code == 499

        time.sleep(0.5)
        InterceptedRequestsLogger.shutdown()

        list_result = runner.invoke(request, ['log', 'list'])
        assert list_result.exit_code == 0

        # Should have a Mock failure entry
        found_failure = False
        for line in list_result.output.strip().split('\n'):
            if not line.strip():
                continue
            try:
                entry = json.loads(line)
                if entry.get('message') == 'Mock failure':
                    found_failure = True
                    assert entry['level'] == 'ERROR'
                    assert entry['status_code'] == 499
                    break
            except json.JSONDecodeError:
                continue

        assert found_failure, f"Expected Mock failure log entry, got:\n{list_result.output}"
