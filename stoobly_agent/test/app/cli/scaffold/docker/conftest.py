import pytest

from stoobly_agent.app.cli.scaffold.app import App
from stoobly_agent.app.cli.scaffold.workflow_namespace import WorkflowNamespace
from stoobly_agent.lib.intercepted_requests.scaffold_logger import ScaffoldInterceptedRequestsLogger
from stoobly_agent.test.app.cli.scaffold.docker.cli_invoker import TMP_E2E_LOG_PATH


def _attach_file_section(report, title, path):
    try:
        with open(path) as f:
            content = f.read().strip()
        if content:
            report.sections.append((title, content))
    except FileNotFoundError:
        pass


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.failed:
        _attach_file_section(report, 'E2E Debug Log', TMP_E2E_LOG_PATH)

        # Attach the request log for the specific workflow under test.
        # Multi-namespace tests use app_dir_path_a/app_dir_path_b (not app_dir_path)
        # and hardcode namespaces rather than using a fixture, so they are skipped here.
        app_dir_path = item.funcargs.get('app_dir_path')
        workflow_name = item.funcargs.get('target_workflow_name')
        if app_dir_path and workflow_name:
            app = App(app_dir_path)
            workflow_namespace = WorkflowNamespace(app, workflow_name)
            log_path = ScaffoldInterceptedRequestsLogger._get_file_path(
                workflow=workflow_name,
                workflow_namespace=workflow_namespace,
            )
            _attach_file_section(report, 'E2E Request Logs', log_path)
