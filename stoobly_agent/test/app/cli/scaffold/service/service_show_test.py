import os
import shutil
import tempfile

import pytest
from click.testing import CliRunner

from stoobly_agent.app.cli.scaffold_cli import scaffold
from stoobly_agent.test.app.cli.scaffold.local.cli_invoker import LocalScaffoldCliInvoker
from stoobly_agent.test.test_helper import reset


class TestScaffoldServiceShow:

    @pytest.fixture(scope='module', autouse=True)
    def settings(self):
        return reset()

    @pytest.fixture(scope='module')
    def runner(self):
        return CliRunner()

    @pytest.fixture(scope='class')
    def temp_dir(self):
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.fixture(scope='class')
    def app_name(self):
        return 'test-app'

    @pytest.fixture(scope='class')
    def app_dir_path(self, temp_dir, app_name):
        return os.path.join(temp_dir, app_name)

    @pytest.fixture(scope='class', autouse=True)
    def create_scaffold_app(self, runner: CliRunner, app_dir_path: str, app_name: str):
        LocalScaffoldCliInvoker.cli_app_create(runner, app_dir_path, app_name)
        yield

    class TestShowExistingService:

        @pytest.fixture(scope='class')
        def service_name(self):
            return 'show-service'

        @pytest.fixture(scope='class', autouse=True)
        def create_service(self, runner: CliRunner, app_dir_path: str, service_name: str):
            LocalScaffoldCliInvoker.cli_service_create(runner, app_dir_path, 'show.example.com', service_name, False)

        def test_show_service(self, runner: CliRunner, app_dir_path: str, service_name: str):
            result = runner.invoke(scaffold, [
                'service', 'show',
                '--app-dir-path', app_dir_path,
                service_name,
            ])

            assert result.exit_code == 0
            assert service_name in result.output

    class TestShowNonExistentService:

        def test_show_nonexistent_service_shows_nothing(self, runner: CliRunner, app_dir_path: str):
            result = runner.invoke(scaffold, [
                'service', 'show',
                '--app-dir-path', app_dir_path,
                'does-not-exist',
            ])

            assert result.exit_code == 0
            assert 'does-not-exist' not in result.output
