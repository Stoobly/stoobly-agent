import pdb

from mergedeep import merge

from stoobly_agent.app.settings import Settings
from stoobly_agent.app.proxy.intercept_settings import InterceptSettings
from stoobly_agent.config.constants import mode, replay_policy
from stoobly_agent.config.constants import mock_policy, record_policy
from stoobly_agent.lib.api.interfaces.scenarios import ScenarioShowResponse
from stoobly_agent.lib.api.keys.project_key import ProjectKey
from stoobly_agent.lib.api.keys.scenario_key import ScenarioKey
from stoobly_agent.lib.api.scenarios_resource import ScenariosResource

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

    # GET /api/v1/admin/configs/policies
    def get_configs_policies(self, context):
        settings = Settings.instance()
        active_mode = settings.proxy.intercept.active

        if active_mode in [mode.MOCK, mode.TEST]:
            context.render(
                json = [mock_policy.ALL, mock_policy.FOUND],
                status = 200
            )
        elif active_mode == mode.RECORD:
            context.render(
                json = [record_policy.ALL, record_policy.FOUND, record_policy.NOT_FOUND],
                status = 200
            )
        elif active_mode == mode.REPLAY:
            context.render(
                json = [replay_policy.ALL],
                status = 200
            )

    # GET /api/v1/admin/configs
    def get_configs(self, context):
        settings = Settings.instance()

        context.render(
            json = settings.to_dict(),
            status = 200
        )

    # GET /api/v1/admin/configs/summary
    def get_configs_summary(self, context):
        settings = Settings.instance()
        proxy = settings.proxy
        intercept_settings = InterceptSettings(settings)

        project_key = intercept_settings.project_key
        project_id = ProjectKey(project_key).id if project_key else None
                
        scenario_key = intercept_settings.scenario_key
        scenario_id =  ScenarioKey(scenario_key).id if scenario_key else None

        # Check to make sure the scenario still exists
        if scenario_id:
            resource = ScenariosResource(settings.remote.api_url, settings.remote.api_key)
            res = resource.show(scenario_id)

            if not res.ok and res.status_code == 404:
                scenario_id = None
                intercept_settings.scenario_key = None
                settings.commit()

        context.render(
            json = {
                'active': intercept_settings.active,
                'mode': intercept_settings.mode,
                'modes': [mode.RECORD, mode.MOCK, mode.TEST, mode.REPLAY],
                'project_id': project_id,
                'proxy_url': proxy.url,
                'scenario_id': scenario_id,
            },
            status = 200
        )

    # PUT /api/v1/admin/configs
    def put_configs(self, context):
        updated_settings = context.parse_body()
        settings = Settings.instance()
        merged_settings = merge(settings.to_dict(), updated_settings)
        settings.write(merged_settings)

        context.render(
            json = merged_settings,
            status = 200
        )