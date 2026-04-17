import json
import pytest
import requests
import socket
import time

from click.testing import CliRunner
from typing import Optional

from stoobly_agent.app.cli.scaffold_cli import scaffold
from stoobly_agent.app.cli.scaffold.constants import (
    PROXY_MODE_FORWARD,
    WORKFLOW_MOCK_TYPE,
    WORKFLOW_RECORD_TYPE,
)
from stoobly_agent.app.proxy.constants.custom_response_codes import NOT_FOUND
from stoobly_agent.app.settings import Settings
from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.test.app.cli.scaffold.docker.cli_invoker import ScaffoldCliInvoker
from stoobly_agent.test.test_helper import reset


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


def wait_for_port(host: str, port: int, timeout: float = 120.0, interval: float = 1.0) -> bool:
    """Block until TCP port accepts connections or timeout expires. Returns True if ready."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with socket.create_connection((host, port), timeout=2.0):
                return True
        except (socket.error, OSError):
            time.sleep(interval)
    return False


def wait_for_forward_proxy_intercept(proxy_url: str, hostname: str, timeout: float = 30.0, interval: float = 1.0) -> bool:
    """Poll until the forward proxy is intercepting (returns 499 for unrecorded requests).

    The stoobly proxy starts before its settings file is written, so there is a brief
    window where requests are forwarded instead of intercepted.  This function waits
    until the proxy is in mock-intercept mode before the test proceeds.
    """
    from stoobly_agent.app.proxy.constants.custom_response_codes import NOT_FOUND
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            resp = requests.get(
                f'http://{hostname}/',
                proxies={'http': proxy_url, 'https': proxy_url},
                verify=False,
                timeout=5.0,
            )
            if resp.status_code == NOT_FOUND:
                return True
        except Exception:
            pass
        time.sleep(interval)
    return False


def wait_for_reverse_proxy_ready(hostname: str, timeout: float = 60.0, interval: float = 1.0) -> bool:
    """Poll until the stoobly proxy behind Traefik is handling requests (non-502/503 response).

    Traefik becomes ready before the per-service stoobly proxy is fully initialised.
    This function waits until actual requests reach the stoobly proxy.
    """
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            resp = requests.get(
                f'http://localhost:80/',
                headers={'Host': hostname},
                timeout=5.0,
            )
            if resp.status_code not in (502, 503):
                return True
        except Exception:
            pass
        time.sleep(interval)
    return False


def wait_for_record_active(proxy_url: str, hostname: str, runner, workflow_name: str, context_dir_path: str, settings, timeout: float = 120.0, interval: float = 1.0, recommit_interval: float = 10.0) -> bool:
    """Poll until the forward proxy is actively recording.

    Clears stale log entries first, then commits settings and polls until a 'Record
    success' or 'Record failure' entry appears. Either confirms the proxy reloaded
    settings and entered record mode — 'Record failure' occurs when the upstream is
    unreachable (e.g. in CI) but the proxy is still intercepting.

    Periodically recommits settings to handle the race where PollingObserver starts
    after the initial settings.commit().
    """
    runner.invoke(scaffold, [
        'request', 'logs', 'delete', workflow_name,
        '--context-dir-path', context_dir_path
    ])
    settings.commit()
    last_commit = time.time()

    deadline = time.time() + timeout
    while time.time() < deadline:
        if time.time() - last_commit >= recommit_interval:
            settings.commit()
            last_commit = time.time()
        try:
            requests.get(
                f'http://{hostname}/',
                proxies={'http': proxy_url, 'https': proxy_url},
                verify=False,
                timeout=5.0,
            )
        except Exception:
            pass
        time.sleep(interval)
        result = runner.invoke(scaffold, [
            'request', 'logs', 'list', workflow_name,
            '--context-dir-path', context_dir_path
        ])
        if result.exit_code == 0 and result.output.strip():
            if find_log_entry(result.output, 'Record success') or find_log_entry(result.output, 'Record failure'):
                return True
    return False


def wait_for_reverse_proxy_record_active(hostname: str, runner, workflow_name: str, context_dir_path: str, settings, timeout: float = 120.0, interval: float = 1.0, recommit_interval: float = 10.0) -> bool:
    """Poll until the reverse proxy is actively recording.

    Clears stale log entries first, then commits settings and polls until a 'Record
    success' or 'Record failure' entry appears. Either confirms the proxy reloaded
    settings and entered record mode — 'Record failure' occurs when the upstream is
    unreachable (e.g. in CI) but the proxy is still intercepting.

    Periodically recommits settings to handle the race where PollingObserver starts
    after the initial settings.commit().
    """
    runner.invoke(scaffold, [
        'request', 'logs', 'delete', workflow_name,
        '--context-dir-path', context_dir_path
    ])
    settings.commit()
    last_commit = time.time()

    deadline = time.time() + timeout
    while time.time() < deadline:
        if time.time() - last_commit >= recommit_interval:
            settings.commit()
            last_commit = time.time()
        try:
            requests.get(
                'http://localhost:80/',
                headers={'Host': hostname},
                timeout=5.0,
            )
        except Exception:
            pass
        time.sleep(interval)
        result = runner.invoke(scaffold, [
            'request', 'logs', 'list', workflow_name,
            '--context-dir-path', context_dir_path
        ])
        if result.exit_code == 0 and result.output.strip():
            if find_log_entry(result.output, 'Record success') or find_log_entry(result.output, 'Record failure'):
                return True
    return False


def poll_for_log_entry(runner, workflow_name, context_dir_path, message, max_retries=20, interval=1.0):
    """Poll scaffold request logs list until a matching entry appears."""
    for _ in range(max_retries):
        time.sleep(interval)
        result = runner.invoke(scaffold, [
            'request', 'logs', 'list', workflow_name,
            '--context-dir-path', context_dir_path
        ])
        if result.exit_code == 0 and result.output.strip():
            entry = find_log_entry(result.output, message)
            if entry is not None:
                return entry
    return None


@pytest.mark.e2e
class TestDockerRequestLogE2e():

    @pytest.fixture(scope='module', autouse=True)
    def settings(self):
        return reset()

    @pytest.fixture(scope='module')
    def runner(self):
        yield CliRunner()

    @pytest.fixture(scope='class', autouse=True)
    def temp_dir(self):
        data_dir_path = DataDir.instance().path
        tmp_path = data_dir_path[:data_dir_path.rfind('/')]
        yield tmp_path

    @pytest.fixture(scope='class', autouse=True)
    def app_dir_path(self, temp_dir):
        yield temp_dir

    @pytest.fixture(scope='class')
    def hostname(self):
        yield "http.badssl.com"

    class TestForwardProxyMockRequestLog():

        @pytest.fixture(scope='class')
        def app_name(self):
            yield "docker-request-log-forward"

        @pytest.fixture(scope='class')
        def service_name(self):
            yield "external-service"

        @pytest.fixture(scope='class', autouse=True)
        def target_workflow_name(self):
            yield WORKFLOW_MOCK_TYPE

        @pytest.fixture(scope='class')
        def proxy_url(self):
            yield "http://localhost:8080"

        @pytest.fixture(scope='class', autouse=True)
        def create_scaffold_setup(self, runner, app_dir_path, app_name, hostname, service_name):
            ScaffoldCliInvoker.cli_app_create(runner, app_dir_path, app_name, proxy_mode=PROXY_MODE_FORWARD)
            ScaffoldCliInvoker.cli_service_create(runner, app_dir_path, hostname, service_name, False)

        @pytest.fixture(scope='class', autouse=True)
        def setup_workflow_up(self, create_scaffold_setup, runner, app_dir_path, target_workflow_name, proxy_url, hostname):
            ScaffoldCliInvoker.cli_workflow_up(runner, app_dir_path, target_workflow_name)
            assert wait_for_forward_proxy_intercept(proxy_url, hostname), "Forward proxy did not enter mock-intercept mode"

        @pytest.fixture(scope='class', autouse=True)
        def cleanup_after_all(self, setup_workflow_up, runner, app_dir_path, target_workflow_name):
            yield
            ScaffoldCliInvoker.cli_workflow_down(runner, app_dir_path, target_workflow_name)

        def test_mock_failure_logged(self, runner, app_dir_path, hostname, target_workflow_name, proxy_url):
            """Make an unrecorded request through the forward proxy and verify a Mock failure log entry appears."""
            requests.get(
                f'http://{hostname}/',
                proxies={'http': proxy_url, 'https': proxy_url},
                verify=False
            )

            entry = poll_for_log_entry(runner, target_workflow_name, app_dir_path, 'Mock failure')
            assert entry is not None, "Expected 'Mock failure' log entry but none appeared"
            assert entry['level'] == 'ERROR'
            assert entry['method'] == 'GET'
            assert hostname in entry.get('url', '')
            assert entry['status_code'] == NOT_FOUND
            assert entry.get('timestamp'), "timestamp should exist and not be empty"
            assert entry.get('latency_ms') is not None, "latency_ms should exist"

        def test_log_delete_clears_entries(self, runner, app_dir_path, hostname, target_workflow_name, proxy_url):
            """Verify that deleting logs clears all entries."""
            requests.get(
                f'http://{hostname}/another-unrecorded',
                proxies={'http': proxy_url, 'https': proxy_url},
                verify=False
            )

            entry = poll_for_log_entry(runner, target_workflow_name, app_dir_path, 'Mock failure')
            assert entry is not None, "Expected log entries before delete"

            delete_result = runner.invoke(scaffold, [
                'request', 'logs', 'delete', target_workflow_name,
                '--context-dir-path', app_dir_path
            ])
            assert delete_result.exit_code == 0

            list_result = runner.invoke(scaffold, [
                'request', 'logs', 'list', target_workflow_name,
                '--context-dir-path', app_dir_path
            ])
            assert list_result.exit_code == 0
            assert not list_result.output.strip(), f"Log should be empty after delete, got: {list_result.output}"

    class TestReverseProxyMockRequestLog():

        @pytest.fixture(scope='class')
        def app_name(self):
            yield "docker-request-log-reverse"

        @pytest.fixture(scope='class')
        def service_name(self):
            yield "external-service"

        @pytest.fixture(scope='class', autouse=True)
        def target_workflow_name(self):
            yield WORKFLOW_MOCK_TYPE

        @pytest.fixture(scope='class', autouse=True)
        def create_scaffold_setup(self, runner, app_dir_path, app_name, hostname, service_name):
            ScaffoldCliInvoker.cli_app_create(runner, app_dir_path, app_name)
            ScaffoldCliInvoker.cli_service_create(runner, app_dir_path, hostname, service_name, False)

        @pytest.fixture(scope='class', autouse=True)
        def setup_workflow_up(self, create_scaffold_setup, runner, app_dir_path, target_workflow_name):
            ScaffoldCliInvoker.cli_workflow_up(runner, app_dir_path, target_workflow_name)
            assert wait_for_port('localhost', 80), "Reverse proxy did not become ready on port 80"
            time.sleep(3)  # Allow per-service stoobly proxy to fully initialise behind Traefik

        @pytest.fixture(scope='class', autouse=True)
        def cleanup_after_all(self, setup_workflow_up, runner, app_dir_path, target_workflow_name):
            yield
            ScaffoldCliInvoker.cli_workflow_down(runner, app_dir_path, target_workflow_name)

        def test_mock_failure_logged(self, runner, app_dir_path, hostname, target_workflow_name):
            """Make an unrecorded request via Host header and verify a Mock failure log entry appears."""
            requests.get(
                'http://localhost:80/',
                headers={'Host': hostname},
            )

            entry = poll_for_log_entry(runner, target_workflow_name, app_dir_path, 'Mock failure')
            assert entry is not None, "Expected 'Mock failure' log entry but none appeared"

            assert entry['level'] == 'ERROR'
            assert entry['method'] == 'GET'
            assert hostname in entry.get('url', '')
            assert entry['status_code'] == NOT_FOUND
            assert entry.get('timestamp'), "timestamp should exist and not be empty"
            assert entry.get('latency_ms') is not None, "latency_ms should exist"

        def test_log_delete_clears_entries(self, runner, app_dir_path, hostname, target_workflow_name):
            """Verify that deleting logs clears all entries."""
            requests.get(
                'http://localhost:80/another-unrecorded',
                headers={'Host': hostname},
            )

            entry = poll_for_log_entry(runner, target_workflow_name, app_dir_path, 'Mock failure')
            assert entry is not None, "Expected log entries before delete"

            delete_result = runner.invoke(scaffold, [
                'request', 'logs', 'delete', target_workflow_name,
                '--context-dir-path', app_dir_path
            ])
            assert delete_result.exit_code == 0

            list_result = runner.invoke(scaffold, [
                'request', 'logs', 'list', target_workflow_name,
                '--context-dir-path', app_dir_path
            ])
            assert list_result.exit_code == 0
            assert not list_result.output.strip(), f"Log should be empty after delete, got: {list_result.output}"


@pytest.mark.e2e
class TestDockerRecordRequestLogE2e():

    @pytest.fixture(scope='module', autouse=True)
    def settings(self):
        return reset('stoobly-agent-test-record')

    @pytest.fixture(scope='module')
    def runner(self):
        yield CliRunner()

    @pytest.fixture(scope='class', autouse=True)
    def temp_dir(self):
        data_dir_path = DataDir.instance().path
        tmp_path = data_dir_path[:data_dir_path.rfind('/')]
        yield tmp_path

    @pytest.fixture(scope='class', autouse=True)
    def app_dir_path(self, temp_dir):
        yield temp_dir

    @pytest.fixture(scope='class')
    def hostname(self):
        yield "http.badssl.com"

    class TestForwardProxyRecordRequestLog():

        @pytest.fixture(scope='class')
        def app_name(self):
            yield "docker-request-log-forward-record"

        @pytest.fixture(scope='class')
        def service_name(self):
            yield "external-service-record"

        @pytest.fixture(scope='class', autouse=True)
        def target_workflow_name(self):
            yield WORKFLOW_RECORD_TYPE

        @pytest.fixture(scope='class')
        def proxy_url(self):
            yield "http://localhost:8080"

        @pytest.fixture(scope='class', autouse=True)
        def create_scaffold_setup(self, runner, app_dir_path, app_name, hostname, service_name):
            ScaffoldCliInvoker.cli_app_create(runner, app_dir_path, app_name, proxy_mode=PROXY_MODE_FORWARD)
            ScaffoldCliInvoker.cli_service_create(runner, app_dir_path, hostname, service_name, False)

        @pytest.fixture(scope='class', autouse=True)
        def setup_workflow_up(self, create_scaffold_setup, runner, app_dir_path, target_workflow_name, proxy_url, hostname, settings):
            ScaffoldCliInvoker.cli_workflow_up(runner, app_dir_path, target_workflow_name)
            assert wait_for_port('localhost', 8080), "Forward proxy did not become ready on port 8080"
            settings.load()
            settings.proxy.intercept.active = True
            assert wait_for_record_active(proxy_url, hostname, runner, target_workflow_name, app_dir_path, settings), \
                "Forward proxy did not enter record-active mode"

        @pytest.fixture(scope='class', autouse=True)
        def cleanup_after_all(self, setup_workflow_up, runner, app_dir_path, target_workflow_name):
            yield
            ScaffoldCliInvoker.cli_workflow_down(runner, app_dir_path, target_workflow_name)

        def test_record_success_logged(self, runner, app_dir_path, hostname, target_workflow_name, proxy_url):
            """Make a request through the forward proxy record workflow and verify a Record success log entry appears."""
            res = requests.get(
                f'http://{hostname}/',
                proxies={'http': proxy_url, 'https': proxy_url},
                verify=False
            )

            entry = poll_for_log_entry(runner, target_workflow_name, app_dir_path, 'Record success')

            assert entry is not None, "Expected 'Record success' log entry but none appeared"
            assert entry['level'] == 'INFO'
            assert entry['method'] == 'GET'
            assert hostname in entry.get('url', '')
            assert entry.get('timestamp'), "timestamp should exist and not be empty"
            assert entry.get('latency_ms') is not None, "latency_ms should exist"

        def test_log_delete_clears_entries(self, runner, app_dir_path, hostname, target_workflow_name, proxy_url):
            """Verify that deleting logs clears all entries."""
            requests.get(
                f'http://{hostname}/',
                proxies={'http': proxy_url, 'https': proxy_url},
                verify=False
            )

            entry = poll_for_log_entry(runner, target_workflow_name, app_dir_path, 'Record success')
            assert entry is not None, "Expected log entries before delete"

            delete_result = runner.invoke(scaffold, [
                'request', 'logs', 'delete', target_workflow_name,
                '--context-dir-path', app_dir_path
            ])
            assert delete_result.exit_code == 0

            list_result = runner.invoke(scaffold, [
                'request', 'logs', 'list', target_workflow_name,
                '--context-dir-path', app_dir_path
            ])
            assert list_result.exit_code == 0
            assert not list_result.output.strip(), f"Log should be empty after delete, got: {list_result.output}"

    class TestReverseProxyRecordRequestLog():

        @pytest.fixture(scope='class')
        def app_name(self):
            yield "docker-request-log-record"

        @pytest.fixture(scope='class')
        def service_name(self):
            yield "external-service"

        @pytest.fixture(scope='class', autouse=True)
        def target_workflow_name(self):
            yield WORKFLOW_RECORD_TYPE

        @pytest.fixture(scope='class', autouse=True)
        def create_scaffold_setup(self, runner, app_dir_path, app_name, hostname, service_name):
            ScaffoldCliInvoker.cli_app_create(runner, app_dir_path, app_name)
            ScaffoldCliInvoker.cli_service_create(runner, app_dir_path, hostname, service_name, False)

        @pytest.fixture(scope='class', autouse=True)
        def setup_workflow_up(self, create_scaffold_setup, runner, app_dir_path, target_workflow_name, hostname, settings):
            ScaffoldCliInvoker.cli_workflow_up(runner, app_dir_path, target_workflow_name)
            assert wait_for_port('localhost', 80), "Reverse proxy did not become ready on port 80"
            assert wait_for_reverse_proxy_ready(hostname), "stoobly proxy behind Traefik did not become ready"
            settings.load()
            settings.proxy.intercept.active = True
            assert wait_for_reverse_proxy_record_active(hostname, runner, target_workflow_name, app_dir_path, settings), \
                "Reverse proxy did not enter record-active mode"

        @pytest.fixture(scope='class', autouse=True)
        def cleanup_after_all(self, setup_workflow_up, runner, app_dir_path, target_workflow_name):
            yield
            ScaffoldCliInvoker.cli_workflow_down(runner, app_dir_path, target_workflow_name)

        def test_record_success_logged(self, runner, app_dir_path, hostname, target_workflow_name):
            """Make a request through the reverse proxy record workflow and verify a Record success log entry appears."""
            res = requests.get(
                'http://localhost:80/',
                headers={'Host': hostname},
            )

            entry = poll_for_log_entry(runner, target_workflow_name, app_dir_path, 'Record success')
            assert entry is not None, "Expected 'Record success' log entry but none appeared"

            assert entry['level'] == 'INFO'
            assert entry['method'] == 'GET'
            assert hostname in entry.get('url', '')
            assert entry.get('timestamp'), "timestamp should exist and not be empty"
            assert entry.get('latency_ms') is not None, "latency_ms should exist"

        def test_log_delete_clears_entries(self, runner, app_dir_path, hostname, target_workflow_name):
            """Verify that deleting logs clears all entries."""
            requests.get(
                'http://localhost:80/another-path',
                headers={'Host': hostname},
            )

            entry = poll_for_log_entry(runner, target_workflow_name, app_dir_path, 'Record success')
            assert entry is not None, "Expected log entries before delete"

            delete_result = runner.invoke(scaffold, [
                'request', 'logs', 'delete', target_workflow_name,
                '--context-dir-path', app_dir_path
            ])
            assert delete_result.exit_code == 0

            list_result = runner.invoke(scaffold, [
                'request', 'logs', 'list', target_workflow_name,
                '--context-dir-path', app_dir_path
            ])
            assert list_result.exit_code == 0
            assert not list_result.output.strip(), f"Log should be empty after delete, got: {list_result.output}"
