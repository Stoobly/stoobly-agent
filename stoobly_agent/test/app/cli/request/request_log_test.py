import json
import os
import pdb
import pytest
import requests
import shutil
import tempfile
import time

from click.testing import CliRunner
from unittest.mock import patch

from stoobly_agent.app.cli.request_cli import request
from stoobly_agent.app.cli.scaffold.constants import (
    WORKFLOW_MOCK_TYPE,
    WORKFLOW_RECORD_TYPE,
    WORKFLOW_TEST_TYPE,
)
from stoobly_agent.app.settings import Settings
from stoobly_agent.app.proxy.constants.custom_response_codes import NOT_FOUND
from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.lib.intercepted_requests_logger import InterceptedRequestsLogger
from stoobly_agent.test.app.cli.scaffold.local.cli_invoker import LocalScaffoldCliInvoker
from stoobly_agent.test.test_helper import reset
from typing import Optional


def find_log_entry(output: str, message: str, method: str = None) -> Optional[dict]:
    """Find a log entry matching the given message and optional method."""
    for line in output.strip().split('\n'):
        if not line.strip():
            continue
        try:
            entry = json.loads(line)
            if entry.get('message') == message:
                if method is None or entry.get('method') == method:
                    return entry
        except json.JSONDecodeError:
            continue
    return None


@pytest.mark.e2e
class TestRequestLogE2e():

    @pytest.fixture(scope='class', autouse=True)
    def settings(self):
        return reset()

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
        yield "docs.stoobly.com"

    @pytest.fixture(scope='class')
    def service_name(self):
        yield "test-api"

    @pytest.fixture(scope='class', autouse=True)
    def target_workflow_name(self):
        yield WORKFLOW_MOCK_TYPE

    @pytest.fixture(scope="class", autouse=True)
    def proxy_url(self):
        return "http://localhost:8081"

    @pytest.fixture(scope="class", autouse=True)
    def create_scaffold_setup(self, settings, runner: CliRunner, app_dir_path: str, app_name: str, service_name: str, hostname: str):
        LocalScaffoldCliInvoker.cli_app_create(runner, app_dir_path, app_name)
        LocalScaffoldCliInvoker.cli_service_create(runner, app_dir_path, hostname, service_name, False)

    @pytest.fixture(scope="class", autouse=True)
    def workflow_up(self, create_scaffold_setup, runner: CliRunner, app_dir_path: str, target_workflow_name: str, settings: Settings):
        """Start mock workflow for testing."""
        LocalScaffoldCliInvoker.cli_workflow_up(runner, app_dir_path, target_workflow_name)
        time.sleep(1)
        settings.load()

    @pytest.fixture(scope="class", autouse=True)
    def workflow_down(self, workflow_up, runner: CliRunner, app_dir_path: str, proxy_url: str, target_workflow_name: str):
        yield

        LocalScaffoldCliInvoker.cli_workflow_down(runner, app_dir_path, target_workflow_name)
        time.sleep(1)

    def test_log_list_shows_mock_failures(self, app_dir_path, hostname, runner: CliRunner, proxy_url: str):
        """Test that 499 mock failures are logged and visible via request log list."""
        # Make an unrecorded request through proxy - should trigger 499
        # curl -x http://localhost:8081 -k 'https://docs.stoobly.com/test-unrecorded'
        res = requests.get(
            f'https://{hostname}/test-unrecorded',
            proxies={'http': proxy_url, 'https': proxy_url},
            verify=False
        )

        assert res.status_code == NOT_FOUND

        # Give time for async logging to complete
        time.sleep(0.5)

        # Invoke request log list
        result = runner.invoke(request, ['log', 'list', '--context-dir-path', app_dir_path])
        assert result.exit_code == 0

        output = result.output
        assert output, "Log output should not be empty"

        entry = find_log_entry(output, 'Mock failure')
        assert entry is not None, f"Expected to find 'Mock failure' log entry in output:\n{output}"

        # Check specific field values
        assert entry['level'] == 'ERROR'
        assert entry['method'] == 'GET'
        assert hostname in entry.get('url', '')
        assert entry['status_code'] == NOT_FOUND
        assert 'scenario_key' in entry

        # Assert these fields exist and are not null
        assert entry.get('timestamp'), "timestamp should exist and not be empty"
        assert entry.get('user_agent'), "user_agent should exist and not be empty"
        assert entry.get('latency_ms') is not None, "latency_ms should exist"

    def test_log_delete_clears_log_entries(self, app_dir_path, runner: CliRunner, proxy_url: str, hostname):
        """Test that request log delete clears all log entries."""
        # Make another request to ensure we have log entries
        requests.get(
            f'https://{hostname}/another-unrecorded',
            proxies={'http': proxy_url, 'https': proxy_url},
            verify=False
        )
        time.sleep(0.5)
        InterceptedRequestsLogger.shutdown()

        # Verify log has entries
        result = runner.invoke(request, ['log', 'list', '--context-dir-path', app_dir_path])
        assert result.exit_code == 0
        assert result.output.strip(), "Log should have entries before delete"

        # Delete log entries
        delete_result = runner.invoke(request, ['log', 'delete', '--context-dir-path', app_dir_path])
        assert delete_result.exit_code == 0

        # Verify log is now empty
        list_result = runner.invoke(request, ['log', 'list', '--context-dir-path', app_dir_path])
        assert list_result.exit_code == 0
        assert not list_result.output.strip(), f"Log should be empty after delete, got: {list_result.output}"

