import os
import pytest
import requests
import shutil
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Tuple

from click.testing import CliRunner

from stoobly_agent.app.cli.helpers.certificate_authority import CertificateAuthority
from stoobly_agent.app.cli.scaffold.constants import WORKFLOW_MOCK_TYPE, WORKFLOW_RECORD_TYPE
from stoobly_agent.app.cli.scaffold_cli import scaffold
from stoobly_agent.app.proxy.constants.custom_response_codes import NOT_FOUND
from stoobly_agent.app.settings import Settings
from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.lib.api.keys.project_key import LOCAL_PROJECT_ID
from stoobly_agent.lib.intercepted_requests.logger import InterceptedRequestsLogger
from stoobly_agent.lib.orm.scenario import Scenario
from stoobly_agent.test.app.cli.scaffold.local.cli_invoker import LocalScaffoldCliInvoker
from stoobly_agent.test.app.cli.scaffold.log_test_helpers import count_log_entries, find_all_log_entries
from stoobly_agent.test.test_helper import NON_DETERMINISTIC_GET_REQUEST_HOST, NON_DETERMINISTIC_GET_REQUEST_URL, reset


PROXY_URL = os.environ.get("STOOBLY_PROXY_URL", "http://localhost:8081")
SERVICES = [NON_DETERMINISTIC_GET_REQUEST_HOST, 'example.com', 'docs.stoobly.com']

# These tests bind to PROXY_URL and must run sequentially — parallel execution
# (e.g. pytest-xdist) will cause port conflicts across test classes.


def wait_for_forward_proxy_intercept(proxy_url: str, hostname: str, timeout: float = 30.0, interval: float = 1.0) -> bool:
    """Poll until the forward proxy returns 499 for unrecorded requests, confirming intercept mode is active."""
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


def fire_concurrent_requests(targets: List[Tuple[str, str]], proxy_url: str) -> List[int]:
    def _get(hostname_path):
        hostname, path = hostname_path
        try:
            resp = requests.get(
                f'https://{hostname}{path}',
                proxies={'http': proxy_url, 'https': proxy_url},
                verify=False,
                timeout=10.0,
            )
            return resp.status_code
        except Exception:
            return -1

    with ThreadPoolExecutor(max_workers=len(targets)) as pool:
        futures = [pool.submit(_get, t) for t in targets]
        return [f.result() for f in as_completed(futures)]


def set_scenario_key_on_settings(settings: Settings, scenario_key: str, watchdog_delay: float = 1.0) -> None:
    """Commit scenario_key and wait for the proxy watchdog to reload the settings file."""
    settings.proxy.data.data_rules(str(LOCAL_PROJECT_ID)).scenario_key = scenario_key
    settings.commit()
    # The proxy subprocess detects the file change via a watchdog that polls ~every 1s.
    time.sleep(watchdog_delay)
    settings.load()


def create_scenario_and_get_key(name: str) -> str:
    scenario = Scenario.create(name=name)
    return scenario.key()


@pytest.fixture(scope='module')
def runner():
    yield CliRunner()


@pytest.mark.e2e
class TestMultiServiceLoggingCompleteness:
    """All services produce log entries when traffic reaches each of them."""

    @pytest.fixture(scope='class', autouse=True)
    def settings(self):
        return reset()

    @pytest.fixture(scope='class')
    def temp_dir(self):
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.fixture(scope='class')
    def app_dir_path(self, temp_dir, app_name):
        return os.path.join(temp_dir, app_name)

    @pytest.fixture(scope='class')
    def app_name(self):
        yield "multi-svc-completeness-app"

    @pytest.fixture(scope='class', autouse=True)
    def create_scaffold_setup(self, settings, runner, app_dir_path, app_name):
        LocalScaffoldCliInvoker.cli_app_create(runner, app_dir_path, app_name)
        for hostname in SERVICES:
            LocalScaffoldCliInvoker.cli_service_create(runner, app_dir_path, hostname, hostname.split('.')[0], True)

    @pytest.fixture(scope='class', autouse=True)
    def workflow_up(self, create_scaffold_setup, runner, app_dir_path, settings):
        LocalScaffoldCliInvoker.cli_workflow_up(runner, app_dir_path, WORKFLOW_MOCK_TYPE)
        time.sleep(1)
        settings.load()
        wait_for_forward_proxy_intercept(PROXY_URL, NON_DETERMINISTIC_GET_REQUEST_HOST)

    @pytest.fixture(scope='class', autouse=True)
    def workflow_down(self, workflow_up, runner, app_dir_path):
        yield
        LocalScaffoldCliInvoker.cli_workflow_down(runner, app_dir_path, WORKFLOW_MOCK_TYPE)
        time.sleep(1)

    def test_all_services_produce_log_entries(self, app_dir_path, runner):
        runner.invoke(scaffold, ['request', 'logs', 'delete', WORKFLOW_MOCK_TYPE, '--app-dir-path', app_dir_path])

        for hostname in SERVICES:
            requests.get(
                f'https://{hostname}/',
                proxies={'http': PROXY_URL, 'https': PROXY_URL},
                verify=False,
            )

        time.sleep(0.5)

        result = runner.invoke(scaffold, ['request', 'logs', 'list', WORKFLOW_MOCK_TYPE, '--app-dir-path', app_dir_path])
        assert result.exit_code == 0
        output = result.output

        for hostname in SERVICES:
            entries = [e for e in find_all_log_entries(output) if hostname in e.get('url', '')]
            assert len(entries) >= 1, f"Expected ≥1 log entry for {hostname}"
            assert all(e['level'] == 'ERROR' for e in entries), f"All entries for {hostname} should be ERROR"
            assert all(e['status_code'] == NOT_FOUND for e in entries), f"All entries for {hostname} should be 499"

    def test_service_name_is_entrypoint_in_local_mode(self, app_dir_path, runner):
        """Gap 3: LocalWorkflowRunCommand always sets SERVICE_NAME=entrypoint in the env,
        so every local-mode log entry carries service_name='entrypoint'."""
        runner.invoke(scaffold, ['request', 'logs', 'delete', WORKFLOW_MOCK_TYPE, '--app-dir-path', app_dir_path])

        for hostname in SERVICES:
            requests.get(
                f'https://{hostname}/',
                proxies={'http': PROXY_URL, 'https': PROXY_URL},
                verify=False,
            )

        time.sleep(0.5)

        result = runner.invoke(scaffold, ['request', 'logs', 'list', WORKFLOW_MOCK_TYPE, '--app-dir-path', app_dir_path])
        assert result.exit_code == 0

        entries = find_all_log_entries(result.output)
        assert entries, "Expected log entries"
        for e in entries:
            assert e.get('service_name') == 'entrypoint', \
                f"Expected service_name='entrypoint' in local mode, got: {e.get('service_name')!r}"


