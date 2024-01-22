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