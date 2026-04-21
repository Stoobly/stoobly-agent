import importlib
import os
import pytest

from click.testing import CliRunner
from mock import patch
from unittest.mock import MagicMock

from stoobly_agent.test.test_helper import DETERMINISTIC_GET_REQUEST_URL, reset

from stoobly_agent.config.constants import env_vars
import stoobly_agent.cli as cli
from stoobly_agent.lib.api.keys import ProjectKey
from stoobly_agent.lib.orm.request import Request

from stoobly_agent.app.proxy.mock.custom_not_found_response_builder import CustomNotFoundResponseBuilder
from stoobly_agent.app.proxy.mock.ignored_components_response_builder import IgnoreComponentsResponseBuilder
from stoobly_agent.app.settings import Settings
from stoobly_agent.app.settings.constants import intercept_mode, request_component
from stoobly_agent.app.settings.match_rule import MatchRule


@pytest.fixture(scope='module', autouse=True)
def _remote_cli_options():
    """Register remote-only flags on stoobly_agent.cli without leaking is_remote=True to the rest of the suite."""
    previous = os.environ.get(env_vars.FEATURE_REMOTE)
    os.environ[env_vars.FEATURE_REMOTE] = '1'
    importlib.reload(cli)
    yield
    if previous is None:
        os.environ.pop(env_vars.FEATURE_REMOTE, None)
    else:
        os.environ[env_vars.FEATURE_REMOTE] = previous
    importlib.reload(cli)


@pytest.fixture(scope='module')
def runner():
    return CliRunner()

@pytest.fixture(scope='module')
def mock():
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
                # inject_search_endpoint returns a callable; its result is used as the endpoint dict
                # for headers. A bare MagicMock breaks mitmproxy (header values must be str/bytes).
                spy.return_value = lambda method, url, **query_params: {
                    'id': '1',
                    'ignored_components': [],
                }
                mock_result = runner.invoke(mock, ['--remote-project-key', project_key.raw, DETERMINISTIC_GET_REQUEST_URL])
                assert mock_result.exit_code == 0

                return spy

        def test_it_calls_search_endpoint_once(self, search_endpoint: MagicMock):
            assert search_endpoint.call_count == 1

        def test_search_endpoint_has_project_id_call_arg(self, search_endpoint: MagicMock, project_key: ProjectKey):
            args = search_endpoint.call_args[0]
            assert len(args) == 1
            assert str(args[0]) == str(project_key.id)

    class TestWhenNotFound():
        @pytest.fixture(scope='class', autouse=True)
        def enable_match_rules(self, settings):
            # Empty proxy.match in test settings makes __filter_by_match_rules drop all hashes, so no
            # ENDPOINT_PROMISE reaches __handle_request_not_found. Enable a catch-all mock rule that
            # keeps all request components so ignored-components handling runs.
            rule = MatchRule({
                'pattern': '.*?',
                'methods': ['GET', 'POST', 'DELETE', 'OPTIONS', 'PUT'],
                'modes': [intercept_mode.MOCK],
                'components': [
                    request_component.HEADER,
                    request_component.QUERY_PARAM,
                    request_component.BODY_PARAM,
                ],
            })
            Settings.instance().proxy.match.set_match_rules('0', [rule])

        @pytest.fixture(scope='class')
        def project_key(self):
            return ProjectKey(ProjectKey.encode(1, 1))

        @pytest.fixture(scope='class')
        def spies(self, runner: CliRunner, mock, project_key: ProjectKey, enable_match_rules):
            @patch('stoobly_agent.app.proxy.mock.eval_request_service.inject_search_endpoint')
            @patch.object(
                CustomNotFoundResponseBuilder,
                'build',
                wraps=CustomNotFoundResponseBuilder.build,
            )
            @patch.object(
                IgnoreComponentsResponseBuilder,
                'build',
                wraps=IgnoreComponentsResponseBuilder.build,
            )
            def spy_on(ignore_components_build, custom_not_found_build, search_endpoint):
                search_endpoint.return_value = lambda method, url, **query_params: {
                    'id': '1',
                    'ignored_components': [],
                }
                test_result = runner.invoke(mock, ['--remote-project-key', project_key.raw, DETERMINISTIC_GET_REQUEST_URL])
                assert test_result.exit_code == 1
                return [search_endpoint, custom_not_found_build, ignore_components_build]

            return spy_on()

        @pytest.fixture(scope='class')
        def search_endpoint(self, spies):
            return spies[0]

        @pytest.fixture(scope='class')
        def custom_not_found_build(self, spies):
            return spies[1]

        @pytest.fixture(scope='class')
        def ignore_components_build(self, spies):
            return spies[2]

        def test_it_calls_custom_not_found_once(self, custom_not_found_build: MagicMock):
            assert custom_not_found_build.call_count == 1

        def test_it_does_not_call_ignore_components_when_list_empty(self, ignore_components_build: MagicMock):
            assert ignore_components_build.call_count == 0