import os

import pytest

from click.testing import CliRunner

from stoobly_agent.app.cli.scaffold_cli import scaffold
from stoobly_agent.app.cli.scaffold_request_log_cli import request
from stoobly_agent.config.data_dir import DataDir, DATA_DIR_NAME
from stoobly_agent.test.test_helper import reset


class TestReadOnlyScaffoldCommandsDoNotCreateDataDir:
    """Read-only scaffold commands pointed at a directory that is not a scaffold must
    fail without creating a `.stoobly` folder in it."""

    @pytest.fixture(autouse=True)
    def settings(self):
        return reset()

    @pytest.fixture(autouse=True)
    def isolate_data_dir_cache(self):
        DataDir._instances = None
        yield
        DataDir._instances = None

    @pytest.fixture
    def empty_dir(self, tmp_path):
        app_dir = os.path.join(str(tmp_path), 'empty')
        os.makedirs(app_dir)
        return app_dir

    def _assert_no_data_dir(self, app_dir: str):
        assert not os.path.exists(os.path.join(app_dir, DATA_DIR_NAME)), (
            f"Command created {os.path.join(app_dir, DATA_DIR_NAME)}"
        )

    def test_request_logs_list_fails_without_creating_data_dir(self, empty_dir):
        result = CliRunner().invoke(request, ['logs', 'list', 'record', '--app-dir-path', empty_dir])

        assert result.exit_code != 0, result.output
        self._assert_no_data_dir(empty_dir)

    def test_request_logs_path_fails_without_creating_data_dir(self, empty_dir):
        result = CliRunner().invoke(request, ['logs', 'path', 'record', '--app-dir-path', empty_dir])

        assert result.exit_code != 0, result.output
        self._assert_no_data_dir(empty_dir)

    def test_service_list_fails_without_creating_data_dir(self, empty_dir):
        result = CliRunner().invoke(scaffold, ['service', 'list', '--app-dir-path', empty_dir])

        assert result.exit_code != 0, result.output
        self._assert_no_data_dir(empty_dir)

    def test_workflow_show_fails_without_creating_data_dir(self, empty_dir):
        result = CliRunner().invoke(scaffold, ['workflow', 'show', 'record', '--app-dir-path', empty_dir])

        assert result.exit_code != 0, result.output
        self._assert_no_data_dir(empty_dir)

    def test_failed_service_delete_does_not_create_data_dir(self, empty_dir):
        result = CliRunner().invoke(scaffold, ['service', 'delete', 'svc', '--app-dir-path', empty_dir])

        assert result.exit_code != 0, result.output
        self._assert_no_data_dir(empty_dir)

    def test_service_create_requires_scaffold_app(self, empty_dir):
        result = CliRunner().invoke(scaffold, ['service', 'create', 'api', '--app-dir-path', empty_dir, '--quiet'])

        assert result.exit_code != 0, result.output
        assert 'does not exist' in result.output
        self._assert_no_data_dir(empty_dir)

    def test_workflow_copy_requires_scaffold_app(self, empty_dir):
        result = CliRunner().invoke(scaffold, ['workflow', 'copy', 'record', 'dest', '--app-dir-path', empty_dir, '--service', 'api'])

        assert result.exit_code != 0, result.output
        assert 'does not exist' in result.output
        self._assert_no_data_dir(empty_dir)
