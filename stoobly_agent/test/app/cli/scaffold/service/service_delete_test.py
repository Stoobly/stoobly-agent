import os
import shutil
import tempfile

import pytest
from click.testing import CliRunner

from stoobly_agent.app.cli.scaffold_cli import scaffold
from stoobly_agent.app.cli.scaffold.app import App
from stoobly_agent.app.cli.scaffold.service import Service
from stoobly_agent.test.app.cli.scaffold.local.cli_invoker import LocalScaffoldCliInvoker
from stoobly_agent.test.test_helper import reset


class TestScaffoldServiceDelete:

    @pytest.fixture(scope='module', autouse=True)
    @classmethod
    def settings(cls):
        return reset()

    @pytest.fixture(scope='module')
    @classmethod
    def runner(cls):
        return CliRunner()

    @pytest.fixture(scope='class')
    @classmethod
    def temp_dir(cls):
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.fixture(scope='class')
    @classmethod
    def app_name(cls):
        return 'test-app'

    @pytest.fixture(scope='class')
    @classmethod
    def app_dir_path(cls, temp_dir, app_name):
        return os.path.join(temp_dir, app_name)

    @pytest.fixture(scope='class', autouse=True)
    @classmethod
    def create_scaffold_app(cls, runner: CliRunner, app_dir_path: str, app_name: str):
        LocalScaffoldCliInvoker.cli_app_create(runner, app_dir_path, app_name)
        yield

    class TestDeleteExistingService:

        @pytest.fixture(scope='class')
        @classmethod
        def service_name(cls):
            return 'delete-me-service'

        @pytest.fixture(scope='class', autouse=True)
        @classmethod
        def create_service(cls, runner: CliRunner, app_dir_path: str, service_name: str):
            LocalScaffoldCliInvoker.cli_service_create(runner, app_dir_path, 'delete-me.example.com', service_name, False)

        def test_delete_service(self, runner: CliRunner, app_dir_path: str, service_name: str):
            result = runner.invoke(scaffold, [
                'service', 'delete',
                '--app-dir-path', app_dir_path,
                service_name,
            ])

            assert result.exit_code == 0

            app = App(app_dir_path)
            service = Service(service_name, app)
            assert not os.path.exists(service.dir_path)

    class TestDeleteNonExistentService:

        def test_delete_nonexistent_service_is_noop(self, runner: CliRunner, app_dir_path: str):
            result = runner.invoke(scaffold, [
                'service', 'delete',
                '--app-dir-path', app_dir_path,
                'does-not-exist',
            ])

            assert result.exit_code == 0
            assert 'does not exist' in result.output