@pytest.mark.e2e
class TestRequestLogWithRecordedRequestsE2e():
    """Test logging behavior when we have both recorded and unrecorded requests."""

    @pytest.fixture(scope='class', autouse=True)
    def settings(self):
        return reset()

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
    def create_scaffold_setup(self, settings, runner: CliRunner, app_dir_path: str, app_name: str, service_name: str, hostname: str):
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
        settings.load()

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

    def test_successful_mock_logged_at_info_level(self, app_dir_path, record_then_mock_workflow, runner: CliRunner, proxy_url: str):
        """Test that successful mock requests are logged at INFO level (default)."""
        # Clear log first
        runner.invoke(request, ['log', 'delete', '--context-dir-path', app_dir_path])

        # Make the recorded request - should succeed with mocked response
        res = requests.get(
            'https://dog.ceo/api/breeds/list/all',
            proxies={'http': proxy_url, 'https': proxy_url},
            verify=False
        )

        time.sleep(0.5)
        InterceptedRequestsLogger.shutdown()

        list_result = runner.invoke(request, ['log', 'list', '--context-dir-path', app_dir_path])
        assert list_result.exit_code == 0

        if res.status_code != 200:
            assert False, f"Expected successful mock (200), got {res.status_code}. Response: {res.text}. Ensure the request was recorded properly before mocking."

        # If the request was successful (200), there should be a "Mock success" log entry
        # because default log level is INFO
        output = list_result.output
        entry = find_log_entry(output, 'Mock success')
        assert entry is not None, f"Expected Mock success log entry, got:\n{output}"

        # Check specific field values
        assert entry['level'] == 'INFO'
        assert entry['method'] == 'GET'
        assert 'dog.ceo' in entry.get('url', '')
        assert entry['status_code'] == 200
        assert 'scenario_key' in entry

        # Assert these fields exist and are not null
        assert entry.get('timestamp'), "timestamp should exist and not be empty"
        assert entry.get('user_agent'), "user_agent should exist and not be empty"
        assert entry.get('latency_ms') is not None, "latency_ms should exist"

    def test_unrecorded_request_logged_as_error(self, app_dir_path, record_then_mock_workflow, runner: CliRunner, proxy_url: str):
        """Test that unrecorded requests in mock mode are logged as errors."""
        # Clear log first
        runner.invoke(request, ['log', 'delete', '--context-dir-path', app_dir_path])

        # Make an unrecorded request - should trigger 499
        res = requests.get(
            'https://dog.ceo/api/breeds/unknown-endpoint',
            proxies={'http': proxy_url, 'https': proxy_url},
            verify=False
        )
        assert res.status_code == NOT_FOUND

        time.sleep(0.5)
        InterceptedRequestsLogger.shutdown()

        list_result = runner.invoke(request, ['log', 'list', '--context-dir-path', app_dir_path])
        assert list_result.exit_code == 0

        # Should have a Mock failure entry
        entry = find_log_entry(list_result.output, 'Mock failure')
        assert entry is not None, f"Expected Mock failure log entry, got:\n{list_result.output}"
        assert entry['level'] == 'ERROR'
        assert entry['status_code'] == NOT_FOUND

    def test_options_request_not_logged_as_failure(self, app_dir_path, record_then_mock_workflow, runner: CliRunner, proxy_url: str):
        """Test that OPTIONS requests are not logged as mock failures."""
        # Clear log first
        runner.invoke(request, ['log', 'delete', '--context-dir-path', app_dir_path])

        # Make an OPTIONS request - should get CORS response, not logged as failure
        res = requests.options(
            'https://dog.ceo/api/breeds/list/all',
            proxies={'http': proxy_url, 'https': proxy_url},
            verify=False
        )

        # OPTIONS requests should return 200 with CORS headers
        assert res.status_code == 200

        time.sleep(0.5)
        InterceptedRequestsLogger.shutdown()

        list_result = runner.invoke(request, ['log', 'list', '--context-dir-path', app_dir_path])
        assert list_result.exit_code == 0

        # Should NOT have a Mock failure entry for OPTIONS request
        entry = find_log_entry(list_result.output, 'Mock failure', method='OPTIONS')
        assert entry is None, f"OPTIONS request should not be logged as Mock failure, got log output:\n{list_result.output}"