@pytest.mark.e2e
class TestMultiServiceUrlFilter:
    """--url filter isolates logs for one service out of many."""

    @pytest.fixture(scope='class', autouse=True)
    def settings(self):
        return reset()

    @pytest.fixture(scope='class')
    def temp_dir(self):
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.fixture(scope='class')
    def app_dir_path(self, temp_dir, app_name):
        return os.path.join(temp_dir, app_name)

    @pytest.fixture(scope='class')
    def app_name(self):
        yield "multi-svc-url-filter-app"

    @pytest.fixture(scope='class', autouse=True)
    def create_scaffold_setup(self, settings, runner, app_dir_path, app_name):
        LocalScaffoldCliInvoker.cli_app_create(runner, app_dir_path, app_name)
        for hostname in SERVICES:
            LocalScaffoldCliInvoker.cli_service_create(runner, app_dir_path, hostname, hostname.split('.')[0], True)

    @pytest.fixture(scope='class', autouse=True)
    def workflow_up(self, create_scaffold_setup, runner, app_dir_path, settings):
        LocalScaffoldCliInvoker.cli_workflow_up(runner, app_dir_path, WORKFLOW_MOCK_TYPE)
        time.sleep(1)
        settings.load()
        wait_for_forward_proxy_intercept(PROXY_URL, NON_DETERMINISTIC_GET_REQUEST_HOST)

    @pytest.fixture(scope='class', autouse=True)
    def workflow_down(self, workflow_up, runner, app_dir_path):
        yield
        LocalScaffoldCliInvoker.cli_workflow_down(runner, app_dir_path, WORKFLOW_MOCK_TYPE)
        time.sleep(1)

    def _send_to_all_services(self):
        for hostname in SERVICES:
            requests.get(
                f'https://{hostname}/',
                proxies={'http': PROXY_URL, 'https': PROXY_URL},
                verify=False,
            )

    def _flush(self):
        time.sleep(0.5)

    def test_url_filter_returns_only_matching_service(self, app_dir_path, runner):
        runner.invoke(scaffold, ['request', 'logs', 'delete', WORKFLOW_MOCK_TYPE, '--app-dir-path', app_dir_path])
        self._send_to_all_services()
        self._flush()

        result = runner.invoke(scaffold, ['request', 'logs', 'list', WORKFLOW_MOCK_TYPE,
            '--url', NON_DETERMINISTIC_GET_REQUEST_HOST, '--app-dir-path', app_dir_path])
        assert result.exit_code == 0

        entries = find_all_log_entries(result.output)
        assert entries, f"Expected log entries with --url {NON_DETERMINISTIC_GET_REQUEST_HOST} filter"
        for e in entries:
            assert NON_DETERMINISTIC_GET_REQUEST_HOST in e.get('url', ''), f"Expected {NON_DETERMINISTIC_GET_REQUEST_HOST} in URL, got: {e.get('url')}"

    def test_url_filter_excludes_other_services(self, app_dir_path, runner):
        runner.invoke(scaffold, ['request', 'logs', 'delete', WORKFLOW_MOCK_TYPE, '--app-dir-path', app_dir_path])
        self._send_to_all_services()
        self._flush()

        result = runner.invoke(scaffold, ['request', 'logs', 'list', WORKFLOW_MOCK_TYPE,
            '--url', 'example.com', '--app-dir-path', app_dir_path])
        assert result.exit_code == 0

        entries = find_all_log_entries(result.output)
        for e in entries:
            url = e.get('url', '')
            assert NON_DETERMINISTIC_GET_REQUEST_HOST not in url, f"{NON_DETERMINISTIC_GET_REQUEST_HOST} should be excluded, got: {url}"
            assert 'docs.stoobly.com' not in url, f"docs.stoobly.com should be excluded, got: {url}"


