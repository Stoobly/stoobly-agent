import os
import pdb
import pytest

from click.testing import CliRunner
from mock import patch
from unittest.mock import MagicMock

from stoobly_agent.test.test_helper import DETERMINISTIC_GET_REQUEST_URL, reset

# Enable remote feature
from stoobly_agent.config.constants import env_vars, test_strategy
os.environ[env_vars.FEATURE_REMOTE] = '1'

from stoobly_agent.cli import record, scenario
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.lib.orm.scenario import Scenario

@pytest.fixture(scope='module')
def runner():
    return CliRunner()

class TestScenarioTestIntegration():
    @pytest.fixture(scope='class', autouse=True)
    def settings(self):
        return reset()

    class TestWhenDiffTest():
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

        @pytest.fixture(scope='class')
        def diff_matches(self, runner: CliRunner, created_scenario: Scenario):
            with patch('stoobly_agent.app.proxy.test.test_service.diff_matches') as spy:
                spy.return_value = (True, '')
                test_result = runner.invoke(scenario, ['test', created_scenario.key()])
                assert test_result.exit_code == 0

                return spy

        def test_it_calls_diff_matches_once(self, diff_matches: MagicMock):
            assert diff_matches.call_count == 1

    class TestWhenFuzzyTest():
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

        @pytest.fixture(scope='class')
        def fuzzy_matches(self, runner: CliRunner, created_scenario: Scenario):
            with patch('stoobly_agent.app.proxy.test.test_service.fuzzy_matches') as spy:
                spy.return_value = (True, '')
                test_result = runner.invoke(scenario, ['test', '--strategy', test_strategy.FUZZY, created_scenario.key()])
                assert test_result.exit_code == 0

                return spy

        def test_it_calls_fuzzy_matches_once(self, fuzzy_matches: MagicMock):
            assert fuzzy_matches.call_count == 1

    class TestWhenCustomTest():
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

        @pytest.fixture(scope='class')
        def custom_matches(self, runner: CliRunner, created_scenario: Scenario):
            with patch('stoobly_agent.app.proxy.test.test_service.custom_matches') as spy:
                spy.return_value = (True, '')
                test_result = runner.invoke(scenario, ['test', '--strategy', test_strategy.CUSTOM, created_scenario.key()])
                assert test_result.exit_code == 0

                return spy

        def test_it_calls_custom_matches_once(self, custom_matches: MagicMock):
            assert custom_matches.call_count == 1

    class TestWhenContractTest():
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

        @pytest.fixture(scope='class')
        def contract_matches(self, runner: CliRunner, created_scenario: Scenario):
            with patch('stoobly_agent.app.proxy.test.test_service.contract_matches') as spy:
                spy.return_value = (True, '')
                test_result = runner.invoke(scenario, ['test', '--strategy', test_strategy.CONTRACT, created_scenario.key()])
                assert test_result.exit_code == 0

                return spy

        def test_it_calls_contraact_matches_once(self, contract_matches: MagicMock):
            assert contract_matches.call_count == 1