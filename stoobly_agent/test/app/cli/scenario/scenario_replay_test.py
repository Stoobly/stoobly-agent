import json
import pdb
import pytest

from click.testing import CliRunner
from typing import List

from stoobly_agent.test.test_helper import DETERMINISTIC_GET_REQUEST_URL, reset

from stoobly_agent.app.cli.helpers.handle_replay_service import JSON_FORMAT
from stoobly_agent.app.models.adapters.raw_http_response_adapter import RawHttpResponseAdapter
from stoobly_agent.app.cli.types.output import ReplayOutput
from stoobly_agent.cli import record, scenario
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.lib.orm.scenario import Scenario
from stoobly_agent.lib.utils.decode import decode

@pytest.fixture(scope='module')
def runner():
    return CliRunner()

class TestReplay():
    @pytest.fixture(scope='class', autouse=True)
    def settings(self):
        return reset()

    class TestWhenNoOptions():

        @pytest.fixture(scope='class')
        def created_scenario(self, runner: CliRunner):
            create_result = runner.invoke(scenario, ['create', 'test'])
            assert create_result.exit_code == 0
            return Scenario.last()

        @pytest.fixture(scope='class')
        def recorded_request(self, runner: CliRunner, created_scenario: Scenario):
            record_result = runner.invoke(record, ['--scenario-key', created_scenario.key(), DETERMINISTIC_GET_REQUEST_URL])
            assert record_result.exit_code == 0
            return Request.last()

        @pytest.fixture(scope='class')
        def recorded_response_raw(self, recorded_request: Request):
            return recorded_request.response.raw
            
        def test_it_matches_recorded_response(self, runner, created_scenario: Scenario, recorded_response_raw: bytes):
            replay_result = runner.invoke(scenario, ['replay', '--format', JSON_FORMAT, created_scenario.key()])
            assert replay_result.exit_code == 0

            try:
                replay_outputs: List[ReplayOutput] = json.loads(replay_result.stdout)
            except Exception:
                assert False, 'Invalid JSON output'
            
            replay_output = replay_outputs[0]
            assert not not replay_output.get('content')

            response = RawHttpResponseAdapter(recorded_response_raw).to_response()
            assert replay_output['content']  == decode(response.content)


        def test_it_does_not_override_response_raw(self, recorded_request: Request, recorded_response_raw: bytes):
            new_response = Request.find(recorded_request.id).response.raw
            assert new_response == recorded_response_raw

    class TestWhenOverwritting():

        @pytest.fixture(scope='class')
        def created_scenario(self, runner: CliRunner):
            create_result = runner.invoke(scenario, ['create', 'test'])
            assert create_result.exit_code == 0
            return Scenario.last()

        @pytest.fixture(scope='class')
        def recorded_request(self, runner: CliRunner, created_scenario: Scenario):
            record_result = runner.invoke(record, ['--scenario-key', created_scenario.key(), DETERMINISTIC_GET_REQUEST_URL])
            assert record_result.exit_code == 0
            return Request.last()

        @pytest.fixture(scope='class')
        def recorded_response_raw(self, recorded_request: Request):
            return recorded_request.response.raw

        def test_it_overwrites_response_raw(self, runner: CliRunner, created_scenario: Scenario, recorded_request: Request, recorded_response_raw: bytes):
            replay_result = runner.invoke(scenario, ['replay', '--overwrite', created_scenario.key()])
            assert replay_result.exit_code == 0

            new_response = Request.find(recorded_request.id).response.raw
            assert new_response != recorded_response_raw

        def test_it_creates_one_replayed_response(self, recorded_request: Request):
            assert len(recorded_request.replayed_responses) == 1

        def test_it_sets_replayed_response_raw_to_response_raw(self, recorded_request: Request, recorded_response_raw: bytes):
            replayed_response = recorded_request.replayed_responses[0]
            assert replayed_response.raw == recorded_response_raw

    class TestWhenRecord():

        @pytest.fixture(scope='class')
        def created_scenario(self, runner: CliRunner):
            create_result = runner.invoke(scenario, ['create', 'test'])
            assert create_result.exit_code == 0
            return Scenario.last()

        @pytest.fixture(scope='class', autouse=True)
        def recorded_request(self, runner: CliRunner, created_scenario: Scenario):
            record_result = runner.invoke(record, ['--scenario-key', created_scenario.key(), DETERMINISTIC_GET_REQUEST_URL])
            assert record_result.exit_code == 0
            return Request.last()

        def test_it_records(self, runner: CliRunner, created_scenario: Scenario):
            replay_result = runner.invoke(scenario, ['replay', '--record', created_scenario.key()])
            assert replay_result.exit_code == 0

            assert Request.count() == 2

            _scenario = Scenario.find(created_scenario.id)
            assert _scenario.requests.count() == 1

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

            def test_it_records_to_scenario(self, runner: CliRunner, source_scenario: Scenario, destination_scenario: Scenario):
                replay_result = runner.invoke(scenario, ['replay', '--record' , '--scenario-key', destination_scenario.key(), source_scenario.key()])
                assert replay_result.exit_code == 0

                assert Request.count() == 2

                _scenario = Scenario.find(source_scenario.id)
                assert _scenario.requests.count() == 1

                _scenario = Scenario.find(destination_scenario.id)
                assert _scenario.requests.count() == 1