import os
import pytest

from click.testing import CliRunner

from stoobly_agent.app.cli.scaffold_cli import scaffold
from stoobly_agent.app.cli.scaffold_request_log_cli import request
from stoobly_agent.config.data_dir import DataDir, DATA_DIR_NAME
from stoobly_agent.test.app.cli.scaffold.local.cli_invoker import LocalScaffoldCliInvoker
from stoobly_agent.test.test_helper import reset


class TestScaffoldRequestLogCli:
    """Command-level tests for `scaffold request logs ...` that build a REAL scaffold
    app first (via `scaffold app create`), so the invocations match how the command is
    actually run rather than hand-crafted paths."""

    @pytest.fixture(autouse=True)
    def settings(self):
        return reset()

    @pytest.fixture(autouse=True)
    def isolate_data_dir_cache(self):
        DataDir._instances = None
        yield
        DataDir._instances = None

    @pytest.fixture
    def scaffold_app(self, tmp_path):
        """Create a real scaffold app and return its app dir (the PARENT of .stoobly,
        which is exactly what --app-dir-path receives in the generated Makefile/CLI)."""
        runner = CliRunner()
        app_dir = os.path.join(str(tmp_path), 'myapp')
        LocalScaffoldCliInvoker.cli_app_create(runner, app_dir, 'myapp')
        LocalScaffoldCliInvoker.cli_service_create(
            runner, app_dir, 'docs.stoobly.com', 'test-api', True
        )
        return app_dir

    @staticmethod
    def _nested_data_dir(app_dir: str) -> str:
        return os.path.join(app_dir, DATA_DIR_NAME, DATA_DIR_NAME)

    def test_realistic_request_logs_list_does_not_nest(self, scaffold_app):
        """Realistic flow: with a real scaffold app, invoke request logs the way the
        Makefile does -- `--app-dir-path <app>` (the parent). Asserts the command works
        and produces no nested `<app>/.stoobly/.stoobly`."""
        runner = CliRunner()

        result = runner.invoke(request, ['logs', 'list', 'mock', '--app-dir-path', scaffold_app])

        assert result.exit_code == 0, result.output
        assert not os.path.exists(self._nested_data_dir(scaffold_app)), (
            f"Realistic flow nested: {self._nested_data_dir(scaffold_app)}"
        )

    def test_list_nonexistent_workflow_does_not_create_tmp_folder(self, scaffold_app):
        """Running `logs list` for a workflow that doesn't exist must not create the tmp dir."""
        runner = CliRunner()
        result = runner.invoke(request, ['logs', 'list', 'mock123', '--app-dir-path', scaffold_app])

        assert result.exit_code == 0, result.output
        tmp_workflow_dir = os.path.join(scaffold_app, DATA_DIR_NAME, 'tmp', 'mock123')
        assert not os.path.exists(tmp_workflow_dir), (
            f"`logs list` created unexpected directory: {tmp_workflow_dir}"
        )

    def test_path_nonexistent_workflow_does_not_create_tmp_folder(self, scaffold_app):
        """Running `logs path` for a workflow that doesn't exist must not create the tmp dir."""
        runner = CliRunner()
        result = runner.invoke(request, ['logs', 'path', 'mock123', '--app-dir-path', scaffold_app])

        assert result.exit_code == 0, result.output
        tmp_workflow_dir = os.path.join(scaffold_app, DATA_DIR_NAME, 'tmp', 'mock123')
        assert not os.path.exists(tmp_workflow_dir), (
            f"`logs path` created unexpected directory: {tmp_workflow_dir}"
        )

    def test_workflow_logs_nonexistent_workflow_does_not_create_tmp_folder(self, scaffold_app):
        """Running `workflow logs` for a workflow that was never started must not create the tmp dir."""
        runner = CliRunner()
        result = runner.invoke(scaffold, ['workflow', 'logs', 'asdf123', '--app-dir-path', scaffold_app])

        assert result.exit_code == 1, result.output
        assert 'not running' in result.output, result.output
        tmp_workflow_dir = os.path.join(scaffold_app, DATA_DIR_NAME, 'tmp', 'asdf123')
        assert not os.path.exists(tmp_workflow_dir), (
            f"`workflow logs` created unexpected directory: {tmp_workflow_dir}"
        )

    def test_workflow_logs_dry_run_nonexistent_workflow_does_not_create_tmp_folder(self, scaffold_app):
        """Running `workflow logs --dry-run` for a nonexistent workflow must not create the tmp dir."""
        runner = CliRunner()
        result = runner.invoke(scaffold, ['workflow', 'logs', 'asdf123', '--dry-run', '--app-dir-path', scaffold_app])

        assert result.exit_code == 0, result.output
        tmp_workflow_dir = os.path.join(scaffold_app, DATA_DIR_NAME, 'tmp', 'asdf123')
        assert not os.path.exists(tmp_workflow_dir), (
            f"`workflow logs --dry-run` created unexpected directory: {tmp_workflow_dir}"
        )
