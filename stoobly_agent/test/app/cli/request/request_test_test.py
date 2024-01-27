import pdb
import pytest

from click.testing import CliRunner

from stoobly_agent.test.test_helper import DETERMINISTIC_GET_REQUEST_URL, reset

from stoobly_agent.cli import record, request
from stoobly_agent.config.constants import test_strategy
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