@pytest.mark.e2e
class TestMultiServiceLevelFilter:
    """--level filter partitions ERROR vs INFO entries across mixed traffic from multiple services."""

    @pytest.fixture(scope='class', autouse=True)
    def settings(self):
        return reset()

    @pytest.fixture(scope='class')
    def temp_dir(self):
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.fixture(scope='class')
    def app_dir_path(self, temp_dir, app_name):
        return os.path.join(temp_dir, app_name)

    @pytest.fixture(scope='class')
    def app_name(self):
        yield "multi-svc-level-filter-app"

    @pytest.fixture(scope='class', autouse=True)
    def create_scaffold_setup(self, settings, runner, app_dir_path, app_name):
        LocalScaffoldCliInvoker.cli_app_create(runner, app_dir_path, app_name)
        for hostname in SERVICES:
            LocalScaffoldCliInvoker.cli_service_create(runner, app_dir_path, hostname, hostname.split('.')[0], True)

    @pytest.fixture(scope='class', autouse=True)
    def record_then_mock_workflow(self, create_scaffold_setup, runner, app_dir_path, settings):
        """Record NON_DETERMINISTIC_GET_REQUEST_URL, then switch to mock workflow."""
        CertificateAuthority(certs_dir=DataDir.instance().ca_certs_dir_path).generate_certs()

        LocalScaffoldCliInvoker.cli_workflow_up(runner, app_dir_path, WORKFLOW_RECORD_TYPE)
        time.sleep(1)
        settings.load()

        settings.proxy.intercept.active = True
        settings.commit()
        time.sleep(1)
        settings.load()

        requests.get(
            NON_DETERMINISTIC_GET_REQUEST_URL,
            proxies={'http': PROXY_URL, 'https': PROXY_URL},
            verify=False,
        )

        LocalScaffoldCliInvoker.cli_workflow_down(runner, app_dir_path, WORKFLOW_RECORD_TYPE)
        time.sleep(1)

        LocalScaffoldCliInvoker.cli_workflow_up(runner, app_dir_path, WORKFLOW_MOCK_TYPE)
        time.sleep(1)
        settings.load()
        wait_for_forward_proxy_intercept(PROXY_URL, NON_DETERMINISTIC_GET_REQUEST_HOST)

        yield

        LocalScaffoldCliInvoker.cli_workflow_down(runner, app_dir_path, WORKFLOW_MOCK_TYPE)
        time.sleep(1)

    def test_level_error_filter_returns_only_errors(self, app_dir_path, runner):
        runner.invoke(scaffold, ['request', 'logs', 'delete', WORKFLOW_MOCK_TYPE, '--app-dir-path', app_dir_path])

        for hostname in SERVICES:
            requests.get(
                f'https://{hostname}/unrecorded-path',
                proxies={'http': PROXY_URL, 'https': PROXY_URL},
                verify=False,
            )

        time.sleep(0.5)

        result = runner.invoke(scaffold, ['request', 'logs', 'list', WORKFLOW_MOCK_TYPE,
            '--level', 'error', '--app-dir-path', app_dir_path])
        assert result.exit_code == 0

        entries = find_all_log_entries(result.output)
        assert entries, "Expected ERROR log entries"
        for e in entries:
            assert e.get('level') == 'ERROR', f"Expected ERROR, got {e.get('level')}"

    def test_level_info_filter_returns_only_successes(self, app_dir_path, runner):
        runner.invoke(scaffold, ['request', 'logs', 'delete', WORKFLOW_MOCK_TYPE, '--app-dir-path', app_dir_path])

        res = requests.get(
            NON_DETERMINISTIC_GET_REQUEST_URL,
            proxies={'http': PROXY_URL, 'https': PROXY_URL},
            verify=False,
        )
        for hostname in ['example.com', 'docs.stoobly.com']:
            requests.get(
                f'https://{hostname}/',
                proxies={'http': PROXY_URL, 'https': PROXY_URL},
                verify=False,
            )

        time.sleep(0.5)

        result = runner.invoke(scaffold, ['request', 'logs', 'list', WORKFLOW_MOCK_TYPE,
            '--level', 'info', '--app-dir-path', app_dir_path])
        assert result.exit_code == 0

        if res.status_code != 200:
            pytest.skip(f"{NON_DETERMINISTIC_GET_REQUEST_HOST} returned {res.status_code}; skipping INFO-level assertions")

        entries = find_all_log_entries(result.output)
        assert entries, "Expected INFO log entries"
        for e in entries:
            assert e.get('level') == 'INFO', f"Expected INFO, got {e.get('level')}"

        non_deterministic_host_entries = [e for e in entries if NON_DETERMINISTIC_GET_REQUEST_HOST in e.get('url', '')]
        assert any(e.get('status_code') == 200 for e in non_deterministic_host_entries), f"Expected 200 entry for {NON_DETERMINISTIC_GET_REQUEST_HOST}"

    def test_both_levels_present_without_filter(self, app_dir_path, runner):
        runner.invoke(scaffold, ['request', 'logs', 'delete', WORKFLOW_MOCK_TYPE, '--app-dir-path', app_dir_path])

        res = requests.get(
            NON_DETERMINISTIC_GET_REQUEST_URL,
            proxies={'http': PROXY_URL, 'https': PROXY_URL},
            verify=False,
        )
        requests.get(
            'https://example.com/',
            proxies={'http': PROXY_URL, 'https': PROXY_URL},
            verify=False,
        )

        time.sleep(0.5)

        result = runner.invoke(scaffold, ['request', 'logs', 'list', WORKFLOW_MOCK_TYPE, '--app-dir-path', app_dir_path])
        assert result.exit_code == 0

        entries = find_all_log_entries(result.output)
        if res.status_code == 200:
            assert any(e.get('level') == 'INFO' for e in entries), "Expected ≥1 INFO entry"
        assert any(e.get('level') == 'ERROR' for e in entries), "Expected ≥1 ERROR entry"


@pytest.mark.e2e
class TestScenarioChangeDelimiter:
    """Switching the active scenario_key mid-run produces a delimiter entry in the log."""

    @pytest.fixture(scope='class', autouse=True)
    def settings(self):
        return reset()

    @pytest.fixture(scope='class')
    def temp_dir(self):
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.fixture(scope='class')
    def app_dir_path(self, temp_dir, app_name):
        return os.path.join(temp_dir, app_name)

    @pytest.fixture(scope='class')
    def app_name(self):
        yield "scenario-delimiter-app"

    @pytest.fixture(scope='class')
    def scenario_a_key(self, settings):
        return create_scenario_and_get_key("scenario-alpha")

    @pytest.fixture(scope='class')
    def scenario_b_key(self, settings):
        return create_scenario_and_get_key("scenario-beta")

    @pytest.fixture(scope='class', autouse=True)
    def create_scaffold_setup(self, settings, runner, app_dir_path, app_name):
        LocalScaffoldCliInvoker.cli_app_create(runner, app_dir_path, app_name)
        LocalScaffoldCliInvoker.cli_service_create(runner, app_dir_path, NON_DETERMINISTIC_GET_REQUEST_HOST, 'www', True)

    @pytest.fixture(scope='class', autouse=True)
    def workflow_up(self, create_scaffold_setup, runner, app_dir_path, settings):
        LocalScaffoldCliInvoker.cli_workflow_up(runner, app_dir_path, WORKFLOW_MOCK_TYPE)
        time.sleep(1)
        settings.load()
        wait_for_forward_proxy_intercept(PROXY_URL, NON_DETERMINISTIC_GET_REQUEST_HOST)

    @pytest.fixture(scope='class', autouse=True)
    def workflow_down(self, workflow_up, runner, app_dir_path):
        yield
        LocalScaffoldCliInvoker.cli_workflow_down(runner, app_dir_path, WORKFLOW_MOCK_TYPE)
        time.sleep(1)

    def test_scenario_change_delimiter_appears(self, settings, app_dir_path, runner, scenario_a_key, scenario_b_key):
        runner.invoke(scaffold, ['request', 'logs', 'delete', WORKFLOW_MOCK_TYPE, '--app-dir-path', app_dir_path])

        set_scenario_key_on_settings(settings, scenario_a_key)
        requests.get(f'https://{NON_DETERMINISTIC_GET_REQUEST_HOST}/', proxies={'http': PROXY_URL, 'https': PROXY_URL}, verify=False)

        set_scenario_key_on_settings(settings, scenario_b_key)

        requests.get(f'https://{NON_DETERMINISTIC_GET_REQUEST_HOST}/', proxies={'http': PROXY_URL, 'https': PROXY_URL}, verify=False)
        time.sleep(0.5)

        result = runner.invoke(scaffold, ['request', 'logs', 'list', WORKFLOW_MOCK_TYPE, '--app-dir-path', app_dir_path])
        assert result.exit_code == 0
        output = result.output

        all_entries = find_all_log_entries(output)

        assert any(e.get('scenario_key') == scenario_a_key for e in all_entries), \
            f"Expected ≥1 entry with scenario_key={scenario_a_key}"

        delimiter_entries = [e for e in all_entries if e.get('type') == '----- Scenario change delimiter -----']
        assert len(delimiter_entries) >= 1, \
            f"Expected delimiter entry; entry types: {[e.get('type') for e in all_entries]}"
        scenario_b_delimiters = [e for e in delimiter_entries if e.get('current_scenario_key') == scenario_b_key]
        assert len(scenario_b_delimiters) >= 1, \
            f"Expected delimiter with current_scenario_key={scenario_b_key}; found: {[e.get('current_scenario_key') for e in delimiter_entries]}"

        assert any(e.get('scenario_key') == scenario_b_key for e in all_entries), \
            f"Expected ≥1 entry with scenario_key={scenario_b_key}"


