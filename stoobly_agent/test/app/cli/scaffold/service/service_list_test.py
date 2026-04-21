import os
import shutil
import tempfile

import pytest
from click.testing import CliRunner

from stoobly_agent.app.cli.scaffold_cli import scaffold
from stoobly_agent.test.app.cli.scaffold.local.cli_invoker import LocalScaffoldCliInvoker
from stoobly_agent.test.test_helper import reset


class TestScaffoldServiceList:

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

    @pytest.fixture(scope='class')
    def service_name_1(self):
        return 'list-service-one'

    @pytest.fixture(scope='class')
    def service_name_2(self):
        return 'list-service-two'

    @pytest.fixture(scope='class', autouse=True)
    def create_scaffold_app(self, runner: CliRunner, app_dir_path: str, app_name: str, service_name_1: str, service_name_2: str):
        LocalScaffoldCliInvoker.cli_app_create(runner, app_dir_path, app_name)
        LocalScaffoldCliInvoker.cli_service_create(runner, app_dir_path, 'service-one.example.com', service_name_1, False)
        LocalScaffoldCliInvoker.cli_service_create(runner, app_dir_path, 'service-two.example.com', service_name_2, False)
        yield

    class TestListAll:

        def test_list_returns_all_services(self, runner: CliRunner, app_dir_path: str, service_name_1: str, service_name_2: str):
            result = runner.invoke(scaffold, [
                'service', 'list',
                '--app-dir-path', app_dir_path,
            ])

            assert result.exit_code == 0
            assert service_name_1 in result.output
            assert service_name_2 in result.output

    class TestListWithFilter:

        def test_list_filters_by_service_name(self, runner: CliRunner, app_dir_path: str, service_name_1: str, service_name_2: str):
            result = runner.invoke(scaffold, [
                'service', 'list',
                '--app-dir-path', app_dir_path,
                '--service', service_name_1,
            ])

            assert result.exit_code == 0
            assert service_name_1 in result.output
            assert service_name_2 not in result.output
