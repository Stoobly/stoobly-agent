import json
import os
import pdb
import pytest

from click.testing import CliRunner
from mock import patch
from unittest.mock import MagicMock

from stoobly_agent.test.test_helper import DETERMINISTIC_GET_REQUEST_URL, reset

# Enable remote feature
from stoobly_agent.config.constants import env_vars
os.environ[env_vars.FEATURE_REMOTE] = '1'

from stoobly_agent.cli import record, scenario
from stoobly_agent.lib.api.keys import ProjectKey
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.lib.orm.response import Response
from stoobly_agent.lib.orm.scenario import Scenario

from stoobly_agent.app.models.factories.resource.local_db.request_adapter import LocalDBRequestAdapter
from stoobly_agent.app.proxy.replay.replay_request_service import ReplayRequestOptions, replay
from stoobly_agent.app.proxy.record.upload_request_service import upload_request

@pytest.fixture(scope='module')
def runner():
    return CliRunner()

class TestReplayIntegration():
    @pytest.fixture(scope='class', autouse=True)
    def settings(self):
        return reset()

    class TestWhenNoOptions():

        @pytest.fixture(scope='class')
        def project_key(self):
            return ProjectKey(ProjectKey.encode(1, 1))

        @pytest.fixture(scope='class')
        def created_scenario(self, runner: CliRunner):
            create_result = runner.invoke(scenario, ['create', 'test'])
            assert create_result.exit_code == 0
            return Scenario.last()

        @pytest.fixture(scope='class', autouse=True)
        def recorded_request_one(self, runner: CliRunner, created_scenario: Scenario):
            record_result = runner.invoke(record, ['--scenario-key', created_scenario.key(), DETERMINISTIC_GET_REQUEST_URL])
            assert record_result.exit_code == 0
            return Request.last()

        @pytest.fixture(scope='class', autouse=True)
        def recorded_request_two(self, runner: CliRunner, created_scenario: Scenario):
            record_result = runner.invoke(record, ['--scenario-key', created_scenario.key(), DETERMINISTIC_GET_REQUEST_URL])
            assert record_result.exit_code == 0
            return Request.last()

        @pytest.fixture(scope='class')
        def override_response_spy(self):
            with patch('stoobly_agent.app.proxy.handle_test_service.__override_response') as spy:
                return spy

        @pytest.fixture(scope='class')
        def handle_request_not_found_spy(self):
            @patch.object(LocalDBRequestAdapter, 'create', wraps=LocalDBRequestAdapter(Request, Response).create)
            def spy_on(create_spy: MagicMock):
                return create_spy

            return spy_on()

        @pytest.fixture(scope='class', autouse=True)
        def test_results(self, runner: CliRunner, project_key: ProjectKey, created_scenario: Scenario):
            test_result = runner.invoke(scenario, ['test', '--remote-project-key', project_key.raw, created_scenario.key()])
            assert test_result.exit_code == 0

        @pytest.fixture(scope='class')
        def replay_options(self, override_response_spy: MagicMock) -> ReplayRequestOptions:
            return override_response_spy.call_args.args[1]

        def test_it_calls_handle_request_not_found_spy_once(self, handle_request_not_found_spy: MagicMock):
            assert handle_request_not_found_spy.call_count == 1
            
        def test_it_called_twice(self, override_response_spy: MagicMock):
            assert override_response_spy.call_count == 1