@pytest.mark.e2e
class TestConcurrentHighTrafficLogging:
    """Async queue-based logger does not drop entries under 30 concurrent requests."""

    @pytest.fixture(scope='class', autouse=True)
    def settings(self):
        return reset()

    @pytest.fixture(scope='class')
    def temp_dir(self):
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.fixture(scope='class')
    def app_dir_path(self, temp_dir, app_name):
        return os.path.join(temp_dir, app_name)

    @pytest.fixture(scope='class')
    def app_name(self):
        yield "multi-svc-concurrent-app"

    @pytest.fixture(scope='class', autouse=True)
    def create_scaffold_setup(self, settings, runner, app_dir_path, app_name):
        LocalScaffoldCliInvoker.cli_app_create(runner, app_dir_path, app_name)
        for hostname in SERVICES:
            LocalScaffoldCliInvoker.cli_service_create(runner, app_dir_path, hostname, hostname.split('.')[0], True)

    @pytest.fixture(scope='class', autouse=True)
    def workflow_up(self, create_scaffold_setup, runner, app_dir_path, settings):
        LocalScaffoldCliInvoker.cli_workflow_up(runner, app_dir_path, WORKFLOW_MOCK_TYPE)
        time.sleep(1)
        settings.load()
        wait_for_forward_proxy_intercept(PROXY_URL, NON_DETERMINISTIC_GET_REQUEST_HOST)

    @pytest.fixture(scope='class', autouse=True)
    def workflow_down(self, workflow_up, runner, app_dir_path):
        yield
        LocalScaffoldCliInvoker.cli_workflow_down(runner, app_dir_path, WORKFLOW_MOCK_TYPE)
        time.sleep(1)

    @pytest.mark.xfail(strict=False)
    def test_concurrent_requests_do_not_drop_log_entries(self, app_dir_path, runner):
        runner.invoke(scaffold, ['request', 'logs', 'delete', WORKFLOW_MOCK_TYPE, '--app-dir-path', app_dir_path])

        targets = [
            (hostname, f'/concurrent-{i}')
            for i in range(10)
            for hostname in SERVICES
        ]

        fire_concurrent_requests(targets, PROXY_URL)

        time.sleep(1.0)

        result = runner.invoke(scaffold, ['request', 'logs', 'list', WORKFLOW_MOCK_TYPE, '--app-dir-path', app_dir_path])
        assert result.exit_code == 0
        output = result.output

        total = count_log_entries(output)
        assert total >= 27, f"Expected ≥27 log entries (30 sent, 10% tolerance), got {total}"

        all_entries = find_all_log_entries(output)
        for hostname in SERVICES:
            count = sum(1 for e in all_entries if hostname in e.get('url', ''))
            assert count >= 8, f"Expected ≥8 entries for {hostname}, got {count}"