@pytest.mark.e2e
class TestRequestLogWithTestWorkflowE2e():
    """Test logging behavior for the test scaffold workflow."""

    @pytest.fixture(scope='class', autouse=True)
    def settings(self):
        return reset()

    @pytest.fixture(scope='module')
    def runner(self):
        yield CliRunner()

    @pytest.fixture(scope='class')
    def app_name(self):
        yield "request-log-test-workflow-app"

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
        yield "dog-api-test"

    @pytest.fixture(scope="class", autouse=True)
    def proxy_url(self):
        return "http://localhost:8081"

    @pytest.fixture(scope="class", autouse=True)
    def create_scaffold_setup(self, settings, runner: CliRunner, app_dir_path: str, app_name: str, service_name: str, hostname: str):
        LocalScaffoldCliInvoker.cli_app_create(runner, app_dir_path, app_name)
        LocalScaffoldCliInvoker.cli_service_create(runner, app_dir_path, hostname, service_name, True)

    @pytest.fixture(scope="class", autouse=True)
    def record_then_test_workflow(self, create_scaffold_setup, runner: CliRunner, app_dir_path: str, proxy_url: str, settings: Settings):
        """Record a request, then switch to test workflow for testing."""
        # Start record workflow
        LocalScaffoldCliInvoker.cli_workflow_up(runner, app_dir_path, WORKFLOW_RECORD_TYPE)
        time.sleep(1)
        settings.load()

        # Record a request
        settings.proxy.intercept.active = True
        settings.commit()
        time.sleep(1)
        settings.load()

        requests.get(
            'https://dog.ceo/api/breeds/list/all',
            proxies={'http': proxy_url, 'https': proxy_url},
            verify=False
        )

        # Stop record workflow
        LocalScaffoldCliInvoker.cli_workflow_down(runner, app_dir_path, WORKFLOW_RECORD_TYPE)
        time.sleep(1)

        # Start test workflow
        LocalScaffoldCliInvoker.cli_workflow_up(runner, app_dir_path, WORKFLOW_TEST_TYPE)
        time.sleep(1)
        settings.load()

        yield

        # Cleanup: stop test workflow
        LocalScaffoldCliInvoker.cli_workflow_down(runner, app_dir_path, WORKFLOW_TEST_TYPE)
        time.sleep(1)

    def test_successful_test_logged_at_info_level(self, app_dir_path, record_then_test_workflow, runner: CliRunner, proxy_url: str):
        """Test that successful test requests are logged at INFO level."""
        # Clear log first
        runner.invoke(request, ['log', 'delete', WORKFLOW_TEST_TYPE, '--context-dir-path', app_dir_path])

        # Make the recorded request - should succeed with test comparison
        res = requests.get(
            'https://dog.ceo/api/breeds/list/all',
            proxies={'http': proxy_url, 'https': proxy_url},
            verify=False
        )

        time.sleep(0.5)
        InterceptedRequestsLogger.shutdown()

        list_result = runner.invoke(request, ['log', 'list', WORKFLOW_TEST_TYPE, '--context-dir-path', app_dir_path])
        assert list_result.exit_code == 0

        if res.status_code != 200:
            assert False, f"Expected successful test (200), got {res.status_code}. Response: {res.text}."

        # Should have a "Mock success" log entry (test workflow uses mock mode)
        output = list_result.output
        entry = find_log_entry(output, 'Mock success')
        assert entry is not None, f"Expected Mock success log entry, got:\n{output}"

        # Check specific field values
        assert entry['level'] == 'INFO'
        assert entry['method'] == 'GET'
        assert 'dog.ceo' in entry.get('url', '')
        assert entry['status_code'] == 200
        assert 'scenario_key' in entry

        # Assert these fields exist and are not null
        assert entry.get('timestamp'), "timestamp should exist and not be empty"
        assert entry.get('user_agent'), "user_agent should exist and not be empty"
        assert entry.get('latency_ms') is not None, "latency_ms should exist"

    def test_unrecorded_request_logged_as_test_failure(self, app_dir_path, record_then_test_workflow, runner: CliRunner, proxy_url: str):
        """Test that unrecorded requests in test mode are logged as test failures."""
        # Clear log first
        runner.invoke(request, ['log', 'delete', WORKFLOW_TEST_TYPE, '--context-dir-path', app_dir_path])

        # Make an unrecorded request - should trigger test failure
        res = requests.get(
            'https://dog.ceo/api/breeds/unknown-endpoint',
            proxies={'http': proxy_url, 'https': proxy_url},
            verify=False
        )
        assert res.status_code == NOT_FOUND

        time.sleep(0.5)
        InterceptedRequestsLogger.shutdown()

        list_result = runner.invoke(request, ['log', 'list', WORKFLOW_TEST_TYPE, '--context-dir-path', app_dir_path])
        assert list_result.exit_code == 0

        # Should have a Mock failure entry (test workflow uses mock mode)
        entry = find_log_entry(list_result.output, 'Mock failure')
        assert entry is not None, f"Expected Mock failure log entry, got:\n{list_result.output}"
        assert entry['level'] == 'ERROR'
        assert entry['status_code'] == NOT_FOUND

    def test_options_request_not_logged_as_test_failure(self, app_dir_path, record_then_test_workflow, runner: CliRunner, proxy_url: str):
        """Test that OPTIONS requests are not logged as test failures."""
        # Clear log first
        runner.invoke(request, ['log', 'delete', WORKFLOW_TEST_TYPE, '--context-dir-path', app_dir_path])

        # Make an OPTIONS request - should get CORS response, not logged as failure
        res = requests.options(
            'https://dog.ceo/api/breeds/list/all',
            proxies={'http': proxy_url, 'https': proxy_url},
            verify=False
        )

        # OPTIONS requests should return 200 with CORS headers
        assert res.status_code == 200

        time.sleep(0.5)
        InterceptedRequestsLogger.shutdown()

        list_result = runner.invoke(request, ['log', 'list', WORKFLOW_TEST_TYPE, '--context-dir-path', app_dir_path])
        assert list_result.exit_code == 0

        # Should NOT have a Mock failure entry for OPTIONS request
        entry = find_log_entry(list_result.output, 'Mock failure', method='OPTIONS')
        assert entry is None, f"OPTIONS request should not be logged as Test failure, got log output:\n{list_result.output}"


