import pytest

from stoobly_agent.test.app.cli.scaffold.docker.cli_invoker import TMP_E2E_LOG_PATH


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when in ('setup', 'call') and report.failed:
        try:
            with open(TMP_E2E_LOG_PATH) as f:
                content = f.read().strip()
            if content:
                report.sections.append(('E2E Debug Log', content))
        except FileNotFoundError:
            pass