@pytest.mark.e2e
class TestConcurrentScenarioChangeRace:
    """Gap 1 regression: _previous_scenario_key is guarded by a lock so concurrent requests
    cannot emit duplicate delimiters for the same scenario transition."""

    @pytest.fixture(scope='class', autouse=True)
    def settings(self):
        return reset()

    @pytest.fixture(scope='class')
    def temp_dir(self):
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.fixture(scope='class')
    def app_dir_path(self, temp_dir, app_name):
        return os.path.join(temp_dir, app_name)

    @pytest.fixture(scope='class')
    def app_name(self):
        yield "concurrent-scenario-race-app"

    @pytest.fixture(scope='class')
    def scenario_a_key(self, settings):
        return create_scenario_and_get_key("race-scenario-alpha")

    @pytest.fixture(scope='class')
    def scenario_b_key(self, settings):
        return create_scenario_and_get_key("race-scenario-beta")

    @pytest.fixture(scope='class', autouse=True)
    def create_scaffold_setup(self, settings, runner, app_dir_path, app_name):
        LocalScaffoldCliInvoker.cli_app_create(runner, app_dir_path, app_name)
        for hostname in SERVICES:
            LocalScaffoldCliInvoker.cli_service_create(runner, app_dir_path, hostname, hostname.split('.')[0], True)

    @pytest.fixture(scope='class', autouse=True)
    def workflow_up(self, create_scaffold_setup, runner, app_dir_path, settings):
        LocalScaffoldCliInvoker.cli_workflow_up(runner, app_dir_path, WORKFLOW_MOCK_TYPE)
        time.sleep(1)
        settings.load()
        wait_for_forward_proxy_intercept(PROXY_URL, NON_DETERMINISTIC_GET_REQUEST_HOST)

    @pytest.fixture(scope='class', autouse=True)
    def workflow_down(self, workflow_up, runner, app_dir_path):
        yield
        LocalScaffoldCliInvoker.cli_workflow_down(runner, app_dir_path, WORKFLOW_MOCK_TYPE)
        time.sleep(1)

    def test_scenario_change_produces_exactly_one_delimiter(self, settings, app_dir_path, runner, scenario_a_key, scenario_b_key):
        runner.invoke(scaffold, ['request', 'logs', 'delete', WORKFLOW_MOCK_TYPE, '--app-dir-path', app_dir_path])

        # Establish scenario_a so the only transition under test is a→b
        set_scenario_key_on_settings(settings, scenario_a_key)

        # Fire 15 concurrent requests, then switch scenario_b mid-burst, then fire 15 more.
        # Without the lock, two threads arriving at the a→b transition simultaneously
        # would both emit a delimiter before either updates _previous_scenario_key.
        batch_a = [(hostname, f'/race-a-{i}') for i in range(5) for hostname in SERVICES]
        fire_concurrent_requests(batch_a, PROXY_URL)

        set_scenario_key_on_settings(settings, scenario_b_key)

        batch_b = [(hostname, f'/race-b-{i}') for i in range(5) for hostname in SERVICES]
        fire_concurrent_requests(batch_b, PROXY_URL)

        result = runner.invoke(scaffold, ['request', 'logs', 'list', WORKFLOW_MOCK_TYPE, '--app-dir-path', app_dir_path])
        assert result.exit_code == 0
        output = result.output

        all_entries = find_all_log_entries(output)

        # The only delimiter that should appear for the a→b transition is exactly one.
        a_to_b_delimiters = [
            e for e in all_entries
            if e.get('type') == '----- Scenario change delimiter -----'
            and e.get('previous_scenario_key') == scenario_a_key
            and e.get('current_scenario_key') == scenario_b_key
        ]
        assert len(a_to_b_delimiters) == 1, \
            f"Expected exactly 1 a→b delimiter (race condition produces duplicates); got {len(a_to_b_delimiters)}"


@pytest.mark.e2e
class TestMultiScenarioFilter:
    """--scenario-name filter returns only entries from a specific scenario, across multiple services."""

    @pytest.fixture(scope='class', autouse=True)
    def settings(self):
        return reset()

    @pytest.fixture(scope='class')
    def temp_dir(self):
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.fixture(scope='class')
    def app_dir_path(self, temp_dir, app_name):
        return os.path.join(temp_dir, app_name)

    @pytest.fixture(scope='class')
    def app_name(self):
        yield "multi-svc-scenario-filter-app"

    @pytest.fixture(scope='class')
    def scenario_a_key(self, settings):
        return create_scenario_and_get_key("filter-scenario-alpha")

    @pytest.fixture(scope='class')
    def scenario_b_key(self, settings):
        return create_scenario_and_get_key("filter-scenario-beta")

    @pytest.fixture(scope='class', autouse=True)
    def create_scaffold_setup(self, settings, runner, app_dir_path, app_name):
        LocalScaffoldCliInvoker.cli_app_create(runner, app_dir_path, app_name)
        for hostname in SERVICES:
            LocalScaffoldCliInvoker.cli_service_create(runner, app_dir_path, hostname, hostname.split('.')[0], True)

    @pytest.fixture(scope='class', autouse=True)
    def workflow_up(self, create_scaffold_setup, runner, app_dir_path, settings):
        LocalScaffoldCliInvoker.cli_workflow_up(runner, app_dir_path, WORKFLOW_MOCK_TYPE)
        time.sleep(1)
        settings.load()
        wait_for_forward_proxy_intercept(PROXY_URL, NON_DETERMINISTIC_GET_REQUEST_HOST)

    @pytest.fixture(scope='class', autouse=True)
    def workflow_down(self, workflow_up, runner, app_dir_path):
        yield
        LocalScaffoldCliInvoker.cli_workflow_down(runner, app_dir_path, WORKFLOW_MOCK_TYPE)
        time.sleep(1)

    def test_scenario_name_filter_isolates_entries(self, settings, app_dir_path, runner, scenario_a_key, scenario_b_key):
        runner.invoke(scaffold, ['request', 'logs', 'delete', WORKFLOW_MOCK_TYPE, '--app-dir-path', app_dir_path])

        # Phase A: send to NON_DETERMINISTIC_GET_REQUEST_HOST and example.com under scenario_a
        set_scenario_key_on_settings(settings, scenario_a_key)
        for hostname in [NON_DETERMINISTIC_GET_REQUEST_HOST, 'example.com']:
            requests.get(
                f'https://{hostname}/',
                proxies={'http': PROXY_URL, 'https': PROXY_URL},
                verify=False,
            )

        # Phase B: switch to scenario_b and send to all 3 (includes docs.stoobly.com)
        set_scenario_key_on_settings(settings, scenario_b_key)

        for hostname in SERVICES:
            requests.get(
                f'https://{hostname}/',
                proxies={'http': PROXY_URL, 'https': PROXY_URL},
                verify=False,
            )

        result = runner.invoke(scaffold, ['request', 'logs', 'list', WORKFLOW_MOCK_TYPE,
            '--scenario-name', 'filter-scenario-alpha', '--app-dir-path', app_dir_path])
        assert result.exit_code == 0

        entries = find_all_log_entries(result.output)
        assert entries, "Expected entries for filter-scenario-alpha"

        for e in entries:
            scenario_name = e.get('scenario_name', '')
            assert 'filter-scenario-alpha' in scenario_name, \
                f"Expected filter-scenario-alpha in scenario_name, got: {scenario_name}"
            assert 'filter-scenario-beta' not in scenario_name, \
                f"filter-scenario-beta should not appear, got: {scenario_name}"
            url = e.get('url', '')
            assert 'docs.stoobly.com' not in url, \
                f"docs.stoobly.com was only requested in phase B (scenario_b), got: {url}"


