import hashlib
import os
import pytest
from unittest.mock import MagicMock, patch

from stoobly_agent.app.models.request_model import RequestModel
from stoobly_agent.app.models.scenario_model import ScenarioModel
from stoobly_agent.app.proxy.record.overwrite_scenario_service import (
    overwrite_scenario,
    overwrite_scenario_with_lock,
)
from stoobly_agent.app.settings import Settings
from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.lib.api.keys.scenario_key import ScenarioKey


@pytest.fixture
def scenario_key():
    return ScenarioKey(ScenarioKey.encode('1', '123e4567-e89b-12d3-a456-426614174000'))


@pytest.fixture
def mock_settings():
    return MagicMock(spec=Settings)


class TestOverwriteScenario:
    @pytest.fixture
    def mocks(self, mock_settings):
        with patch('stoobly_agent.app.proxy.record.overwrite_scenario_service.Settings') as MockSettings, \
             patch('stoobly_agent.app.proxy.record.overwrite_scenario_service.ScenarioModel') as MockScenarioModel, \
             patch('stoobly_agent.app.proxy.record.overwrite_scenario_service.RequestModel') as MockRequestModel:

            MockSettings.instance.return_value = mock_settings

            mock_scenario_model = MagicMock(spec=ScenarioModel)
            MockScenarioModel.return_value = mock_scenario_model

            mock_request_model = MagicMock(spec=RequestModel)
            MockRequestModel.return_value = mock_request_model

            yield {
                'settings': mock_settings,
                'scenario_model': mock_scenario_model,
                'request_model': mock_request_model,
            }

    def test_overwrites_scenario_when_overwritable(self, scenario_key, mocks):
        mocks['scenario_model'].show.return_value = ({'id': '1', 'overwritable': True}, 200)
        mocks['scenario_model'].update.return_value = ({}, 200)
        mocks['request_model'].destroy_all.return_value = ({'deleted': 5}, 200)

        result = overwrite_scenario(scenario_key)

        assert result == {'deleted': 5}
        mocks['scenario_model'].show.assert_called_once_with(scenario_key.id)
        mocks['scenario_model'].update.assert_called_once_with(scenario_key.id, overwritable=False)
        mocks['request_model'].destroy_all.assert_called_once_with(scenario_id='1')

    def test_does_nothing_when_scenario_not_overwritable(self, scenario_key, mocks):
        mocks['scenario_model'].show.return_value = ({'id': '1', 'overwritable': False}, 200)

        result = overwrite_scenario(scenario_key)

        assert result is None
        mocks['scenario_model'].show.assert_called_once_with(scenario_key.id)
        mocks['scenario_model'].update.assert_not_called()
        mocks['request_model'].destroy_all.assert_not_called()

    def test_does_nothing_when_show_fails(self, scenario_key, mocks):
        mocks['scenario_model'].show.return_value = ({'error': 'not found'}, 404)

        result = overwrite_scenario(scenario_key)

        assert result is None
        mocks['scenario_model'].show.assert_called_once_with(scenario_key.id)
        mocks['scenario_model'].update.assert_not_called()
        mocks['request_model'].destroy_all.assert_not_called()

    def test_does_nothing_when_update_to_not_overwritable_fails(self, scenario_key, mocks):
        mocks['scenario_model'].show.return_value = ({'id': '1', 'overwritable': True}, 200)
        mocks['scenario_model'].update.return_value = ({'error': 'conflict'}, 409)

        result = overwrite_scenario(scenario_key)

        assert result is None
        mocks['scenario_model'].show.assert_called_once_with(scenario_key.id)
        mocks['scenario_model'].update.assert_called_once_with(scenario_key.id, overwritable=False)
        mocks['request_model'].destroy_all.assert_not_called()

    def test_does_nothing_when_destroy_all_fails(self, scenario_key, mocks):
        mocks['scenario_model'].show.return_value = ({'id': '1', 'overwritable': True}, 200)
        mocks['scenario_model'].update.return_value = ({}, 200)
        mocks['request_model'].destroy_all.return_value = ({'error': 'forbidden'}, 403)

        result = overwrite_scenario(scenario_key)

        assert result is None
        mocks['request_model'].destroy_all.assert_called_once_with(scenario_id='1')


