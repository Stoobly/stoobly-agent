import pdb
import pytest

from click.testing import CliRunner

from stoobly_agent.test.test_helper import DETERMINISTIC_GET_REQUEST_URL, NON_DETERMINISTIC_GET_REQUEST_URL, reset

from stoobly_agent.app.cli.helpers.handle_replay_service import BODY_FORMAT
from stoobly_agent.app.models.adapters.raw_http_response_adapter import RawHttpResponseAdapter
from stoobly_agent.cli import record, request, scenario
from stoobly_agent.lib.api.keys.scenario_key import ScenarioKey
from stoobly_agent.lib.orm.request import Request
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
        def recorded_request(self, runner: CliRunner):
            record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
            assert record_result.exit_code == 0
            return Request.last()

        @pytest.fixture(scope='class')
        def recorded_response_raw(self, recorded_request: Request):
            return recorded_request.response.raw
            
        def test_it_matches_recorded_response(self, runner, recorded_request: Request, recorded_response_raw: bytes):
            replay_result = runner.invoke(request, ['replay', '--format', BODY_FORMAT, recorded_request.key()])
            assert replay_result.exit_code == 0

            response = RawHttpResponseAdapter(recorded_response_raw).to_response()
            assert replay_result.stdout.rstrip() == decode(response.content)

        def test_it_does_not_override_response_raw(self, recorded_request: Request, recorded_response_raw: bytes):
            new_response = Request.find(recorded_request.id).response.raw
            assert new_response == recorded_response_raw

    class TestWhenOverwritting():

        @pytest.fixture(scope='class')
        def recorded_request(self, runner: CliRunner):
            record_result = runner.invoke(record, [NON_DETERMINISTIC_GET_REQUEST_URL])
            assert record_result.exit_code == 0
            return Request.last()

        @pytest.fixture(scope='class')
        def recorded_response_raw(self, recorded_request: Request):
            return recorded_request.response.raw

        def test_it_overwrites_response_raw(self, runner: CliRunner, recorded_request: Request, recorded_response_raw: bytes):
            replay_result = runner.invoke(request, ['replay', '--overwrite', recorded_request.key()])
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
        def recorded_request(self, runner: CliRunner):
            record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
            assert record_result.exit_code == 0
            return Request.last()

        def test_it_records(self, runner: CliRunner, recorded_request: Request):
            replay_result = runner.invoke(request, ['replay', '--record', recorded_request.key()])
            assert replay_result.exit_code == 0

            assert Request.count() == 2

        class TestWhenScenario():
            @pytest.fixture(scope='class', autouse=True)
            def settings(self):
                return reset()

            @pytest.fixture(scope='class')
            def recorded_request(self, runner: CliRunner):
                record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
                assert record_result.exit_code == 0
                return Request.last()

            @pytest.fixture()
            def scenario_key(self, runner: CliRunner):
                res = runner.invoke(scenario, ['create', '--select', 'key', '--without-headers', 'test-scenario'])
                assert res.exit_code == 0
                return ScenarioKey(res.stdout.strip())

            def test_it_records_to_scenario(self, runner: CliRunner, recorded_request: Request, scenario_key: ScenarioKey):
                replay_result = runner.invoke(request, ['replay', '--record' , '--scenario-key', scenario_key.raw, recorded_request.key()])
                assert replay_result.exit_code == 0

                assert Request.count() == 2

                _request = Request.last()
                assert _request.scenario.uuid == scenario_key.id

    class TestWhenScheme():

        @pytest.fixture(scope='class')
        def recorded_request(self, runner: CliRunner):
            record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
            assert record_result.exit_code == 0
            return Request.last()

        def test_it_overrides_scheme(self, runner: CliRunner, recorded_request: Request):
            replay_result = runner.invoke(request, ['replay', '--record', '--scheme' , 'http', recorded_request.key()])
            assert replay_result.exit_code == 0

            _request = Request.last()
            assert _request.scheme == 'http'

    class TestWhenHost():

        @pytest.fixture(scope='class')
        def recorded_request(self, runner: CliRunner):
            record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
            assert record_result.exit_code == 0
            return Request.last()

        def test_it_overrides_scheme(self, runner: CliRunner, recorded_request: Request):
            host = 'www.google.com'
            replay_result = runner.invoke(request, ['replay', '--record', '--host' , host, recorded_request.key()])
            assert replay_result.exit_code == 0

            _request = Request.last()
            assert _request.host == host