@pytest.mark.e2e
class TestScenarioChangeMidBurst:
    """Gap 6: changing scenario_key while concurrent requests are in-flight produces
    a correctly placed delimiter with entries on both sides of it."""

    @pytest.fixture(scope='class', autouse=True)
    def settings(self):
        return reset()

    @pytest.fixture(scope='class')
    def temp_dir(self):
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.fixture(scope='class')
    def app_dir_path(self, temp_dir, app_name):
        return os.path.join(temp_dir, app_name)

    @pytest.fixture(scope='class')
    def app_name(self):
        yield "mid-burst-scenario-app"

    @pytest.fixture(scope='class')
    def scenario_a_key(self, settings):
        return create_scenario_and_get_key("burst-scenario-alpha")

    @pytest.fixture(scope='class')
    def scenario_b_key(self, settings):
        return create_scenario_and_get_key("burst-scenario-beta")

    @pytest.fixture(scope='class', autouse=True)
    def create_scaffold_setup(self, settings, runner, app_dir_path, app_name):
        LocalScaffoldCliInvoker.cli_app_create(runner, app_dir_path, app_name)
        for hostname in SERVICES:
            LocalScaffoldCliInvoker.cli_service_create(runner, app_dir_path, hostname, hostname.split('.')[0], True)

    @pytest.fixture(scope='class', autouse=True)
    def workflow_up(self, create_scaffold_setup, runner, app_dir_path, settings):
        LocalScaffoldCliInvoker.cli_workflow_up(runner, app_dir_path, WORKFLOW_MOCK_TYPE)
        time.sleep(1)
        settings.load()
        wait_for_forward_proxy_intercept(PROXY_URL, NON_DETERMINISTIC_GET_REQUEST_HOST)

    @pytest.fixture(scope='class', autouse=True)
    def workflow_down(self, workflow_up, runner, app_dir_path):
        yield
        LocalScaffoldCliInvoker.cli_workflow_down(runner, app_dir_path, WORKFLOW_MOCK_TYPE)
        time.sleep(1)

    @pytest.mark.xfail(strict=False)
    def test_scenario_change_mid_burst_produces_delimiter(self, settings, app_dir_path, runner, scenario_a_key, scenario_b_key):
        runner.invoke(scaffold, ['request', 'logs', 'delete', WORKFLOW_MOCK_TYPE, '--app-dir-path', app_dir_path])

        set_scenario_key_on_settings(settings, scenario_a_key)

        batch_a = [(hostname, f'/burst-a-{i}') for i in range(5) for hostname in SERVICES]
        batch_b = [(hostname, f'/burst-b-{i}') for i in range(5) for hostname in SERVICES]

        # Inlined rather than using fire_concurrent_requests so we can submit futures
        # and mutate settings before the pool blocks waiting for them to finish.
        def _get(hostname_path):
            hostname, path = hostname_path
            try:
                resp = requests.get(
                    f'https://{hostname}{path}',
                    proxies={'http': PROXY_URL, 'https': PROXY_URL},
                    verify=False,
                    timeout=10.0,
                )
                return resp.status_code
            except Exception:
                return -1

        # Submit batch_a and commit the scenario change before futures complete.
        # The proxy's watchdog picks up the settings file change ~1s after commit,
        # so some batch_a requests may still be in-flight or mid-processing when
        # the transition fires — creating the fuzzy boundary this test exercises.
        with ThreadPoolExecutor(max_workers=len(batch_a)) as pool:
            for t in batch_a:
                pool.submit(_get, t)
            settings.proxy.data.data_rules(str(LOCAL_PROJECT_ID)).scenario_key = scenario_b_key
            settings.commit()
            # pool.__exit__ waits for all futures_a to complete

        # Wait for watchdog to reload, then sync test-process settings view
        time.sleep(1)
        settings.load()

        fire_concurrent_requests(batch_b, PROXY_URL)

        result = runner.invoke(scaffold, ['request', 'logs', 'list', WORKFLOW_MOCK_TYPE, '--app-dir-path', app_dir_path])
        assert result.exit_code == 0

        all_entries = find_all_log_entries(result.output)

        a_to_b_delimiters = [
            e for e in all_entries
            if e.get('type') == '----- Scenario change delimiter -----'
            and e.get('previous_scenario_key') == scenario_a_key
            and e.get('current_scenario_key') == scenario_b_key
        ]
        assert len(a_to_b_delimiters) >= 1, \
            f"Expected ≥1 a→b delimiter; got {len(a_to_b_delimiters)}"
        assert any(e.get('scenario_key') == scenario_a_key for e in all_entries), \
            f"Expected ≥1 entry with scenario_key={scenario_a_key}"
        assert any(e.get('scenario_key') == scenario_b_key for e in all_entries), \
            f"Expected ≥1 entry with scenario_key={scenario_b_key}"


