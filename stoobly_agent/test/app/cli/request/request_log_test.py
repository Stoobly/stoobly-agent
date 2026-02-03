import json
import os
import pytest
import requests
import signal
import socket
import subprocess
import sys
import time

from click.testing import CliRunner
from typing import Optional
from unittest.mock import patch

from stoobly_agent.app.cli.intercept_cli import intercept
from stoobly_agent.app.cli.request_cli import request
from stoobly_agent.app.proxy.constants.custom_response_codes import NOT_FOUND
from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.lib.intercepted_requests.simple_logger import SimpleInterceptedRequestsLogger
from stoobly_agent.test.test_helper import reset


class TestRequestLogCliParams:
    """Unit tests for non-scaffold request log CLI parameter handling."""

    @pytest.fixture(scope='class', autouse=True)
    def settings(self):
        return reset()

    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_log_list_calls_dump_logs(self, runner):
        """request log list calls dump_logs for non-scaffold use."""
        with patch.object(SimpleInterceptedRequestsLogger, 'dump_logs') as mock_dump:
            result = runner.invoke(request, ['log', 'list'])
            assert result.exit_code == 0
            mock_dump.assert_called_once_with(data_dir_path=DataDir.instance().context_dir_path)

    def test_log_delete_calls_truncate(self, runner):
        """request log delete calls truncate for non-scaffold use."""
        with patch.object(SimpleInterceptedRequestsLogger, 'truncate') as mock_truncate:
            result = runner.invoke(request, ['log', 'delete'])
            assert result.exit_code == 0
            mock_truncate.assert_called_once_with(data_dir_path=DataDir.instance().context_dir_path)

    def test_log_path_calls_get_log_file_path(self, runner):
        """request log path calls get_log_file_path for non-scaffold use."""
        with patch.object(SimpleInterceptedRequestsLogger, 'get_log_file_path') as mock_get:
            result = runner.invoke(request, ['log', 'path'])
            assert result.exit_code == 0
            mock_get.assert_called_once_with(data_dir_path=DataDir.instance().context_dir_path)


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
    """E2e tests for non-scaffold request log commands using stoobly-agent run."""

    @pytest.fixture(scope='class', autouse=True)
    def settings(self):
        return reset()

    @pytest.fixture(scope='module')
    def runner(self):
        yield CliRunner()

    @pytest.fixture(scope='class')
    def hostname(self):
        yield "docs.stoobly.com"

    @pytest.fixture(scope='class', autouse=True)
    def proxy_port(self):
        yield 8082

    @pytest.fixture(scope='class', autouse=True)
    def proxy_url(self, proxy_port):
        return f"http://localhost:{proxy_port}"

    @pytest.fixture(scope='class', autouse=True)
    def configure_mock_policy(self, settings):
        """Set mock policy to ALL so unmatched requests return 499 instead of proxying upstream."""
        runner = CliRunner()
        result = runner.invoke(intercept, ['configure', '--mode', 'mock', '--policy', 'all'])
        assert result.exit_code == 0

    @pytest.fixture(scope='class', autouse=True)
    def proxy_pid(self, settings, proxy_port, configure_mock_policy):
        """Start stoobly-agent run in detached mode with request logging enabled."""
        log_output_path = os.path.join(os.getcwd(), 'proxy-run.log')

        result = subprocess.run(
            [
                sys.executable, '-m', 'stoobly_agent',
                'run',
                '--detached', log_output_path,
                '--request-log-enable',
                '--intercept',
                '--intercept-mode', 'mock',
                '--headless',
                '--proxy-port', str(proxy_port),
                '--ssl-insecure',
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0, f"Failed to start proxy: {result.stderr}"
        pid = int(result.stdout.strip())

        # Wait for proxy to be ready by polling the port
        max_attempts = 20
        for attempt in range(max_attempts):
            try:
                with socket.create_connection(('localhost', proxy_port), timeout=1):
                    break
            except (socket.timeout, socket.error):
                if attempt == max_attempts - 1:
                    raise RuntimeError(f"Proxy did not start listening on port {proxy_port} within {max_attempts * 0.5}s")
                time.sleep(0.5)

        yield pid

        # Teardown: stop the proxy process
        try:
            os.kill(pid, signal.SIGTERM)
        except ProcessLookupError:
            pass

    def test_log_list_shows_mock_failures(self, hostname, proxy_url, runner: CliRunner, proxy_pid):
        """Test that 499 mock failures are logged and visible via request log list."""
        res = requests.get(
            f'https://{hostname}/test-unrecorded',
            proxies={'http': proxy_url, 'https': proxy_url},
            verify=False
        )

        assert res.status_code == NOT_FOUND

        time.sleep(0.5)

        result = runner.invoke(request, ['log', 'list'])
        assert result.exit_code == 0

        output = result.output
        assert output, "Log output should not be empty"

        entry = find_log_entry(output, 'Mock failure')
        assert entry is not None, f"Expected to find 'Mock failure' log entry in output:\n{output}"

        assert entry['level'] == 'ERROR'
        assert entry['method'] == 'GET'
        assert hostname in entry.get('url', '')
        assert entry['status_code'] == NOT_FOUND

        assert entry.get('timestamp'), "timestamp should exist and not be empty"
        assert entry.get('user_agent'), "user_agent should exist and not be empty"
        assert entry.get('latency_ms') is not None, "latency_ms should exist"

    def test_log_delete_clears_log_entries(self, hostname, proxy_url, runner: CliRunner, proxy_pid):
        """Test that request log delete clears all log entries."""
        requests.get(
            f'https://{hostname}/another-unrecorded',
            proxies={'http': proxy_url, 'https': proxy_url},
            verify=False
        )
        time.sleep(0.5)

        result = runner.invoke(request, ['log', 'list'])
        assert result.exit_code == 0
        assert result.output.strip(), "Log should have entries before delete"

        delete_result = runner.invoke(request, ['log', 'delete'])
        assert delete_result.exit_code == 0

        list_result = runner.invoke(request, ['log', 'list'])
        assert list_result.exit_code == 0
        assert not list_result.output.strip(), f"Log should be empty after delete, got: {list_result.output}"

    def test_log_path_shows_correct_path(self, runner: CliRunner, proxy_pid):
        """Test that request log path outputs the correct simple log path."""
        result = runner.invoke(request, ['log', 'path'])
        assert result.exit_code == 0
        assert 'tmp/logs/requests.json' in result.output
