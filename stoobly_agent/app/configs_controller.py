from mergedeep import merge

from ..lib.api.stoobly_api import StooblyApi
from ..lib.intercept_handler.constants import mock_policy, modes, record_policy
from ..lib.settings import Settings

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
        active_mode = settings.active_mode

        if active_mode in [modes.MOCK, modes.TEST]:
            context.render(
                json = [mock_policy.ALL, mock_policy.FOUND, mock_policy.NONE],
                status = 200
            )
        elif active_mode == modes.RECORD:
            context.render(
                json = [record_policy.ALL, record_policy.NONE, record_policy.NOT_FOUND],
                status = 200
            )

    # GET /api/v1/admin/configs
    def get_configs(self, context):
        settings = Settings.instance()

        context.render(
            json = settings.to_hash(),
            status = 200
        )

    # GET /api/v1/admin/configs/modes
    def get_configs_modes(self, context):
        settings = Settings.instance()
        mode = settings.mode

        mock = {}
        mock_mode = mode.get('mock')
        if mock_mode:
            project_key = self.__merge_project_key(mock, mock_mode)
            self.__merge_scenario_key(mock, mock_mode, project_key)

        record = {}
        record_mode = mode.get('record')
        if record_mode:
            project_key = self.__merge_project_key(record, record_mode)
            self.__merge_scenario_key(record, record_mode, project_key)

        test = {}
        test_mode = mode.get('test')
        if test_mode:
            project_key = self.__merge_project_key(test, test_mode)
            self.__merge_scenario_key(test, test_mode, project_key)

        active_mode =  settings.active_mode

        context.render(
            json = {
                'active': active_mode,
                'details': {
                    'mock': mock,
                    'record': record,
                    'test': test,
                },
                'enabled': settings.active_mode_settings.get('enabled'),
                'list': [modes.MOCK, modes.NONE, modes.RECORD, modes.TEST],
                'proxy_url': settings.proxy_url,
            },
            status = 200
        )

    # PUT /api/v1/admin/configs
    def put_configs(self, context):
        updated_settings = context.parse_body()
        settings = Settings.instance()

        merged_settings = merge(settings.to_hash(), updated_settings)
        settings.update(merged_settings)

        context.render(
            json = merged_settings,
            status = 200
        )

    def __merge_project_key(self, h, mode):
        project_key = mode.get('project_key')
        project = StooblyApi.decode_project_key(project_key)
        h['project_id'] = project.get('id')
        return project_key

    def __merge_scenario_key(self, h, mode, project_key):
        scenario_key = mode.get('settings', {}).get(project_key, {}).get('scenario_key')
        if isinstance(scenario_key, str) and len(scenario_key) > 0:
            scenario = StooblyApi.decode_scenario_key(scenario_key)
            h['scenario_id'] = scenario['id']
        return scenario_key
