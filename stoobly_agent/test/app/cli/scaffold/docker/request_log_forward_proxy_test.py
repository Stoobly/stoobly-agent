import json
import pytest
import requests
import subprocess
import time

from click.testing import CliRunner
from typing import Optional

from stoobly_agent.test.test_helper import reset  # must be first: calls reset() at module level to initialise settings before other CLI modules import
from stoobly_agent.app.cli.scaffold_cli import scaffold
from stoobly_agent.app.cli.scaffold.constants import (
    PROXY_MODE_FORWARD,
    WORKFLOW_MOCK_TYPE,
    WORKFLOW_RECORD_TYPE,
)
from stoobly_agent.app.proxy.constants.custom_response_codes import NOT_FOUND
from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.test.app.cli.scaffold.docker.cli_invoker import ScaffoldCliInvoker, _append_error_to_tmp_log, _dump_docker_state


def find_log_entry(output: str, message: str, method: str = None) -> Optional[dict]:
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


def wait_for_forward_proxy_intercept(proxy_url: str, hostname: str, timeout: float = 30.0, interval: float = 0.5) -> bool:
    """Poll until the forward proxy is intercepting (returns 499 for unrecorded requests)."""
    deadline = time.time() + timeout
    last_status = None
    last_exc = None
    while time.time() < deadline:
        try:
            resp = requests.get(
                f'http://{hostname}/',
                proxies={'http': proxy_url, 'https': proxy_url},
                verify=False,
                timeout=5.0,
            )
            last_status = resp.status_code
            if resp.status_code == NOT_FOUND:
                return True
        except Exception as e:
            last_exc = e
        time.sleep(interval)
    _append_error_to_tmp_log([
        f"wait_for_forward_proxy_intercept timed out after {timeout}s",
        f"Last HTTP status: {last_status}",
        f"Last exception: {last_exc}",
    ])
    return False


def wait_for_forward_proxy_ready(proxy_url: str, hostname: str, timeout: float = 30.0, interval: float = 0.5) -> bool:
    """Poll until the forward proxy is accepting and processing HTTP requests."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            requests.get(
                f'http://{hostname}/',
                proxies={'http': proxy_url, 'https': proxy_url},
                verify=False,
                timeout=5.0,
            )
            return True
        except requests.exceptions.ProxyError:
            pass  # mitmproxy not ready yet (ProxyError is a subclass of ConnectionError; must come first)
        except requests.exceptions.ConnectionError:
            return True  # proxy forwarded the request; upstream connection failed
        except Exception:
            pass  # timeout or other transient error — keep polling
        time.sleep(interval)
    return False


def _enable_intercept_in_container(container_name: str) -> bool:
    """Run 'stoobly-agent intercept enable' inside the named Docker container."""
    result = subprocess.run(
        ['docker', 'exec', '--user', 'stoobly', container_name, 'stoobly-agent', 'intercept', 'enable'],
        capture_output=True,
        timeout=30,
    )
    return result.returncode == 0


def wait_for_record_active(proxy_url: str, hostname: str, runner, workflow_name: str, context_dir_path: str, timeout: float = 120.0, interval: float = 0.5, reenable_interval: float = 10.0) -> bool:
    """Poll until the forward proxy is actively recording."""
    container_name = f'{workflow_name}-gateway.service-1'
    runner.invoke(scaffold, [
        'request', 'logs', 'delete', workflow_name,
        '--context-dir-path', context_dir_path
    ])
    _enable_intercept_in_container(container_name)
    last_enable = time.time()

    deadline = time.time() + timeout
    while time.time() < deadline:
        if time.time() - last_enable >= reenable_interval:
            _enable_intercept_in_container(container_name)
            last_enable = time.time()
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


def poll_for_log_entry(runner, workflow_name, context_dir_path, message, max_retries=20, interval=0.25):
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
            success = wait_for_forward_proxy_intercept(proxy_url, hostname)
            if not success:
                _dump_docker_state()
            assert success, "Forward proxy did not enter mock-intercept mode"

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

    @pytest.mark.xfail(reason="wait_for_record_active is flaky in CI (host-to-container inotify unreliable on GitHub Actions runners)", strict=False)
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
        def setup_workflow_up(self, create_scaffold_setup, runner, app_dir_path, target_workflow_name, proxy_url, hostname):
            ScaffoldCliInvoker.cli_workflow_up(runner, app_dir_path, target_workflow_name)
            assert wait_for_forward_proxy_ready(proxy_url, hostname), "Forward proxy did not become ready"
            assert wait_for_record_active(proxy_url, hostname, runner, target_workflow_name, app_dir_path), "Forward proxy did not enter record mode"

        @pytest.fixture(scope='class', autouse=True)
        def cleanup_after_all(self, setup_workflow_up, runner, app_dir_path, target_workflow_name):
            yield
            ScaffoldCliInvoker.cli_workflow_down(runner, app_dir_path, target_workflow_name)

        def test_record_success_logged(self, runner, app_dir_path, hostname, target_workflow_name, proxy_url):
            """Make a request through the forward proxy record workflow and verify a Record success log entry appears."""
            runner.invoke(scaffold, ['request', 'logs', 'delete', target_workflow_name, '--context-dir-path', app_dir_path])

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
