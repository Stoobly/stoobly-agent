import os
import shutil
import tempfile

import pytest
from click.testing import CliRunner

from stoobly_agent.app.cli.scaffold_cli import scaffold
from stoobly_agent.app.cli.scaffold.app import App
from stoobly_agent.app.cli.scaffold.constants import SERVICES_NAMESPACE
from stoobly_agent.app.cli.scaffold.service import Service
from stoobly_agent.app.cli.scaffold.service_config import ServiceConfig
from stoobly_agent.test.app.cli.scaffold.local.cli_invoker import LocalScaffoldCliInvoker
from stoobly_agent.test.test_helper import reset


class TestScaffoldServiceUpdate:

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
        return "test-app"

    @pytest.fixture(scope='class')
    def app_dir_path(self, temp_dir, app_name):
        return os.path.join(temp_dir, app_name)

    @pytest.fixture(scope='class', autouse=True)
    def create_scaffold_app(self, runner: CliRunner, app_dir_path: str, app_name: str):
        LocalScaffoldCliInvoker.cli_app_create(runner, app_dir_path, app_name)
        yield

    class TestUpdateHostname:

        @pytest.fixture(scope='class')
        def service_name(self):
            return 'hostname-update-service'

        @pytest.fixture(scope='class')
        def initial_hostname(self):
            return 'initial.example.com'

        @pytest.fixture(scope='class')
        def updated_hostname(self):
            return 'updated.example.com'

        @pytest.fixture(scope='class', autouse=True)
        def create_service(self, runner: CliRunner, app_dir_path: str, service_name: str, initial_hostname: str):
            LocalScaffoldCliInvoker.cli_service_create(runner, app_dir_path, initial_hostname, service_name, True)

        def test_update_hostname(self, runner: CliRunner, app_dir_path: str, service_name: str, initial_hostname: str, updated_hostname: str):
            result = runner.invoke(scaffold, [
                'service', 'update',
                '--app-dir-path', app_dir_path,
                '--hostname', updated_hostname,
                service_name
            ])
            assert result.exit_code == 0

            app = App(app_dir_path, SERVICES_NAMESPACE)
            service = Service(service_name, app)
            service_config = ServiceConfig(service.dir_path)
            assert service_config.hostname != initial_hostname
            assert service_config.hostname == updated_hostname

    class TestUpdatePort:

        @pytest.fixture(scope='class')
        def service_name(self):
            return 'port-update-service'

        @pytest.fixture(scope='class')
        def hostname(self):
            return 'port-test.example.com'

        @pytest.fixture(scope='class')
        def updated_port(self):
            return 9090

        @pytest.fixture(scope='class', autouse=True)
        def create_service(self, runner: CliRunner, app_dir_path: str, service_name: str, hostname: str):
            LocalScaffoldCliInvoker.cli_service_create(runner, app_dir_path, hostname, service_name, False)

        def test_update_port(self, runner: CliRunner, app_dir_path: str, service_name: str, updated_port: int):
            result = runner.invoke(scaffold, [
                'service', 'update',
                '--app-dir-path', app_dir_path,
                '--port', str(updated_port),
                service_name
            ])
            assert result.exit_code == 0

            app = App(app_dir_path, SERVICES_NAMESPACE)
            service = Service(service_name, app)
            service_config = ServiceConfig(service.dir_path)
            assert service_config.port != 80
            assert service_config.port == updated_port

    class TestUpdateName:

        @pytest.fixture(scope='class')
        def service_name(self):
            return 'name-update-service'

        @pytest.fixture(scope='class')
        def hostname(self):
            return 'name-test.example.com'

        @pytest.fixture(scope='class')
        def new_service_name(self):
            return 'renamed-service'

        @pytest.fixture(scope='class', autouse=True)
        def create_service(self, runner: CliRunner, app_dir_path: str, service_name: str, hostname: str):
            LocalScaffoldCliInvoker.cli_service_create(runner, app_dir_path, hostname, service_name, True)

        def test_update_name(self, runner: CliRunner, app_dir_path: str, service_name: str, new_service_name: str):
            result = runner.invoke(scaffold, [
                'service', 'update',
                '--app-dir-path', app_dir_path,
                '--name', new_service_name,
                service_name
            ])
            assert result.exit_code == 0

            app = App(app_dir_path, SERVICES_NAMESPACE)
            old_service = Service(service_name, app)
            new_service = Service(new_service_name, app)

            assert not os.path.exists(old_service.dir_path)
            assert os.path.exists(new_service.dir_path)

            service_config = ServiceConfig(new_service.dir_path)
            assert service_config.name != service_name
            assert service_config.name == new_service_name
