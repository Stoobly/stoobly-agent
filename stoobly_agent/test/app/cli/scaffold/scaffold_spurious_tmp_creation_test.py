import os
import pytest

from click.testing import CliRunner

from stoobly_agent.app.cli.scaffold_cli import scaffold
from stoobly_agent.config.data_dir import DataDir, DATA_DIR_NAME
from stoobly_agent.test.app.cli.scaffold.local.cli_invoker import LocalScaffoldCliInvoker
from stoobly_agent.test.test_helper import reset


class TestScaffoldSpuriousTmpCreation:

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
        runner = CliRunner()
        app_dir = os.path.join(str(tmp_path), 'myapp')
        LocalScaffoldCliInvoker.cli_app_create(runner, app_dir, 'myapp')
        LocalScaffoldCliInvoker.cli_service_create(
            runner, app_dir, 'docs.stoobly.com', 'test-api', True
        )
        return app_dir

    def test_workflow_down_nonexistent_workflow_does_not_create_tmp_folder(self, scaffold_app):
        """Running `workflow down` for a workflow that was never started must not create the tmp dir."""
        runner = CliRunner()
        result = runner.invoke(scaffold, ['workflow', 'down', 'asdf123', '--app-dir-path', scaffold_app])

        assert result.exit_code == 1
        tmp_workflow_dir = os.path.join(scaffold_app, DATA_DIR_NAME, 'tmp', 'asdf123')
        assert not os.path.exists(tmp_workflow_dir), (
            f"`workflow down` created unexpected directory: {tmp_workflow_dir}"
        )
