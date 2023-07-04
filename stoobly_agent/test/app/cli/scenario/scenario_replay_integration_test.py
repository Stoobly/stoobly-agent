import json
import pdb
import pytest

from click.testing import CliRunner
from mock import patch
from typing import Tuple
from unittest.mock import MagicMock

from stoobly_agent.test.test_helper import DETERMINISTIC_GET_REQUEST_URL, reset

from stoobly_agent.cli import record, scenario
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
        def replay_spy(self, runner: CliRunner, created_scenario: Scenario):
            with patch('stoobly_agent.app.proxy.replay.replay_request_service.replay') as test_patch:
                replay_result = runner.invoke(scenario, ['replay', created_scenario.key()])
                assert replay_result.exit_code == 0
                return test_patch

        @pytest.fixture(scope='class')
        def replay_options(self, replay_spy: MagicMock) -> ReplayRequestOptions:
            return replay_spy.call_args.args[1]
            
        def test_it_called_twice(self, replay_spy: MagicMock):
            assert replay_spy.call_count == 2

        def test_options_has_project_key(self, replay_options: ReplayRequestOptions):
            assert replay_options.get('project_key') is not None

        def test_options_not_has_scenario_key(self, replay_options: ReplayRequestOptions):
            assert replay_options.get('scenario_key') is None

    class TestWhenRecord():

        class TestWhenScenario():
            @pytest.fixture(scope='class', autouse=True)
            def settings(self):
                return reset()

            @pytest.fixture(scope='class')
            def source_scenario(self, runner: CliRunner):
                create_result = runner.invoke(scenario, ['create', 'test'])
                assert create_result.exit_code == 0
                return Scenario.last()

            @pytest.fixture(scope='class')
            def destination_scenario(self, runner: CliRunner):
                create_result = runner.invoke(scenario, ['create', 'test'])
                assert create_result.exit_code == 0
                return Scenario.last()

            @pytest.fixture(scope='class', autouse=True)
            def recorded_request(self, runner: CliRunner, source_scenario: Scenario):
                record_result = runner.invoke(record, ['--scenario-key', source_scenario.key(), DETERMINISTIC_GET_REQUEST_URL])
                assert record_result.exit_code == 0
                return Request.last()

            @pytest.fixture(scope='class')
            def spies(self, runner: CliRunner, source_scenario: Scenario, destination_scenario: Scenario):
                @patch.object(LocalDBRequestAdapter, 'create', wraps=LocalDBRequestAdapter(Request, Response).create)
                @patch('stoobly_agent.app.proxy.record.upload_request_service.upload_request', wraps=upload_request)
                @patch('stoobly_agent.app.proxy.replay.replay_request_service.replay', wraps=replay)
                def spy_on(replay_spy: MagicMock, upload_request_spy: MagicMock, create_spy: MagicMock):
                    replay_result = runner.invoke(scenario, ['replay', '--record' , '--scenario-key', destination_scenario.key(), source_scenario.key()])
                    assert replay_result.exit_code == 0
                    return replay_spy, upload_request_spy, create_spy

                return spy_on()

            @pytest.fixture(scope='class')
            def replay_spy(self, spies: Tuple[MagicMock]):
                return spies[0]

            @pytest.fixture(scope='class')
            def replay_options(self, replay_spy: MagicMock) -> ReplayRequestOptions:
                return replay_spy.call_args.args[1]

            @pytest.fixture(scope='class')
            def upload_request_spy(self, spies: Tuple[MagicMock]):
                return spies[1]

            @pytest.fixture(scope='class')
            def upload_request_intercept_settings(self, upload_request_spy: MagicMock):
                return upload_request_spy.call_args.args[1]

            @pytest.fixture(scope='class')
            def create_spy(self, spies: Tuple[MagicMock]):
                return spies[2]

            @pytest.fixture(scope='class')
            def create_kwargs(self, create_spy: MagicMock):
                return create_spy.call_args.kwargs

            def test_replay_called_once(self, replay_spy: MagicMock):
                replay_spy.assert_called_once()

            def test_options_has_project_key(self, replay_options: ReplayRequestOptions):
                assert replay_options.get('project_key') is not None

            def test_options_not_has_scenario_key(self, replay_options: ReplayRequestOptions, destination_scenario: Scenario):
                assert replay_options.get('scenario_key') == destination_scenario.key()

            def test_upload_request_called_once(self, upload_request_spy: MagicMock):
                upload_request_spy.assert_called_once()

            def test_upload_request_called_with_destination_scenario_key(self, upload_request_intercept_settings, destination_scenario: Scenario):
                assert upload_request_intercept_settings.scenario_key == destination_scenario.key()

            def test_create_called_once(self, create_spy: MagicMock):
                create_spy.assert_called_once()

            def test_create_called_with_destination_scenario_id(self, create_kwargs, destination_scenario: Scenario):
                assert create_kwargs['scenario_id'] == destination_scenario.uuid
