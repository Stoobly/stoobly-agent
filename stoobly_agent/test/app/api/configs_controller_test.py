import uuid
import pytest
from unittest.mock import MagicMock, patch

from stoobly_agent.test.test_helper import reset
from stoobly_agent.app.api.configs_controller import ConfigsController
from stoobly_agent.config.constants import mock_policy, mode, record_policy, replay_policy, test_policy
from stoobly_agent.lib.api.keys.project_key import ProjectKey
from stoobly_agent.lib.api.keys.scenario_key import ScenarioKey

@pytest.fixture(scope='class')
def settings():
    return reset()

@pytest.fixture
def controller():
    ConfigsController._instance = None
    return ConfigsController.instance()

@pytest.fixture
def mock_context():
    context = MagicMock()
    context.render = MagicMock()
    context.params = {}
    return context

class TestConfigsController:

    def test_singleton_pattern(self):
        ConfigsController._instance = None

        instance1 = ConfigsController.instance()
        instance2 = ConfigsController.instance()

        assert instance1 is instance2

    def test_singleton_init_raises_error(self):
        ConfigsController._instance = None
        ConfigsController.instance()

        with pytest.raises(RuntimeError, match="Call instance\\(\\) instead"):
            ConfigsController()

    class TestPolicies:

        def test_policies_mock_mode(self, settings, controller, mock_context):
            settings.proxy.intercept.mode = mode.MOCK

            controller.policies(mock_context)

            mock_context.render.assert_called_once_with(
                json=[mock_policy.ALL, mock_policy.FOUND, mock_policy.NONE],
                status=200
            )

        def test_policies_test_mode(self, settings, controller, mock_context):
            settings.proxy.intercept.mode = mode.TEST

            controller.policies(mock_context)

            mock_context.render.assert_called_once_with(
                json=[test_policy.FOUND],
                status=200
            )

        def test_policies_record_mode(self, settings, controller, mock_context):
            settings.proxy.intercept.mode = mode.RECORD

            controller.policies(mock_context)

            mock_context.render.assert_called_once_with(
                json=[record_policy.ALL, record_policy.API, record_policy.FOUND, record_policy.NOT_FOUND],
                status=200
            )

        def test_policies_replay_mode(self, settings, controller, mock_context):
            settings.proxy.intercept.mode = mode.REPLAY

            controller.policies(mock_context)

            mock_context.render.assert_called_once_with(
                json=[replay_policy.ALL],
                status=200
            )

        def test_policies_none_mode(self, settings, controller, mock_context):
            settings.proxy.intercept.mode = mode.NONE

            controller.policies(mock_context)

            mock_context.render.assert_not_called()

    class TestShow:

        def test_show_returns_settings_dict(self, controller, mock_context):
            controller.show(mock_context)

            mock_context.render.assert_called_once()
            _, kwargs = mock_context.render.call_args
            assert kwargs['status'] == 200
            assert 'json' in kwargs

    class TestSummary:

        def test_summary_basic_configuration(self, controller, mock_context):
            mock_context.params = {}

            controller.summary(mock_context)

            mock_context.render.assert_called_once()
            _, kwargs = mock_context.render.call_args

            assert 'json' in kwargs
            assert 'status' in kwargs
            assert kwargs['status'] == 200

            response_data = kwargs['json']
            assert 'active' in response_data
            assert 'mode' in response_data
            assert 'modes' in response_data
            assert 'project_id' in response_data
            assert 'remote_enabled' in response_data
            assert 'remote_project_id' in response_data
            assert 'scenario_id' in response_data

        def test_summary_with_agent_param(self, controller, mock_context):
            mock_context.params = {'agent': True}

            controller.summary(mock_context)

            _, kwargs = mock_context.render.call_args
            response_data = kwargs['json']

            expected_modes = [mode.RECORD, mode.MOCK, mode.REPLAY]
            assert response_data['modes'] == expected_modes

        def test_summary_without_agent_param(self, controller, mock_context):
            mock_context.params = {}

            controller.summary(mock_context)

            _, kwargs = mock_context.render.call_args
            response_data = kwargs['json']

            expected_modes = [mode.RECORD, mode.MOCK, mode.TEST, mode.REPLAY]
            assert response_data['modes'] == expected_modes

        @patch('stoobly_agent.app.api.configs_controller.ScenarioModel')
        def test_summary_with_invalid_scenario(self, mock_scenario_model_class, settings, controller, mock_context):
            mock_model = MagicMock()
            mock_model.show.return_value = (None, 404)
            mock_scenario_model_class.return_value = mock_model

            project_id = ProjectKey(settings.proxy.intercept.project_key).id
            valid_key = ScenarioKey.encode(project_id, str(uuid.uuid4()))
            settings.proxy.data.data_rules(project_id).scenario_key = valid_key
            mock_context.params = {}

            controller.summary(mock_context)

            assert settings.proxy.data.data_rules(project_id).scenario_key is None

            _, kwargs = mock_context.render.call_args
            response_data = kwargs['json']
            assert response_data['scenario_id'] is None

        @patch('stoobly_agent.app.api.configs_controller.ScenarioModel')
        def test_summary_with_valid_scenario(self, mock_scenario_model_class, settings, controller, mock_context):
            mock_model = MagicMock()
            mock_scenario = {'id': 123}
            mock_model.show.return_value = (mock_scenario, 200)
            mock_scenario_model_class.return_value = mock_model

            project_id = ProjectKey(settings.proxy.intercept.project_key).id
            valid_key = ScenarioKey.encode(project_id, str(uuid.uuid4()))
            settings.proxy.data.data_rules(project_id).scenario_key = valid_key
            mock_context.params = {}

            controller.summary(mock_context)

            _, kwargs = mock_context.render.call_args
            response_data = kwargs['json']
            assert response_data['scenario_id'] == 123

    class TestUpdate:

        @patch('stoobly_agent.app.api.configs_controller.handle_intercept_active_update')
        @patch('stoobly_agent.app.api.configs_controller.handle_order_update')
        @patch('stoobly_agent.app.api.configs_controller.handle_strategy_update')
        @patch('stoobly_agent.app.api.configs_controller.handle_project_update')
        @patch('stoobly_agent.app.api.configs_controller.handle_scenario_update')
        def test_update_calls_all_handlers(self, mock_scenario_update, mock_project_update,
                                         mock_strategy_update, mock_order_update,
                                         mock_active_update, settings, controller, mock_context):
            mock_context.params = {'proxy': {'intercept': {'mode': mode.RECORD}}}

            controller.update(mock_context)

            mock_active_update.assert_called_once()
            mock_order_update.assert_called_once()
            mock_strategy_update.assert_called_once()
            mock_project_update.assert_called_once()
            mock_scenario_update.assert_called_once()

        def test_update_merges_settings_correctly(self, settings, controller, mock_context):
            original_mode = settings.proxy.intercept.mode
            new_mode = mode.RECORD if original_mode != mode.RECORD else mode.MOCK

            mock_context.params = {
                'proxy': {
                    'intercept': {
                        'mode': new_mode
                    }
                }
            }

            with patch.object(settings, 'write') as mock_write:
                controller.update(mock_context)

            assert settings.proxy.intercept.mode == new_mode
            mock_write.assert_called_once()
            _, kwargs = mock_context.render.call_args
            assert kwargs['status'] == 200
            assert 'json' in kwargs

        def test_update_empty_params(self, settings, controller, mock_context):
            mock_context.params = {}
            original_settings = settings.to_dict()

            with patch.object(settings, 'write') as mock_write:
                controller.update(mock_context)

            assert settings.to_dict() == original_settings
            mock_write.assert_called_once()
            _, kwargs = mock_context.render.call_args
            assert kwargs['status'] == 200

        def test_update_strips_api_url_when_remote_disabled(self, settings, controller, mock_context):
            original_remote = settings.cli.features.remote
            original_api_url = settings.remote.api_url

            try:
                settings.cli.features.remote = False
                mock_context.params = {'remote': {'api_url': 'http://malicious.example.com'}}

                with patch.object(settings, 'write'):
                    controller.update(mock_context)

                _, kwargs = mock_context.render.call_args
                assert kwargs['json']['remote']['api_url'] != 'http://malicious.example.com'
                assert kwargs['json']['remote']['api_url'] == original_api_url
            finally:
                settings.cli.features.remote = original_remote

    class TestPrivateMethods:

        def test_remote_project_id_valid_key(self, controller, settings):
            valid_key = ProjectKey.encode(123, -1)
            settings.remote.project_key = valid_key

            result = controller._ConfigsController__remote_project_id(settings)

            assert result == '123'

        def test_remote_project_id_invalid_key(self, controller, settings):
            settings.remote.project_key = 'invalid_key'

            result = controller._ConfigsController__remote_project_id(settings)

            assert result is None

        def test_remote_project_id_no_key(self, controller, settings):
            settings.remote.project_key = None

            result = controller._ConfigsController__remote_project_id(settings)

            assert result is None

        def test_scenario_model_with_settings(self, controller, settings):
            model = controller._ConfigsController__scenario_model(settings)

            assert model is not None
            assert hasattr(model, 'show')

        def test_scenario_model_without_settings(self, controller):
            model = controller._ConfigsController__scenario_model()

            assert model is not None
            assert hasattr(model, 'show')