@pytest.mark.e2e
class TestRequestLogFromDifferentWorkingDirectory():
    """Test that --context-dir-path flag allows viewing logs from a different working directory."""

    @pytest.fixture(scope='class', autouse=True)
    def settings(self):
        return reset()

    @pytest.fixture(scope='module')
    def runner(self):
        yield CliRunner()

    @pytest.fixture(scope='class')
    def app_name(self):
        yield "request-log-diff-cwd-app"

    @pytest.fixture(scope='class', autouse=True)
    def app_dir_path(self):
        data_dir: DataDir = DataDir.instance()
        path = os.path.abspath(os.path.join(data_dir.tmp_dir_path, '..', '..'))
        yield path

    @pytest.fixture(scope='class')
    def different_working_dir(self):
        """Create a completely different directory to simulate user's actual working directory.

        Uses tempfile.mkdtemp directly in /tmp to ensure the directory is truly isolated
        and has no .stoobly folder in any parent directory (which DataDir.find_data_dir would find).
        """
        different_dir = tempfile.mkdtemp(prefix="different_cwd_", dir="/tmp")
        yield different_dir
        shutil.rmtree(different_dir, ignore_errors=True)

    @pytest.fixture(scope='class')
    def hostname(self):
        yield "docs.stoobly.com"

    @pytest.fixture(scope='class')
    def service_name(self):
        yield "test-api-diff-cwd"

    @pytest.fixture(scope='class', autouse=True)
    def target_workflow_name(self):
        yield WORKFLOW_MOCK_TYPE

    @pytest.fixture(scope="class", autouse=True)
    def proxy_url(self):
        return "http://localhost:8081"

    @pytest.fixture(scope="class", autouse=True)
    def create_scaffold_setup(self, settings, runner: CliRunner, app_dir_path: str, app_name: str, service_name: str, hostname: str):
        LocalScaffoldCliInvoker.cli_app_create(runner, app_dir_path, app_name)
        LocalScaffoldCliInvoker.cli_service_create(runner, app_dir_path, hostname, service_name, False)

    @pytest.fixture(scope="class", autouse=True)
    def workflow_up(self, create_scaffold_setup, runner: CliRunner, app_dir_path: str, target_workflow_name: str, settings: Settings):
        """Start mock workflow for testing."""
        LocalScaffoldCliInvoker.cli_workflow_up(runner, app_dir_path, target_workflow_name)
        time.sleep(1)
        settings.load()

    @pytest.fixture(scope="class", autouse=True)
    def workflow_down(self, workflow_up, runner: CliRunner, app_dir_path: str, proxy_url: str, target_workflow_name: str):
        yield

        LocalScaffoldCliInvoker.cli_workflow_down(runner, app_dir_path, target_workflow_name)
        time.sleep(1)

    def test_log_list_with_context_dir_path_from_different_directory(
        self, app_dir_path: str, different_working_dir: str, hostname: str, runner: CliRunner, proxy_url: str
    ):
        """
        Test that request log list works with --context-dir-path when running from a different directory.

        This simulates the bug where users cd to their app directory but logs are in the context directory.
        Without --context-dir-path, logs would not be found.
        With --context-dir-path pointing to the correct location, logs are retrieved.
        """
        # Clear any existing logs
        runner.invoke(request, ['log', 'delete', '--context-dir-path', app_dir_path])

        # Make a request to generate log entries
        res = requests.get(
            f'https://{hostname}/test-different-cwd',
            proxies={'http': proxy_url, 'https': proxy_url},
            verify=False
        )
        assert res.status_code == NOT_FOUND

        time.sleep(0.5)
        InterceptedRequestsLogger.shutdown()

        # Save original directory
        original_cwd = os.getcwd()

        # Save the original DataDir instances to restore later
        original_data_dir_instances = DataDir._instances

        try:
            # Change to a completely different directory (simulating user being in their app dir)
            os.chdir(different_working_dir)

            # Reset DataDir singleton cache to force fresh lookup from new cwd
            # This is critical because DataDir.instance() is cached at module import time
            # in request_cli.py, and we need a fresh lookup for the test to work correctly
            DataDir._instances = None

            # Without --context-dir-path, logs should not be found (empty output or error)
            result_without_flag = runner.invoke(request, ['log', 'list'])
            # The output should be empty because there's no .stoobly in different_working_dir
            assert not result_without_flag.output.strip() or 'Mock failure' not in result_without_flag.output, \
                "Logs should NOT be found without --context-dir-path from a different directory"

            # With --context-dir-path, logs SHOULD be found
            result_with_flag = runner.invoke(request, ['log', 'list', '--context-dir-path', app_dir_path])
            assert result_with_flag.exit_code == 0
            assert result_with_flag.output.strip(), "Logs should be found with --context-dir-path"

            entry = find_log_entry(result_with_flag.output, 'Mock failure')
            assert entry is not None, f"Expected 'Mock failure' log entry with --context-dir-path, got:\n{result_with_flag.output}"
            assert entry['level'] == 'ERROR'
            assert hostname in entry.get('url', '')

        finally:
            # Restore original directory and DataDir instances
            os.chdir(original_cwd)
            DataDir._instances = original_data_dir_instances


