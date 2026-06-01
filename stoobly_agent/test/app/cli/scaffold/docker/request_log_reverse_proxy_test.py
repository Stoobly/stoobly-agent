import json
import pytest
import requests
import socket
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from click.testing import CliRunner
from typing import Optional

from stoobly_agent.test.test_helper import reset  # must be first: calls reset() at module level to initialise settings before other CLI modules import
from stoobly_agent.app.cli.scaffold_cli import scaffold
from stoobly_agent.app.cli.scaffold.constants import (
    WORKFLOW_MOCK_TYPE,
    WORKFLOW_RECORD_TYPE,
)
from stoobly_agent.app.proxy.constants.custom_response_codes import NOT_FOUND
from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.test.app.cli.scaffold.docker.cli_invoker import ScaffoldCliInvoker, _append_error_to_tmp_log, _dump_docker_state
from stoobly_agent.test.app.cli.scaffold.log_test_helpers import count_log_entries, find_all_log_entries


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


def wait_for_port(host: str, port: int, timeout: float = 60.0, interval: float = 1.0) -> bool:
    """Block until TCP port accepts connections or timeout expires."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with socket.create_connection((host, port), timeout=2.0):
                return True
        except (socket.error, OSError):
            time.sleep(interval)
    return False


def wait_for_reverse_proxy_ready(hostname: str, timeout: float = 60.0, interval: float = 0.5) -> bool:
    """Poll until the stoobly proxy behind Traefik is handling requests (non-502/503 response)."""
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


def wait_for_reverse_proxy_intercept(hostname: str, timeout: float = 30.0, interval: float = 0.5) -> bool:
    """Poll until the reverse proxy is intercepting in mock mode (returns 499 for unrecorded requests)."""
    deadline = time.time() + timeout
    last_status = None
    last_exc = None
    while time.time() < deadline:
        try:
            resp = requests.get(
                'http://localhost:80/',
                headers={'Host': hostname},
                timeout=5.0,
            )
            last_status = resp.status_code
            if resp.status_code == NOT_FOUND:
                return True
        except Exception as e:
            last_exc = e
        time.sleep(interval)
    _append_error_to_tmp_log([
        f"wait_for_reverse_proxy_intercept timed out after {timeout}s",
        f"Last HTTP status: {last_status}",
        f"Last exception: {last_exc}",
    ])
    return False


def _enable_intercept_in_container(container_name: str) -> bool:
    """Run 'stoobly-agent intercept enable' inside the named Docker container."""
    result = subprocess.run(
        ['docker', 'exec', '--user', 'stoobly', container_name, 'stoobly-agent', 'intercept', 'enable'],
        capture_output=True,
        timeout=30,
    )
    return result.returncode == 0


def wait_for_reverse_proxy_record_active(hostname: str, runner, workflow_name: str, context_dir_path: str, service_name: str, timeout: float = 120.0, interval: float = 0.5, reenable_interval: float = 10.0) -> bool:
    """Poll until the reverse proxy is actively recording."""
    container_name = f'{workflow_name}-{service_name}.proxy-1'
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


def poll_until_log_count_stable(
    runner,
    workflow_name: str,
    context_dir_path: str,
    target_count: int,
    max_retries: int = 30,
    interval: float = 0.25,
) -> str:
    """Poll until log count reaches target_count. Exits early on success."""
    consecutive_errors = 0
    for _ in range(max_retries):
        time.sleep(interval)
        result = runner.invoke(scaffold, [
            'request', 'logs', 'list', workflow_name,
            '--context-dir-path', context_dir_path,
        ])
        if result.exit_code != 0:
            consecutive_errors += 1
            if consecutive_errors >= 5:
                raise RuntimeError(
                    f"'scaffold request logs list' failed {consecutive_errors} times in a row; "
                    f"last output: {result.output!r}"
                )
            continue
        consecutive_errors = 0
        if count_log_entries(result.output) >= target_count:
            return result.output
    return ''


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

    class TestReverseProxyMockRequestLog():
        """Reverse proxy mock mode — basic request/delete behaviour and high-traffic load share one scaffold."""

        _REQUEST_COUNT = 200

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
        def setup_workflow_up(self, create_scaffold_setup, runner, app_dir_path, target_workflow_name, hostname):
            ScaffoldCliInvoker.cli_workflow_up(runner, app_dir_path, target_workflow_name)
            success = wait_for_reverse_proxy_intercept(hostname)
            if not success:
                _dump_docker_state()
            assert success, "Reverse proxy did not enter mock-intercept mode"

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

        def test_high_traffic_no_dropped_entries(self, runner, app_dir_path, hostname, target_workflow_name):
            """Verify the async logger captures all entries under concurrent load — no dropped writes."""
            delete_result = runner.invoke(scaffold, [
                'request', 'logs', 'delete', target_workflow_name,
                '--context-dir-path', app_dir_path,
            ])
            assert delete_result.exit_code == 0, f"Failed to delete logs before test: {delete_result.output}"

            paths = [f'/high-traffic-{i}' for i in range(self._REQUEST_COUNT)]

            def _get(path):
                try:
                    return requests.get(
                        f'http://localhost:80{path}',
                        headers={'Host': hostname},
                        timeout=10.0,
                    ).status_code
                except Exception:
                    return -1

            with ThreadPoolExecutor(max_workers=self._REQUEST_COUNT) as pool:
                futures = [pool.submit(_get, p) for p in paths]
                status_codes = [f.result() for f in as_completed(futures)]

            transport_failures = sum(1 for s in status_codes if s == -1)
            assert transport_failures == 0, (
                f"{transport_failures}/{self._REQUEST_COUNT} requests failed to reach the proxy "
                f"(transport/connection error) — any log shortfall is not a logger bug"
            )

            output = poll_until_log_count_stable(
                runner, target_workflow_name, app_dir_path,
                target_count=self._REQUEST_COUNT,
            )
            assert output, f"Log count did not reach {self._REQUEST_COUNT} within timeout — entries may have been dropped"

            total = count_log_entries(output)
            assert total == self._REQUEST_COUNT, \
                f"Expected {self._REQUEST_COUNT} log entries, got {total} — logger dropped writes under load"

            entries = find_all_log_entries(output)
            assert all(e['level'] == 'ERROR' for e in entries), "All entries should be ERROR (unrecorded → 499)"
            assert all(e['status_code'] == NOT_FOUND for e in entries), "All entries should have status_code 499"


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
        def setup_workflow_up(self, create_scaffold_setup, runner, app_dir_path, target_workflow_name, hostname, service_name):
            ScaffoldCliInvoker.cli_workflow_up(runner, app_dir_path, target_workflow_name)
            assert wait_for_port('localhost', 80), "Reverse proxy did not become ready on port 80"
            assert wait_for_reverse_proxy_ready(hostname), "stoobly proxy behind Traefik did not become ready"
            success = wait_for_reverse_proxy_record_active(hostname, runner, target_workflow_name, app_dir_path, service_name)
            if not success:
                _dump_docker_state()
            assert success, "Reverse proxy did not enter record mode"

        @pytest.fixture(scope='class', autouse=True)
        def cleanup_after_all(self, setup_workflow_up, runner, app_dir_path, target_workflow_name):
            yield
            ScaffoldCliInvoker.cli_workflow_down(runner, app_dir_path, target_workflow_name)

        def test_record_success_logged(self, runner, app_dir_path, hostname, target_workflow_name):
            """Make a request through the reverse proxy record workflow and verify a Record success log entry appears."""
            runner.invoke(scaffold, ['request', 'logs', 'delete', target_workflow_name, '--context-dir-path', app_dir_path])

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
