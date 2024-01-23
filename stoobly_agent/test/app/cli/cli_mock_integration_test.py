import importlib
import os
import pdb
import pytest

from click.testing import CliRunner
from mock import patch
from unittest.mock import MagicMock

from stoobly_agent.test.test_helper import DETERMINISTIC_GET_REQUEST_URL, reset

# Enable remote feature
from stoobly_agent.config.constants import env_vars
from stoobly_agent import cli
from stoobly_agent.lib.api.keys import ProjectKey
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.lib.orm.response import Response

from stoobly_agent.app.proxy.intercept_settings import InterceptSettings
from stoobly_agent.app.models.factories.resource.local_db.request_adapter import LocalDBRequestAdapter

@pytest.fixture(scope='module')
def runner():
    return CliRunner()

@pytest.fixture(scope='module')
def mock():
    os.environ[env_vars.FEATURE_REMOTE] = '1'
    importlib.reload(cli)
    del [env_vars.FEATURE_REMOTE]
    return cli.mock

class TestCliMockIntegration():
    @pytest.fixture(scope='class', autouse=True)
    def settings(self):
        return reset()

    class TestWhenRemoteProjectKey():
        @pytest.fixture(scope='class')
        def project_key(self):
            return ProjectKey(ProjectKey.encode(1, 1))

        @pytest.fixture(scope='class', autouse=True)
        def recorded_request_one(self, runner: CliRunner):
            record_result = runner.invoke(cli.record, [DETERMINISTIC_GET_REQUEST_URL])
            assert record_result.exit_code == 0
            return Request.last()

        @pytest.fixture(scope='class')
        def search_endpoint(self, runner: CliRunner, mock, project_key: ProjectKey):
            with patch('stoobly_agent.app.proxy.mock.eval_request_service.inject_search_endpoint') as spy:
                mock_result = runner.invoke(mock, ['--remote-project-key', project_key.raw, DETERMINISTIC_GET_REQUEST_URL])
                assert mock_result.exit_code == 0

                return spy

        def test_it_calls_search_endpoint_once(self, search_endpoint: MagicMock):
            assert search_endpoint.call_count == 1

        def test_search_endpoint_has_intercept_settings_call_arg(self, search_endpoint: MagicMock):
            args = search_endpoint.call_args[0]
            assert len(args) == 1
            assert type(args[0]) is InterceptSettings

    class TestWhenNotFound():
        @pytest.fixture(scope='class')
        def project_key(self):
            return ProjectKey(ProjectKey.encode(1, 1))

        @pytest.fixture(scope='class')
        def spies(self, runner: CliRunner, mock, project_key: ProjectKey):
            @patch('stoobly_agent.app.proxy.mock.eval_request_service.inject_search_endpoint')
            @patch.object(
                LocalDBRequestAdapter,
                '_LocalDBRequestAdapter__handle_request_not_found',
                wraps=LocalDBRequestAdapter(Request, Response)._LocalDBRequestAdapter__handle_request_not_found # Mock, but preserve implementation
            )
            @patch.object(
                LocalDBRequestAdapter,
                '_LocalDBRequestAdapter__ignored_components', 
                wraps=LocalDBRequestAdapter(Request, Response)._LocalDBRequestAdapter__ignored_components
            )
            def spy_on(search_endpoint, handle_request_not_found, ignored_components: MagicMock):
                search_endpoint.return_value = lambda a, b, c: {}
                test_result = runner.invoke(mock, ['--remote-project-key', project_key.raw, DETERMINISTIC_GET_REQUEST_URL])
                assert test_result.exit_code == 1
                return [search_endpoint, handle_request_not_found, ignored_components]

            return spy_on()

        @pytest.fixture(scope='class')
        def search_endpoint(self, spies):
            return spies[2]

        @pytest.fixture(scope='class')
        def handle_request_not_found(self, spies):
            return spies[1]

        @pytest.fixture(scope='class')
        def ignored_components(self, spies):
            return spies[0]

        def test_it_calls_handle_request_not_found_spy_once(self, handle_request_not_found: MagicMock):
            assert handle_request_not_found.call_count == 1

        def test_it_calls_ignored_components_once(self, ignored_components: MagicMock):
            assert ignored_components.call_count == 1