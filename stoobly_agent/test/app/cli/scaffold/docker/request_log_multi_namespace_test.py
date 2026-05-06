import os
import pytest
import requests
import shutil
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List
from urllib.parse import urlparse

from click.testing import CliRunner

from stoobly_agent.test.test_helper import reset  # must be first: initialises settings before other CLI modules import
from stoobly_agent.app.cli.scaffold_cli import scaffold
from stoobly_agent.app.cli.scaffold.constants import WORKFLOW_MOCK_TYPE
from stoobly_agent.app.proxy.constants.custom_response_codes import NOT_FOUND
from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.test.app.cli.scaffold.docker.cli_invoker import ScaffoldCliInvoker
from stoobly_agent.test.app.cli.scaffold.log_test_helpers import find_all_log_entries


def _url_has_hostname(url: str, hostname: str) -> bool:
    try:
        return urlparse(url).hostname == hostname
    except Exception:
        return False


def assert_no_entries_for_hostname(output: str, hostname: str) -> None:
    """Raise AssertionError with the offending entry if any parsed log entry's url contains hostname."""
    for entry in find_all_log_entries(output):
        if _url_has_hostname(entry.get('url', ''), hostname):
            raise AssertionError(
                f"Found unexpected log entry for {hostname!r}: {entry}"
            )


def read_log_file_raw(app_dir_path: str, workflow: str, namespace: str) -> str:
    """Read the raw log file content directly; returns '' if the file does not exist."""
    log_path = os.path.join(
        app_dir_path, '.stoobly', 'tmp', namespace, 'logs',
        f'{workflow}.requests.json'
    )
    if not os.path.exists(log_path):
        return ''
    with open(log_path) as f:
        return f.read()