class TestRequestLogCliParams:
    """Unit tests for CLI parameter handling (not E2E)."""

    @pytest.fixture(scope='class', autouse=True)
    def settings(self):
        return reset()

    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_log_list_without_args_uses_defaults(self, runner):
        """request log list without args passes None for both params."""
        with patch.object(InterceptedRequestsLogger, 'dump_logs') as mock_dump:
            result = runner.invoke(request, ['log', 'list'])
            assert result.exit_code == 0
            mock_dump.assert_called_once_with(workflow=None, namespace=None, data_dir_path=None)

    def test_log_delete_without_args_uses_defaults(self, runner):
        """request log delete without args passes None for both params."""
        with patch.object(InterceptedRequestsLogger, 'truncate') as mock_truncate:
            result = runner.invoke(request, ['log', 'delete'])
            assert result.exit_code == 0
            mock_truncate.assert_called_once_with(workflow=None, namespace=None, data_dir_path=None)

    def test_log_list_accepts_workflow_name_argument(self, runner):
        """request log list accepts workflow_name as positional argument."""
        with patch.object(InterceptedRequestsLogger, 'dump_logs') as mock_dump:
            result = runner.invoke(request, ['log', 'list', 'mock'])
            assert result.exit_code == 0
            mock_dump.assert_called_once_with(workflow='mock', namespace=None, data_dir_path=None)

    def test_log_list_accepts_namespace_option(self, runner):
        """request log list accepts --namespace option."""
        with patch.object(InterceptedRequestsLogger, 'dump_logs') as mock_dump:
            result = runner.invoke(request, ['log', 'list', '--namespace', 'test-ns'])
            assert result.exit_code == 0
            mock_dump.assert_called_once_with(workflow=None, namespace='test-ns', data_dir_path=None)

    def test_log_list_accepts_both_workflow_and_namespace(self, runner):
        """request log list accepts both workflow_name and --namespace."""
        with patch.object(InterceptedRequestsLogger, 'dump_logs') as mock_dump:
            result = runner.invoke(request, ['log', 'list', 'record', '--namespace', 'prod'])
            assert result.exit_code == 0
            mock_dump.assert_called_once_with(workflow='record', namespace='prod', data_dir_path=None)

    def test_log_delete_accepts_workflow_name_argument(self, runner):
        """request log delete accepts workflow_name as positional argument."""
        with patch.object(InterceptedRequestsLogger, 'truncate') as mock_truncate:
            result = runner.invoke(request, ['log', 'delete', 'mock'])
            assert result.exit_code == 0
            mock_truncate.assert_called_once_with(workflow='mock', namespace=None, data_dir_path=None)

    def test_log_delete_accepts_namespace_option(self, runner):
        """request log delete accepts --namespace option."""
        with patch.object(InterceptedRequestsLogger, 'truncate') as mock_truncate:
            result = runner.invoke(request, ['log', 'delete', '--namespace', 'test-ns'])
            assert result.exit_code == 0
            mock_truncate.assert_called_once_with(workflow=None, namespace='test-ns', data_dir_path=None)

    def test_log_delete_accepts_both_workflow_and_namespace(self, runner):
        """request log delete accepts both workflow_name and --namespace."""
        with patch.object(InterceptedRequestsLogger, 'truncate') as mock_truncate:
            result = runner.invoke(request, ['log', 'delete', 'record', '--namespace', 'prod'])
            assert result.exit_code == 0
            mock_truncate.assert_called_once_with(workflow='record', namespace='prod', data_dir_path=None)