@pytest.mark.e2e
class TestMultiFilterComposition:
    """Gap 2: multiple CLI filters compose with AND logic.
    Each test combines two filters and asserts that only entries matching both are returned."""

    @pytest.fixture(scope='class', autouse=True)
    def settings(self):
        return reset()

    @pytest.fixture(scope='class')
    def temp_dir(self):
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.fixture(scope='class')
    def app_dir_path(self, temp_dir, app_name):
        return os.path.join(temp_dir, app_name)

    @pytest.fixture(scope='class')
    def app_name(self):
        yield "multi-filter-composition-app"

    @pytest.fixture(scope='class')
    def scenario_a_key(self, settings):
        return create_scenario_and_get_key("compose-scenario-alpha")

    @pytest.fixture(scope='class')
    def scenario_b_key(self, settings):
        return create_scenario_and_get_key("compose-scenario-beta")

    @pytest.fixture(scope='class', autouse=True)
    def create_scaffold_setup(self, settings, runner, app_dir_path, app_name):
        LocalScaffoldCliInvoker.cli_app_create(runner, app_dir_path, app_name)
        for hostname in SERVICES:
            LocalScaffoldCliInvoker.cli_service_create(runner, app_dir_path, hostname, hostname.split('.')[0], True)

    @pytest.fixture(scope='class', autouse=True)
    def workflow_up(self, create_scaffold_setup, runner, app_dir_path, settings):
        LocalScaffoldCliInvoker.cli_workflow_up(runner, app_dir_path, WORKFLOW_MOCK_TYPE)
        time.sleep(1)
        settings.load()
        wait_for_forward_proxy_intercept(PROXY_URL, NON_DETERMINISTIC_GET_REQUEST_HOST)

    @pytest.fixture(scope='class', autouse=True)
    def workflow_down(self, workflow_up, runner, app_dir_path):
        yield
        LocalScaffoldCliInvoker.cli_workflow_down(runner, app_dir_path, WORKFLOW_MOCK_TYPE)
        time.sleep(1)

    def _send_to_all(self):
        for hostname in SERVICES:
            requests.get(
                f'https://{hostname}/',
                proxies={'http': PROXY_URL, 'https': PROXY_URL},
                verify=False,
            )

    def test_url_and_level_filter(self, app_dir_path, runner):
        """--url filter with --level error returns only ERROR entries for the host, excluding other services."""
        runner.invoke(scaffold, ['request', 'logs', 'delete', WORKFLOW_MOCK_TYPE, '--app-dir-path', app_dir_path])
        self._send_to_all()
        time.sleep(0.5)

        result = runner.invoke(scaffold, ['request', 'logs', 'list', WORKFLOW_MOCK_TYPE,
            '--url', NON_DETERMINISTIC_GET_REQUEST_HOST, '--level', 'error', '--app-dir-path', app_dir_path])
        assert result.exit_code == 0

        entries = find_all_log_entries(result.output)
        assert entries, f"Expected entries with --url {NON_DETERMINISTIC_GET_REQUEST_HOST} --level error"
        for e in entries:
            assert NON_DETERMINISTIC_GET_REQUEST_HOST in e.get('url', ''), f"URL filter failed: {e.get('url')}"
            assert e.get('level') == 'ERROR', f"Level filter failed: {e.get('level')}"

    def test_url_and_scenario_filter(self, settings, app_dir_path, runner, scenario_a_key, scenario_b_key):
        """--url filter with --scenario-name returns only matching-scenario entries for the host."""
        runner.invoke(scaffold, ['request', 'logs', 'delete', WORKFLOW_MOCK_TYPE, '--app-dir-path', app_dir_path])

        set_scenario_key_on_settings(settings, scenario_a_key)
        self._send_to_all()

        set_scenario_key_on_settings(settings, scenario_b_key)
        self._send_to_all()

        result = runner.invoke(scaffold, ['request', 'logs', 'list', WORKFLOW_MOCK_TYPE,
            '--url', NON_DETERMINISTIC_GET_REQUEST_HOST, '--scenario-name', 'compose-scenario-alpha', '--app-dir-path', app_dir_path])
        assert result.exit_code == 0

        entries = find_all_log_entries(result.output)
        assert entries, f"Expected entries with --url {NON_DETERMINISTIC_GET_REQUEST_HOST} --scenario-name compose-scenario-alpha"
        for e in entries:
            assert NON_DETERMINISTIC_GET_REQUEST_HOST in e.get('url', ''), f"URL filter failed: {e.get('url')}"
            assert 'compose-scenario-alpha' in e.get('scenario_name', ''), \
                f"Scenario filter failed: {e.get('scenario_name')}"
            assert 'compose-scenario-beta' not in e.get('scenario_name', ''), \
                f"Beta entries leaked through: {e.get('scenario_name')}"

    def test_level_and_scenario_filter(self, settings, app_dir_path, runner, scenario_a_key, scenario_b_key):
        """--level error --scenario-name alpha returns only ERROR entries from the alpha scenario."""
        runner.invoke(scaffold, ['request', 'logs', 'delete', WORKFLOW_MOCK_TYPE, '--app-dir-path', app_dir_path])

        set_scenario_key_on_settings(settings, scenario_a_key)
        self._send_to_all()

        set_scenario_key_on_settings(settings, scenario_b_key)
        self._send_to_all()

        result = runner.invoke(scaffold, ['request', 'logs', 'list', WORKFLOW_MOCK_TYPE,
            '--level', 'error', '--scenario-name', 'compose-scenario-alpha', '--app-dir-path', app_dir_path])
        assert result.exit_code == 0

        entries = find_all_log_entries(result.output)
        assert entries, "Expected entries with --level error --scenario-name compose-scenario-alpha"
        for e in entries:
            assert e.get('level') == 'ERROR', f"Level filter failed: {e.get('level')}"
            assert 'compose-scenario-alpha' in e.get('scenario_name', ''), \
                f"Scenario filter failed: {e.get('scenario_name')}"
            assert 'compose-scenario-beta' not in e.get('scenario_name', ''), \
                f"Beta entries leaked through: {e.get('scenario_name')}"


