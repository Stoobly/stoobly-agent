import json
import pdb
import pytest

from click.testing import CliRunner

from stoobly_agent.test.test_helper import DETERMINISTIC_GET_REQUEST_URL, reset

from stoobly_agent.cli import record, request
from stoobly_agent.config.constants import test_output_level, test_strategy
from stoobly_agent.lib.orm.request import Request

@pytest.fixture(scope='module')
def runner():
    return CliRunner()

class TestReplay():
    @pytest.fixture(scope='class', autouse=True)
    def settings(self):
        return reset()

    class TestWhenDiffStrategy():

        @pytest.fixture(scope='class')
        def recorded_request(self, runner: CliRunner):
            record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
            assert record_result.exit_code == 0
            return Request.last()

        def test_it_matches(self, runner, recorded_request: Request):
            replay_result = runner.invoke(request, ['test', '--strategy', test_strategy.DIFF, recorded_request.key()])
            assert replay_result.exit_code == 0

    class TestWhenContractStrategy():

        @pytest.fixture(scope='class')
        def recorded_request(self, runner: CliRunner):
            record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
            assert record_result.exit_code == 0
            return Request.last()

        def test_it_matches(self, runner, recorded_request: Request):
            replay_result = runner.invoke(request, ['test', '--strategy', test_strategy.CONTRACT, recorded_request.key()])
            assert replay_result.exit_code == 0

    class TestWhenFuzzyStrategy():

        @pytest.fixture(scope='class')
        def recorded_request(self, runner: CliRunner):
            record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
            assert record_result.exit_code == 0
            return Request.last()

        def test_it_matches(self, runner, recorded_request: Request):
            replay_result = runner.invoke(request, ['test', '--strategy', test_strategy.FUZZY, recorded_request.key()])
            assert replay_result.exit_code == 0

    class TestWhenJson():

        @pytest.fixture(scope='class')
        def recorded_request(self, runner: CliRunner):
            record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
            assert record_result.exit_code == 0
            return Request.last()
        
        @pytest.fixture(scope='class')
        def tests_output(self, runner: CliRunner, recorded_request: Request):
            replay_result = runner.invoke(request, ['test', '--format', 'json', recorded_request.key()])
            assert replay_result.exit_code == 0
            return json.loads(replay_result.stdout)

        @pytest.fixture(scope='class')
        def test_output(self, tests_output):
            return tests_output['tests'][0]

        def test_it_matches(self, tests_output):
            assert tests_output['passed'] == tests_output['total']

        def test_it_has_no_expected_response(self, test_output):
            assert test_output.get('expected_response') == None

        def test_it_has_log(self, test_output):
            assert test_output.get('log') == ''

        def test_it_has_response(self, test_output):
            assert len(test_output.get('response').keys() - ['content', 'status_code', 'latency']) == 0

    class TestWhenFailedOutputLevel():

        @pytest.fixture(scope='class')
        def recorded_request(self, runner: CliRunner):
            record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
            assert record_result.exit_code == 0
            return Request.last()
        
        @pytest.fixture(scope='class')
        def test_output(self, runner: CliRunner, recorded_request: Request):
            replay_result = runner.invoke(request, ['test', '--output-level', test_output_level.FAILED, recorded_request.key()])
            assert replay_result.exit_code == 0
            return replay_result.stdout

        def test_it_has_less_output(self, runner: CliRunner, test_output: str, recorded_request: Request):
            replay_result = runner.invoke(request, ['test', recorded_request.key()])
            assert replay_result.exit_code == 0
            assert len(test_output) < len(replay_result.stdout) 

        class TestWhenJson():
            @pytest.fixture(scope='class')
            def recorded_request(self, runner: CliRunner):
                record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
                assert record_result.exit_code == 0
                return Request.last()
            
            @pytest.fixture(scope='class')
            def tests_output(self, runner, recorded_request: Request):
                replay_result = runner.invoke(request, ['test', '--output-level', test_output_level.FAILED, '--format', 'json', recorded_request.key()])
                assert replay_result.exit_code == 0
                return json.loads(replay_result.stdout)

            @pytest.fixture(scope='class')
            def test_output(self, tests_output):
                return tests_output['tests'][0]

            def test_it_has_no_expected_response(self, test_output):
                assert test_output.get('expected_response') == None

            def test_it_has_no_log(self, test_output):
                assert test_output.get('log') == None

            def test_it_has_no_response(self, test_output):
                assert test_output.get('response') == None