class TestOverwriteScenarioWithLock:
    @pytest.fixture
    def tmp_dir_path(self, tmp_path):
        return str(tmp_path)

    @pytest.fixture
    def mocks(self, mock_settings, tmp_dir_path):
        with patch('stoobly_agent.app.proxy.record.overwrite_scenario_service.Settings') as MockSettings, \
             patch('stoobly_agent.app.proxy.record.overwrite_scenario_service.ScenarioModel') as MockScenarioModel, \
             patch('stoobly_agent.app.proxy.record.overwrite_scenario_service.RequestModel') as MockRequestModel, \
             patch('stoobly_agent.app.proxy.record.overwrite_scenario_service.DataDir') as MockDataDir:

            MockSettings.instance.return_value = mock_settings

            mock_scenario_model = MagicMock(spec=ScenarioModel)
            MockScenarioModel.return_value = mock_scenario_model

            mock_request_model = MagicMock(spec=RequestModel)
            MockRequestModel.return_value = mock_request_model

            mock_data_dir = MagicMock(spec=DataDir)
            mock_data_dir.tmp_dir_path = tmp_dir_path
            MockDataDir.instance.return_value = mock_data_dir

            yield {
                'settings': mock_settings,
                'scenario_model': mock_scenario_model,
                'request_model': mock_request_model,
                'data_dir': mock_data_dir,
            }

    def test_performs_overwrite_on_first_call(self, scenario_key, mocks, tmp_dir_path):
        passed_scenario_model = MagicMock(spec=ScenarioModel)
        passed_scenario_model.update.return_value = ({}, 200)

        mocks['scenario_model'].show.return_value = ({'id': '1', 'overwritable': True}, 200)
        mocks['scenario_model'].update.return_value = ({}, 200)
        mocks['request_model'].destroy_all.return_value = ({'deleted': 3}, 200)

        overwrite_scenario_with_lock('overwrite-1', scenario_key, passed_scenario_model)

        passed_scenario_model.update.assert_called_once_with(scenario_key.id, overwritable=True)
        mocks['scenario_model'].show.assert_called_once_with(scenario_key.id)
        mocks['request_model'].destroy_all.assert_called_once_with(scenario_id='1')

        marker_file = os.path.join(tmp_dir_path, f'.{scenario_key.id}_{hashlib_sha256_prefix("overwrite-1")}.overwrite.processed')
        assert os.path.exists(marker_file)

    def test_skips_on_subsequent_call_with_same_overwrite_id(self, scenario_key, mocks, tmp_dir_path):
        passed_scenario_model = MagicMock(spec=ScenarioModel)
        passed_scenario_model.update.return_value = ({}, 200)

        mocks['scenario_model'].show.return_value = ({'id': '1', 'overwritable': True}, 200)
        mocks['scenario_model'].update.return_value = ({}, 200)
        mocks['request_model'].destroy_all.return_value = ({'deleted': 3}, 200)

        overwrite_scenario_with_lock('overwrite-1', scenario_key, passed_scenario_model)
        passed_scenario_model.reset_mock()
        mocks['scenario_model'].reset_mock()
        mocks['request_model'].reset_mock()

        overwrite_scenario_with_lock('overwrite-1', scenario_key, passed_scenario_model)

        passed_scenario_model.update.assert_not_called()
        mocks['scenario_model'].show.assert_not_called()
        mocks['request_model'].destroy_all.assert_not_called()

    def test_performs_overwrite_again_with_different_overwrite_id(self, scenario_key, mocks, tmp_dir_path):
        passed_scenario_model = MagicMock(spec=ScenarioModel)
        passed_scenario_model.update.return_value = ({}, 200)

        mocks['scenario_model'].show.return_value = ({'id': '1', 'overwritable': True}, 200)
        mocks['scenario_model'].update.return_value = ({}, 200)
        mocks['request_model'].destroy_all.return_value = ({'deleted': 3}, 200)

        overwrite_scenario_with_lock('overwrite-1', scenario_key, passed_scenario_model)

        passed_scenario_model.reset_mock()
        mocks['scenario_model'].reset_mock()
        mocks['request_model'].reset_mock()

        overwrite_scenario_with_lock('overwrite-2', scenario_key, passed_scenario_model)

        passed_scenario_model.update.assert_called_once_with(scenario_key.id, overwritable=True)
        mocks['scenario_model'].show.assert_called_once_with(scenario_key.id)
        mocks['request_model'].destroy_all.assert_called_once_with(scenario_id='1')

    def test_does_nothing_when_set_overwritable_fails(self, scenario_key, mocks, tmp_dir_path):
        passed_scenario_model = MagicMock(spec=ScenarioModel)
        passed_scenario_model.update.return_value = ({'error': 'conflict'}, 409)

        overwrite_scenario_with_lock('overwrite-1', scenario_key, passed_scenario_model)

        passed_scenario_model.update.assert_called_once_with(scenario_key.id, overwritable=True)
        mocks['scenario_model'].show.assert_not_called()
        mocks['request_model'].destroy_all.assert_not_called()

        marker_file = os.path.join(tmp_dir_path, f'.{scenario_key.id}_{hashlib_sha256_prefix("overwrite-1")}.overwrite.processed')
        assert not os.path.exists(marker_file)


def hashlib_sha256_prefix(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()[:16]
