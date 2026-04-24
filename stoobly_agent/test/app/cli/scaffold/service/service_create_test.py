import os
import shutil
import tempfile

import pytest
from click.testing import CliRunner

from stoobly_agent.app.cli.scaffold_cli import scaffold
from stoobly_agent.app.cli.scaffold.app import App
from stoobly_agent.app.cli.scaffold.constants import (
    OPENAPI_SPECIFICATION_FILE_NAME,
    WORKFLOW_MOCK_TYPE,
    WORKFLOW_RECORD_TYPE,
    WORKFLOW_TEST_TYPE,
)
from stoobly_agent.app.cli.scaffold.service import Service
from stoobly_agent.app.cli.scaffold.service_config import ServiceConfig
from stoobly_agent.test.app.cli.scaffold.local.cli_invoker import LocalScaffoldCliInvoker
from stoobly_agent.test.test_helper import reset


class TestScaffoldServiceCreate:

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

    class TestCreateBasicService:

        @pytest.fixture(scope='class')
        def service_name(self):
            return 'basic-service'

        def test_create_basic_service(self, runner: CliRunner, app_dir_path: str, service_name: str):
            result = runner.invoke(scaffold, [
                'service', 'create',
                '--app-dir-path', app_dir_path,
                '--quiet',
                service_name,
            ])

            assert result.exit_code == 0

            app = App(app_dir_path)
            service = Service(service_name, app)
            assert os.path.exists(service.dir_path)

    class TestCreateWithHostname:

        @pytest.fixture(scope='class')
        def service_name(self):
            return 'hostname-service'

        @pytest.fixture(scope='class')
        def hostname(self):
            return 'example.com'

        @pytest.fixture(scope='class', autouse=True)
        def create_service(self, runner: CliRunner, app_dir_path: str, service_name: str, hostname: str):
            result = runner.invoke(scaffold, [
                'service', 'create',
                '--app-dir-path', app_dir_path,
                '--hostname', hostname,
                '--quiet',
                service_name,
            ])
            assert result.exit_code == 0

        def test_hostname_is_set(self, app_dir_path: str, service_name: str, hostname: str):
            app = App(app_dir_path)
            service = Service(service_name, app)
            service_config = ServiceConfig(service.dir_path)
            assert service_config.hostname == hostname

    class TestCreateWithPort:

        @pytest.fixture(scope='class')
        def service_name(self):
            return 'port-service'

        @pytest.fixture(scope='class')
        def port(self):
            return 8080

        @pytest.fixture(scope='class', autouse=True)
        def create_service(self, runner: CliRunner, app_dir_path: str, service_name: str, port: int):
            result = runner.invoke(scaffold, [
                'service', 'create',
                '--app-dir-path', app_dir_path,
                '--port', str(port),
                '--quiet',
                service_name,
            ])
            assert result.exit_code == 0

        def test_port_is_set(self, app_dir_path: str, service_name: str, port: int):
            app = App(app_dir_path)
            service = Service(service_name, app)
            service_config = ServiceConfig(service.dir_path)
            assert service_config.port == port

    class TestCreateWithScheme:

        @pytest.fixture(scope='class')
        def service_name(self):
            return 'scheme-service'

        @pytest.fixture(scope='class')
        def scheme(self):
            return 'https'

        @pytest.fixture(scope='class', autouse=True)
        def create_service(self, runner: CliRunner, app_dir_path: str, service_name: str, scheme: str):
            result = runner.invoke(scaffold, [
                'service', 'create',
                '--app-dir-path', app_dir_path,
                '--scheme', scheme,
                '--quiet',
                service_name,
            ])
            assert result.exit_code == 0

        def test_scheme_is_set(self, app_dir_path: str, service_name: str, scheme: str):
            app = App(app_dir_path)
            service = Service(service_name, app)
            service_config = ServiceConfig(service.dir_path)
            assert service_config.scheme == scheme

    class TestCreateWithOpenapiSpecification:

        @pytest.fixture(scope='class')
        def service_name(self):
            return 'openapi-spec-service'

        @pytest.fixture(scope='class')
        @pytest.fixture(scope='class', autouse=True)
        def create_service(self, runner: CliRunner, app_dir_path: str, service_name: str):
            result = runner.invoke(scaffold, [
                'service', 'create',
                '--app-dir-path', app_dir_path,
                '--openapi-specification',
                '--quiet',
                service_name,
            ])
            assert result.exit_code == 0

        def test_openapi_specification_is_set(self, app_dir_path: str, service_name: str):
            app = App(app_dir_path)
            service = Service(service_name, app)
            service_config = ServiceConfig(service.dir_path)
            assert service_config.openapi_specification is True

        def test_openapi_specification_file_is_created(self, app_dir_path: str, service_name: str):
            app = App(app_dir_path)
            service = Service(service_name, app)
            openapi_specification_path = os.path.join(service.dir_path, OPENAPI_SPECIFICATION_FILE_NAME)
            assert os.path.exists(openapi_specification_path)

    class TestCreateWithSingleWorkflow:

        @pytest.fixture(scope='class')
        def service_name(self):
            return 'workflow-service'

        @pytest.fixture(scope='class', autouse=True)
        def create_service(self, runner: CliRunner, app_dir_path: str, service_name: str):
            result = runner.invoke(scaffold, [
                'service', 'create',
                '--app-dir-path', app_dir_path,
                '--workflow', WORKFLOW_MOCK_TYPE,
                '--quiet',
                service_name,
            ])
            assert result.exit_code == 0

        def test_workflow_dir_exists(self, app_dir_path: str, service_name: str):
            app = App(app_dir_path)
            service = Service(service_name, app)
            assert os.path.exists(service.workflow_dir_path(WORKFLOW_MOCK_TYPE))

    class TestCreateWithMultipleWorkflows:

        @pytest.fixture(scope='class')
        def service_name(self):
            return 'multi-workflow-service'

        @pytest.fixture(scope='class', autouse=True)
        def create_service(self, runner: CliRunner, app_dir_path: str, service_name: str):
            result = runner.invoke(scaffold, [
                'service', 'create',
                '--app-dir-path', app_dir_path,
                '--workflow', WORKFLOW_MOCK_TYPE,
                '--workflow', WORKFLOW_RECORD_TYPE,
                '--workflow', WORKFLOW_TEST_TYPE,
                '--quiet',
                service_name,
            ])
            assert result.exit_code == 0

        def test_all_workflow_dirs_exist(self, app_dir_path: str, service_name: str):
            app = App(app_dir_path)
            service = Service(service_name, app)
            for workflow in [WORKFLOW_MOCK_TYPE, WORKFLOW_RECORD_TYPE, WORKFLOW_TEST_TYPE]:
                assert os.path.exists(service.workflow_dir_path(workflow))

    class TestCreateInvalidCases:

        def test_invalid_port_fails(self, runner: CliRunner, app_dir_path: str):
            result = runner.invoke(scaffold, [
                'service', 'create',
                '--app-dir-path', app_dir_path,
                '--port', '70000',
                'invalid-port-service',
            ])
            assert result.exit_code != 0

        def test_invalid_scheme_fails(self, runner: CliRunner, app_dir_path: str):
            result = runner.invoke(scaffold, [
                'service', 'create',
                '--app-dir-path', app_dir_path,
                '--scheme', 'ftp',
                'invalid-scheme-service',
            ])
            assert result.exit_code != 0

        def test_invalid_workflow_fails(self, runner: CliRunner, app_dir_path: str):
            result = runner.invoke(scaffold, [
                'service', 'create',
                '--app-dir-path', app_dir_path,
                '--workflow', 'invalid-workflow',
                'invalid-workflow-service',
            ])
            assert result.exit_code != 0
