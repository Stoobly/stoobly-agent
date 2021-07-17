from mergedeep import merge

from ..lib.settings import Settings
from ..lib.stoobly_api import StooblyApi

class ConfigsController:
    _instance = None

    MODE = {
      'MOCK': 'mock',
      'RECORD': 'record',
    }

    MOCK_POLICY = {
      'ALL': 'all',
      'NONE': 'none',
      'FOUND': 'found',
    }

    RECORD_POLICY = {
      'NONE': 'none',
      'ALL': 'all',
      'NOT_FOUND': 'not_found',
    }

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

        if active_mode == self.MODE['MOCK']:
            context.render(
                json = self.MOCK_POLICY,
                status = 200
            )
        elif active_mode == self.MODE['RECORD']:
            context.render(
                json = self.RECORD_POLICY,
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
            project = StooblyApi.decode_project_key(mock_mode.get('project_key'))
            mock['project_id'] = project.get('id')

            scenario_key = mock_mode.get('scenario_key')
            if isinstance(scenario_key, str) and len(scenario_key) > 0:
                scenario = StooblyApi.decode_scenario_key(scenario_key)
                mock['scenario_id'] = scenario['id']

        record = {}
        record_mode = mode.get('record')
        if record_mode:
            project = StooblyApi.decode_project_key(record_mode.get('project_key'))
            record['project_id'] = project.get('id')

            scenario_key = record_mode.get('scenario_key')
            if isinstance(scenario_key, str) and len(scenario_key) > 0:
                scenario = StooblyApi.decode_scenario_key(scenario_key)
                record['scenario_id'] = scenario['id']

        active_mode =  settings.active_mode

        context.render(
            json = {
                'active': active_mode,
                'details': {
                    'mock': mock,
                    'record': record,
                },
                'enabled': settings.active_mode_settings.get('enabled'),
                'list': list(self.MODE.values()),
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
