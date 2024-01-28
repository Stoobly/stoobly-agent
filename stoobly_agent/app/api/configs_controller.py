import pdb

from mergedeep import merge

from stoobly_agent.app.api.simple_http_request_handler import SimpleHTTPRequestHandler
from stoobly_agent.app.cli.helpers.handle_config_update_service import (
    context as handle_context, handle_intercept_active_update, handle_policy_update, handle_project_update, handle_scenario_update
) 
from stoobly_agent.app.models.scenario_model import ScenarioModel
from stoobly_agent.app.proxy.intercept_settings import InterceptSettings
from stoobly_agent.app.settings import Settings
from stoobly_agent.config.constants import mock_policy, mode, record_policy, replay_policy
from stoobly_agent.lib.api.keys.project_key import InvalidProjectKey, ProjectKey
from stoobly_agent.lib.api.keys.scenario_key import ScenarioKey

class ConfigsController:
    _instance = None

    def __init__(self):
        if self._instance:
            raise RuntimeError('Call instance() instead')
        else:
            self.data = {}

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    # GET /configs/policies
    def policies(self, context):
        settings = Settings.instance()
        active_mode = settings.proxy.intercept.active

        if active_mode in [mode.MOCK, mode.TEST]:
            context.render(
                json = [mock_policy.ALL, mock_policy.FOUND],
                status = 200
            )
        elif active_mode == mode.RECORD:
            context.render(
                json = [record_policy.ALL, record_policy.FOUND, record_policy.NOT_FOUND, record_policy.OVERWRITE],
                status = 200
            )
        elif active_mode == mode.REPLAY:
            context.render(
                json = [replay_policy.ALL],
                status = 200
            )

    # GET /configs
    def show(self, context):
        settings = Settings.instance()

        context.render(
            json = settings.to_dict(),
            status = 200
        )

    # GET /configs/summary
    def summary(self, context):
        settings = Settings.instance()
        proxy = settings.proxy
        intercept_settings = InterceptSettings(settings)

        project_key = intercept_settings.project_key
        project_id = ProjectKey(project_key).id if project_key else None
                
        scenario_key = intercept_settings.scenario_key
        scenario_id = None

        # Check to make sure the scenario still exists
        scenario_uuid = ScenarioKey(scenario_key).id if scenario_key else None

        if scenario_uuid:
            model = self.__scenario_model(settings)
            scenario, status = model.show(scenario_uuid)

            if status == 404:
                intercept_settings.scenario_key = None
                settings.commit()
            elif status == 200:
                scenario_id = scenario['id']

        remote_project_id = self.__remote_project_id(settings)

        modes = [mode.RECORD, mode.MOCK, mode.TEST, mode.REPLAY] if not context.params.get('agent') else [mode.RECORD, mode.MOCK, mode.REPLAY]

        context.render(
            json = {
                'active': intercept_settings.active,
                'mode': intercept_settings.mode,
                'modes': modes,
                'project_id': int(project_id) if project_id != None else None,
                'proxy_url': proxy.url,
                'remote_enabled': settings.cli.features.remote,
                'remote_project_id': remote_project_id,
                'scenario_id': int(scenario_id) if scenario_id != None else None,
            },
            status = 200
        )

    # PUT /configs
    def update(self, context):
        settings = Settings.instance()

        merged_settings = merge(settings.to_dict(), context.params)
        settings.from_dict(merged_settings)

        _handle_context = handle_context()

        handle_intercept_active_update(settings, _handle_context)
        handle_policy_update(settings, _handle_context)
        handle_project_update(settings, _handle_context)
        handle_scenario_update(settings, _handle_context)

        settings.write(settings.to_dict())

        context.render(
            json = merged_settings,
            status = 200
        )

    def __remote_project_id(self, settings: Settings):
        remote_project_key = settings.remote.project_key

        try:
            return ProjectKey(remote_project_key).id if remote_project_key else None
        except InvalidProjectKey:
            pass

    def __scenario_model(self, settings: Settings = None):
        scenario_model = ScenarioModel(settings or Settings.instance())
        return scenario_model