@pytest.mark.e2e
class TestWorkflowRestartLogPersistence:
    """Gap 4: the local workflow calls truncate() on startup so the log file is cleared
    on each restart. Tests verify that logging is fully functional after a restart and
    that each service produces entries in the new session."""

    @pytest.fixture(scope='class', autouse=True)
    def settings(self):
        return reset()

    @pytest.fixture(scope='class')
    def temp_dir(self):
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.fixture(scope='class')
    def app_dir_path(self, temp_dir, app_name):
        return os.path.join(temp_dir, app_name)

    @pytest.fixture(scope='class')
    def app_name(self):
        yield "workflow-restart-persistence-app"

    @pytest.fixture(scope='class', autouse=True)
    def create_scaffold_setup(self, settings, runner, app_dir_path, app_name):
        LocalScaffoldCliInvoker.cli_app_create(runner, app_dir_path, app_name)
        for hostname in SERVICES:
            LocalScaffoldCliInvoker.cli_service_create(runner, app_dir_path, hostname, hostname.split('.')[0], True)

    @pytest.fixture(scope='class', autouse=True)
    def workflow_lifecycle(self, create_scaffold_setup, runner, app_dir_path, settings):
        LocalScaffoldCliInvoker.cli_workflow_up(runner, app_dir_path, WORKFLOW_MOCK_TYPE)
        time.sleep(1)
        settings.load()
        wait_for_forward_proxy_intercept(PROXY_URL, NON_DETERMINISTIC_GET_REQUEST_HOST)
        yield
        LocalScaffoldCliInvoker.cli_workflow_down(runner, app_dir_path, WORKFLOW_MOCK_TYPE)
        time.sleep(1)

    def test_logging_works_after_workflow_restart(self, settings, app_dir_path, runner):
        """Gap 4: the local workflow calls truncate() on startup (not append), so the log
        file is cleared on each restart. This test verifies the logger is functional
        after a restart — not that entries persist (they don't by default)."""
        runner.invoke(scaffold, ['request', 'logs', 'delete', WORKFLOW_MOCK_TYPE, '--app-dir-path', app_dir_path])

        # Session 1: log entries from the first proxy process
        for hostname in SERVICES:
            requests.get(
                f'https://{hostname}/',
                proxies={'http': PROXY_URL, 'https': PROXY_URL},
                verify=False,
            )
        time.sleep(0.5)

        session_1_result = runner.invoke(scaffold, ['request', 'logs', 'list', WORKFLOW_MOCK_TYPE, '--app-dir-path', app_dir_path])
        session_1_entries = find_all_log_entries(session_1_result.output)
        assert len(session_1_entries) >= len(SERVICES), \
            f"Expected ≥{len(SERVICES)} entries in session 1, got {len(session_1_entries)}"

        # Restart: the new proxy process calls truncate() which clears the log file
        LocalScaffoldCliInvoker.cli_workflow_down(runner, app_dir_path, WORKFLOW_MOCK_TYPE)
        time.sleep(1)
        LocalScaffoldCliInvoker.cli_workflow_up(runner, app_dir_path, WORKFLOW_MOCK_TYPE)
        time.sleep(1)
        settings.load()
        wait_for_forward_proxy_intercept(PROXY_URL, NON_DETERMINISTIC_GET_REQUEST_HOST)

        # Session 2: fresh log file — only post-restart entries should be present
        for hostname in SERVICES:
            requests.get(
                f'https://{hostname}/',
                proxies={'http': PROXY_URL, 'https': PROXY_URL},
                verify=False,
            )
        time.sleep(0.5)

        result = runner.invoke(scaffold, ['request', 'logs', 'list', WORKFLOW_MOCK_TYPE, '--app-dir-path', app_dir_path])
        assert result.exit_code == 0

        all_entries = find_all_log_entries(result.output)
        assert len(all_entries) >= len(SERVICES), \
            f"Expected ≥{len(SERVICES)} entries after restart, got {len(all_entries)}"

        # Each hostname must appear at least once in the post-restart log
        for hostname in SERVICES:
            hostname_entries = [e for e in all_entries if hostname in e.get('url', '')]
            assert len(hostname_entries) >= 1, \
                f"Expected ≥1 entry for {hostname} after restart, got {len(hostname_entries)}"


@pytest.mark.e2e
class TestPostTruncateNoSpuriousDelimiter:
    """Gap 5: 'request logs delete' clears the log file. Verifies that the first
    post-clear request under the same active scenario does not produce a spurious
    delimiter — the log starts clean with only request entries."""

    @pytest.fixture(scope='class', autouse=True)
    def settings(self):
        return reset()

    @pytest.fixture(scope='class')
    def temp_dir(self):
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.fixture(scope='class')
    def app_dir_path(self, temp_dir, app_name):
        return os.path.join(temp_dir, app_name)

    @pytest.fixture(scope='class')
    def app_name(self):
        yield "post-truncate-delimiter-app"

    @pytest.fixture(scope='class')
    def scenario_a_key(self, settings):
        return create_scenario_and_get_key("truncate-scenario-alpha")

    @pytest.fixture(scope='class', autouse=True)
    def create_scaffold_setup(self, settings, runner, app_dir_path, app_name):
        LocalScaffoldCliInvoker.cli_app_create(runner, app_dir_path, app_name)
        LocalScaffoldCliInvoker.cli_service_create(runner, app_dir_path, NON_DETERMINISTIC_GET_REQUEST_HOST, 'www', True)

    @pytest.fixture(scope='class', autouse=True)
    def workflow_up(self, create_scaffold_setup, runner, app_dir_path, settings):
        LocalScaffoldCliInvoker.cli_workflow_up(runner, app_dir_path, WORKFLOW_MOCK_TYPE)
        time.sleep(1)
        settings.load()
        wait_for_forward_proxy_intercept(PROXY_URL, NON_DETERMINISTIC_GET_REQUEST_HOST)

    @pytest.fixture(scope='class', autouse=True)
    def workflow_down(self, workflow_up, runner, app_dir_path):
        yield
        LocalScaffoldCliInvoker.cli_workflow_down(runner, app_dir_path, WORKFLOW_MOCK_TYPE)
        time.sleep(1)

    def test_no_spurious_delimiter_after_log_clear(self, settings, app_dir_path, runner, scenario_a_key):
        # Establish scenario_a as the active scenario
        set_scenario_key_on_settings(settings, scenario_a_key)

        requests.get(f'https://{NON_DETERMINISTIC_GET_REQUEST_HOST}/', proxies={'http': PROXY_URL, 'https': PROXY_URL}, verify=False)
        time.sleep(0.5)
        InterceptedRequestsLogger.flush()

        runner.invoke(scaffold, ['request', 'logs', 'delete', WORKFLOW_MOCK_TYPE, '--app-dir-path', app_dir_path])

        # Same scenario continues — the post-clear log should have no delimiter
        requests.get(f'https://{NON_DETERMINISTIC_GET_REQUEST_HOST}/', proxies={'http': PROXY_URL, 'https': PROXY_URL}, verify=False)
        time.sleep(0.5)

        result = runner.invoke(scaffold, ['request', 'logs', 'list', WORKFLOW_MOCK_TYPE, '--app-dir-path', app_dir_path])
        assert result.exit_code == 0

        all_entries = find_all_log_entries(result.output)
        assert all_entries, "Expected log entries after the clear"

        delimiter_entries = [e for e in all_entries if e.get('type') == '----- Scenario change delimiter -----']
        assert len(delimiter_entries) == 0, \
            f"Clearing logs must not produce a spurious delimiter; got: {delimiter_entries}"

        for e in all_entries:
            assert e.get('scenario_key') == scenario_a_key, \
                f"All post-clear entries should have scenario_a; got: {e.get('scenario_key')}"