def wait_for_reverse_proxy_intercept_on_port(
    hostname: str, port: int, timeout: float = 60.0, interval: float = 1.0
) -> bool:
    """Poll until localhost:{port} returns 499 for Host: {hostname}, confirming mock-intercept mode."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            resp = requests.get(
                f'http://localhost:{port}/',
                headers={'Host': hostname},
                timeout=5.0,
            )
            if resp.status_code == NOT_FOUND:
                return True
        except Exception:
            pass
        time.sleep(interval)
    return False


def poll_for_any_log_entry(
    runner,
    workflow_name: str,
    context_dir_path: str,
    namespace: str,
    max_retries: int = 30,
    interval: float = 1.0,
) -> str:
    """Poll scaffold request logs list until ≥1 entry appears. Returns full output or '' on timeout."""
    for _ in range(max_retries):
        time.sleep(interval)
        result = runner.invoke(scaffold, [
            'request', 'logs', 'list', workflow_name,
            '--context-dir-path', context_dir_path,
            '--namespace', namespace,
        ])
        if result.exit_code == 0 and result.output.strip():
            return result.output
    return ''


def _make_app_dir(base_dir: str, suffix: str) -> str:
    """Create (or recreate) an isolated app directory as a subdirectory of base_dir."""
    path = os.path.join(base_dir, suffix)
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path, exist_ok=True)
    return path


@pytest.mark.e2e
class TestDockerMultiNamespaceRequestLogE2e:
    """Docker reverse-proxy multi-namespace CI isolation tests.

    Each nested class spins up one or two Traefik namespaces on ports 8180/8181.
    Classes run sequentially — no port conflicts as each class tears down before
    the next starts.  Do NOT run with pytest-xdist.
    """

    @pytest.fixture(scope='module', autouse=True)
    def settings(self):
        return reset('stoobly-agent-test-multi-ns')

    @pytest.fixture(scope='module')
    def runner(self):
        yield CliRunner()

    @pytest.fixture(scope='module')
    def base_dir(self):
        """Parent directory of the DataDir .stoobly/ folder; shared by all nested classes."""
        data_dir_path = DataDir.instance().path
        yield data_dir_path[:data_dir_path.rfind('/')]

    # ------------------------------------------------------------------
    # TestNamespaceLogIsolation
    # ------------------------------------------------------------------

    class TestNamespaceLogIsolation:
        """Requests in NS A must never appear in NS B's logs and vice versa."""

        @pytest.fixture(scope='class')
        def app_dir_path_a(self, base_dir):
            yield _make_app_dir(base_dir, 'ns-iso-a')

        @pytest.fixture(scope='class')
        def app_dir_path_b(self, base_dir):
            yield _make_app_dir(base_dir, 'ns-iso-b')

        @pytest.fixture(scope='class', autouse=True)
        def setup_ns_a(self, runner, app_dir_path_a):
            ScaffoldCliInvoker.cli_app_create(runner, app_dir_path_a, 'ns-iso-a', proxy_mode='reverse', ui_port=4200)
            ScaffoldCliInvoker.cli_service_create(runner, app_dir_path_a, 'http.badssl.com', 'service-a', False, port=8180)
            ScaffoldCliInvoker.cli_workflow_up(runner, app_dir_path_a, WORKFLOW_MOCK_TYPE, namespace='ns-iso-a')
            assert wait_for_reverse_proxy_intercept_on_port('http.badssl.com', 8180), \
                "NS A proxy did not enter mock-intercept mode on port 8180"

        @pytest.fixture(scope='class', autouse=True)
        def setup_ns_b(self, runner, app_dir_path_b):
            ScaffoldCliInvoker.cli_app_create(runner, app_dir_path_b, 'ns-iso-b', proxy_mode='reverse', ui_port=4201)
            ScaffoldCliInvoker.cli_service_create(runner, app_dir_path_b, 'example.com', 'service-b', False, port=8181)
            ScaffoldCliInvoker.cli_workflow_up(runner, app_dir_path_b, WORKFLOW_MOCK_TYPE, namespace='ns-iso-b')
            assert wait_for_reverse_proxy_intercept_on_port('example.com', 8181), \
                "NS B proxy did not enter mock-intercept mode on port 8181"

        @pytest.fixture(scope='class', autouse=True)
        def teardown(self, setup_ns_a, setup_ns_b, runner, app_dir_path_a, app_dir_path_b):
            yield
            ScaffoldCliInvoker.cli_workflow_down(runner, app_dir_path_a, WORKFLOW_MOCK_TYPE, namespace='ns-iso-a')
            ScaffoldCliInvoker.cli_workflow_down(runner, app_dir_path_b, WORKFLOW_MOCK_TYPE, namespace='ns-iso-b')

        def test_requests_to_ns_a_do_not_appear_in_ns_b_logs(self, runner, app_dir_path_a, app_dir_path_b):
            requests.get('http://localhost:8180/', headers={'Host': 'http.badssl.com'}, timeout=5.0)

            output_a = poll_for_any_log_entry(runner, WORKFLOW_MOCK_TYPE, app_dir_path_a, 'ns-iso-a')
            assert output_a, "Expected ≥1 log entry in NS A"

            output_b = read_log_file_raw(app_dir_path_b, WORKFLOW_MOCK_TYPE, 'ns-iso-b')
            assert_no_entries_for_hostname(output_b, 'http.badssl.com')

        def test_requests_to_ns_b_do_not_appear_in_ns_a_logs(self, runner, app_dir_path_a, app_dir_path_b):
            requests.get('http://localhost:8181/', headers={'Host': 'example.com'}, timeout=5.0)

            output_b = poll_for_any_log_entry(runner, WORKFLOW_MOCK_TYPE, app_dir_path_b, 'ns-iso-b')
            assert output_b, "Expected ≥1 log entry in NS B"

            output_a = read_log_file_raw(app_dir_path_a, WORKFLOW_MOCK_TYPE, 'ns-iso-a')
            assert_no_entries_for_hostname(output_a, 'example.com')

    # ------------------------------------------------------------------
    # TestAllServicesLoggedWithinNamespace
    # ------------------------------------------------------------------

    class TestAllServicesLoggedWithinNamespace:
        """Both services in a namespace must produce log entries."""

        @pytest.fixture(scope='class')
        def app_dir_path(self, base_dir):
            yield _make_app_dir(base_dir, 'all-svc-a')

        @pytest.fixture(scope='class', autouse=True)
        def setup_ns(self, runner, app_dir_path):
            ScaffoldCliInvoker.cli_app_create(runner, app_dir_path, 'all-svc-a', proxy_mode='reverse')
            ScaffoldCliInvoker.cli_service_create(runner, app_dir_path, 'http.badssl.com', 'service-a', False, port=8180)
            ScaffoldCliInvoker.cli_service_create(runner, app_dir_path, 'example.com', 'service-b', False, port=8180)
            ScaffoldCliInvoker.cli_workflow_up(runner, app_dir_path, WORKFLOW_MOCK_TYPE, namespace='all-svc-a')
            assert wait_for_reverse_proxy_intercept_on_port('http.badssl.com', 8180), \
                "service-a proxy did not enter mock-intercept mode on port 8180"
            assert wait_for_reverse_proxy_intercept_on_port('example.com', 8180), \
                "service-b proxy did not enter mock-intercept mode on port 8180"

        @pytest.fixture(scope='class', autouse=True)
        def teardown(self, setup_ns, runner, app_dir_path):
            yield
            ScaffoldCliInvoker.cli_workflow_down(runner, app_dir_path, WORKFLOW_MOCK_TYPE, namespace='all-svc-a')

        def test_both_services_appear_in_namespace_logs(self, runner, app_dir_path):
            requests.get('http://localhost:8180/', headers={'Host': 'http.badssl.com'}, timeout=5.0)
            requests.get('http://localhost:8180/', headers={'Host': 'example.com'}, timeout=5.0)

            output = poll_for_any_log_entry(runner, WORKFLOW_MOCK_TYPE, app_dir_path, 'all-svc-a')
            assert output, "Expected log entries in namespace all-svc-a"

            entries = find_all_log_entries(output)
            badssl_entries = [e for e in entries if _url_has_hostname(e.get('url', ''), 'http.badssl.com')]
            example_entries = [e for e in entries if _url_has_hostname(e.get('url', ''), 'example.com')]

            assert len(badssl_entries) >= 1, "Expected ≥1 log entry for http.badssl.com"
            assert len(example_entries) >= 1, "Expected ≥1 log entry for example.com"
            assert all(e['level'] == 'ERROR' for e in entries), "All entries should be ERROR (unrecorded → 499)"
            assert all(e['status_code'] == NOT_FOUND for e in entries), "All entries should have status_code 499"

    # ------------------------------------------------------------------
    # TestServiceNameFilterWithinNamespace
    # ------------------------------------------------------------------

    class TestServiceNameFilterWithinNamespace:
        """--service-name filter returns only entries from the target service container."""

        @pytest.fixture(scope='class')
        def app_dir_path(self, base_dir):
            yield _make_app_dir(base_dir, 'svc-filter-a')

        @pytest.fixture(scope='class', autouse=True)
        def setup_ns(self, runner, app_dir_path):
            ScaffoldCliInvoker.cli_app_create(runner, app_dir_path, 'svc-filter-a', proxy_mode='reverse')
            ScaffoldCliInvoker.cli_service_create(runner, app_dir_path, 'http.badssl.com', 'service-alpha', False, port=8180)
            ScaffoldCliInvoker.cli_service_create(runner, app_dir_path, 'example.com', 'service-beta', False, port=8180)
            ScaffoldCliInvoker.cli_workflow_up(runner, app_dir_path, WORKFLOW_MOCK_TYPE, namespace='svc-filter-a')
            assert wait_for_reverse_proxy_intercept_on_port('http.badssl.com', 8180), \
                "service-alpha proxy did not enter mock-intercept mode on port 8180"
            assert wait_for_reverse_proxy_intercept_on_port('example.com', 8180), \
                "service-beta proxy did not enter mock-intercept mode on port 8180"

        @pytest.fixture(scope='class', autouse=True)
        def teardown(self, setup_ns, runner, app_dir_path):
            yield
            ScaffoldCliInvoker.cli_workflow_down(runner, app_dir_path, WORKFLOW_MOCK_TYPE, namespace='svc-filter-a')

        def test_service_name_filter_returns_only_target_service(self, runner, app_dir_path):
            requests.get('http://localhost:8180/', headers={'Host': 'http.badssl.com'}, timeout=5.0)
            requests.get('http://localhost:8180/', headers={'Host': 'example.com'}, timeout=5.0)

            output = poll_for_any_log_entry(runner, WORKFLOW_MOCK_TYPE, app_dir_path, 'svc-filter-a')
            assert output, "Expected log entries before filtering"

            # Read a sample entry to confirm the actual service_name value injected by the scaffold
            all_entries = find_all_log_entries(output)
            badssl_entry = next((e for e in all_entries if _url_has_hostname(e.get('url', ''), 'http.badssl.com')), None)
            assert badssl_entry is not None, "Expected an entry for http.badssl.com to determine service_name"
            alpha_service_name = badssl_entry.get('service_name')
            assert alpha_service_name, "service_name should be set on log entries in Docker reverse proxy mode"

            result = runner.invoke(scaffold, [
                'request', 'logs', 'list', WORKFLOW_MOCK_TYPE,
                '--context-dir-path', app_dir_path,
                '--namespace', 'svc-filter-a',
                '--service-name', alpha_service_name,
            ])
            assert result.exit_code == 0
            assert result.output.strip(), "Expected entries after --service-name filter"

            filtered_entries = find_all_log_entries(result.output)
            assert all(e.get('service_name') == alpha_service_name for e in filtered_entries), \
                f"All filtered entries should have service_name={alpha_service_name!r}"
            assert all(_url_has_hostname(e.get('url', ''), 'http.badssl.com') for e in filtered_entries), \
                "All filtered entries should be for http.badssl.com"
            assert not any(_url_has_hostname(e.get('url', ''), 'example.com') for e in filtered_entries), \
                "Filtered entries should not include example.com (service-beta)"

    # ------------------------------------------------------------------
    # TestConcurrentCrossNamespaceTraffic
    # ------------------------------------------------------------------

    @pytest.mark.xfail(strict=False, reason="concurrent cross-namespace contamination check — gathering CI signal")
    class TestConcurrentCrossNamespaceTraffic:
        """Concurrent traffic to both namespaces must produce no cross-namespace log contamination."""

        @pytest.fixture(scope='class')
        def app_dir_path_a(self, base_dir):
            yield _make_app_dir(base_dir, 'concurrent-a')

        @pytest.fixture(scope='class')
        def app_dir_path_b(self, base_dir):
            yield _make_app_dir(base_dir, 'concurrent-b')

        @pytest.fixture(scope='class', autouse=True)
        def setup_ns_a(self, runner, app_dir_path_a):
            ScaffoldCliInvoker.cli_app_create(runner, app_dir_path_a, 'concurrent-a', proxy_mode='reverse', ui_port=4200)
            ScaffoldCliInvoker.cli_service_create(runner, app_dir_path_a, 'http.badssl.com', 'service-a', False, port=8180)
            ScaffoldCliInvoker.cli_workflow_up(runner, app_dir_path_a, WORKFLOW_MOCK_TYPE, namespace='concurrent-a')
            assert wait_for_reverse_proxy_intercept_on_port('http.badssl.com', 8180), \
                "NS A proxy did not enter mock-intercept mode on port 8180"

        @pytest.fixture(scope='class', autouse=True)
        def setup_ns_b(self, runner, app_dir_path_b):
            ScaffoldCliInvoker.cli_app_create(runner, app_dir_path_b, 'concurrent-b', proxy_mode='reverse', ui_port=4201)
            ScaffoldCliInvoker.cli_service_create(runner, app_dir_path_b, 'example.com', 'service-b', False, port=8181)
            ScaffoldCliInvoker.cli_workflow_up(runner, app_dir_path_b, WORKFLOW_MOCK_TYPE, namespace='concurrent-b')
            assert wait_for_reverse_proxy_intercept_on_port('example.com', 8181), \
                "NS B proxy did not enter mock-intercept mode on port 8181"

        @pytest.fixture(scope='class', autouse=True)
        def teardown(self, setup_ns_a, setup_ns_b, runner, app_dir_path_a, app_dir_path_b):
            yield
            ScaffoldCliInvoker.cli_workflow_down(runner, app_dir_path_a, WORKFLOW_MOCK_TYPE, namespace='concurrent-a')
            ScaffoldCliInvoker.cli_workflow_down(runner, app_dir_path_b, WORKFLOW_MOCK_TYPE, namespace='concurrent-b')

        def test_concurrent_requests_no_cross_namespace_contamination(self, runner, app_dir_path_a, app_dir_path_b):
            paths = [f'/concurrent-{i}' for i in range(5)]
            targets_a = [('http.badssl.com', p, 8180) for p in paths]
            targets_b = [('example.com', p, 8181) for p in paths]

            def _get(hostname, path, port):
                try:
                    resp = requests.get(
                        f'http://localhost:{port}{path}',
                        headers={'Host': hostname},
                        timeout=10.0,
                    )
                    return resp.status_code
                except Exception:
                    return -1

            with ThreadPoolExecutor(max_workers=10) as pool:
                futures = [pool.submit(_get, h, p, port) for h, p, port in targets_a + targets_b]
                [f.result() for f in as_completed(futures)]

            output_a = poll_for_any_log_entry(runner, WORKFLOW_MOCK_TYPE, app_dir_path_a, 'concurrent-a')
            output_b = poll_for_any_log_entry(runner, WORKFLOW_MOCK_TYPE, app_dir_path_b, 'concurrent-b')

            assert output_a, "Expected log entries in NS A after concurrent requests"
            assert output_b, "Expected log entries in NS B after concurrent requests"

            assert_no_entries_for_hostname(output_a, 'example.com')
            assert_no_entries_for_hostname(output_b, 'http.badssl.com')

    # ------------------------------------------------------------------
    # TestNamespaceTeardownIsolation
    # ------------------------------------------------------------------

    class TestNamespaceTeardownIsolation:
        """Bringing down NS A must leave NS B's logs and workflow intact."""

        @pytest.fixture(scope='class')
        def app_dir_path_a(self, base_dir):
            yield _make_app_dir(base_dir, 'teardown-a')

        @pytest.fixture(scope='class')
        def app_dir_path_b(self, base_dir):
            yield _make_app_dir(base_dir, 'teardown-b')

        @pytest.fixture(scope='class', autouse=True)
        def setup_both_namespaces(self, runner, app_dir_path_a, app_dir_path_b):
            ScaffoldCliInvoker.cli_app_create(runner, app_dir_path_a, 'teardown-a', proxy_mode='reverse', ui_port=4200)
            ScaffoldCliInvoker.cli_service_create(runner, app_dir_path_a, 'http.badssl.com', 'service-a', False, port=8180)
            ScaffoldCliInvoker.cli_workflow_up(runner, app_dir_path_a, WORKFLOW_MOCK_TYPE, namespace='teardown-a')
            assert wait_for_reverse_proxy_intercept_on_port('http.badssl.com', 8180), \
                "NS A proxy did not enter mock-intercept mode on port 8180"

            ScaffoldCliInvoker.cli_app_create(runner, app_dir_path_b, 'teardown-b', proxy_mode='reverse', ui_port=4201)
            ScaffoldCliInvoker.cli_service_create(runner, app_dir_path_b, 'example.com', 'service-b', False, port=8181)
            ScaffoldCliInvoker.cli_workflow_up(runner, app_dir_path_b, WORKFLOW_MOCK_TYPE, namespace='teardown-b')
            assert wait_for_reverse_proxy_intercept_on_port('example.com', 8181), \
                "NS B proxy did not enter mock-intercept mode on port 8181"

            # Seed at least one log entry in each namespace before tests run
            requests.get('http://localhost:8180/', headers={'Host': 'http.badssl.com'}, timeout=5.0)
            requests.get('http://localhost:8181/', headers={'Host': 'example.com'}, timeout=5.0)
            assert poll_for_any_log_entry(runner, WORKFLOW_MOCK_TYPE, app_dir_path_a, 'teardown-a'), \
                "Setup: expected seed entry in NS A"
            assert poll_for_any_log_entry(runner, WORKFLOW_MOCK_TYPE, app_dir_path_b, 'teardown-b'), \
                "Setup: expected seed entry in NS B"

        @pytest.fixture(scope='class', autouse=True)
        def teardown_ns_b(self, setup_both_namespaces, runner, app_dir_path_b):
            yield
            # NS A is brought down during test_ns_b_logs_survive_ns_a_teardown; only clean up NS B here
            ScaffoldCliInvoker.cli_workflow_down(runner, app_dir_path_b, WORKFLOW_MOCK_TYPE, namespace='teardown-b')

        def test_ns_b_logs_survive_ns_a_teardown(self, runner, app_dir_path_a, app_dir_path_b):
            pre_result = runner.invoke(scaffold, [
                'request', 'logs', 'list', WORKFLOW_MOCK_TYPE,
                '--context-dir-path', app_dir_path_b,
                '--namespace', 'teardown-b',
            ])
            assert pre_result.exit_code == 0
            pre_count = len(find_all_log_entries(pre_result.output))
            assert pre_count >= 1, "Setup: expected seed entries in NS B before NS A teardown"

            ScaffoldCliInvoker.cli_workflow_down(runner, app_dir_path_a, WORKFLOW_MOCK_TYPE, namespace='teardown-a')
            time.sleep(2)

            result = runner.invoke(scaffold, [
                'request', 'logs', 'list', WORKFLOW_MOCK_TYPE,
                '--context-dir-path', app_dir_path_b,
                '--namespace', 'teardown-b',
            ])
            assert result.exit_code == 0
            assert len(find_all_log_entries(result.output)) >= pre_count, \
                "NS B log entries must not be reduced by NS A teardown"

            resp = requests.get('http://localhost:8181/', headers={'Host': 'example.com'}, timeout=5.0)
            assert resp.status_code == NOT_FOUND, "NS B proxy should still be running after NS A teardown"

            new_entry = poll_for_any_log_entry(runner, WORKFLOW_MOCK_TYPE, app_dir_path_b, 'teardown-b', max_retries=20)
            assert new_entry, "NS B should continue logging after NS A teardown"

        def test_ns_a_log_file_readable_after_teardown(self, runner, app_dir_path_a):
            # NS A was torn down in the previous test; the log file must survive workflow down
            result = runner.invoke(scaffold, [
                'request', 'logs', 'list', WORKFLOW_MOCK_TYPE,
                '--context-dir-path', app_dir_path_a,
                '--namespace', 'teardown-a',
            ])
            assert result.exit_code == 0
            assert result.output.strip(), \
                "NS A log file should survive workflow down (critical for CI post-mortem debugging)"
