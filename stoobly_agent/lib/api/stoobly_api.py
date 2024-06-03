import base64
import json
import os
import pdb

from stoobly_agent.config.constants import custom_headers, env_vars
from stoobly_agent.lib.api.keys import InvalidReportKey, InvalidScenarioKey, ProjectKey, ReportKey, ScenarioKey

from .api import Api

class StooblyApi(Api):
    REPORTS_ENDPOINT = '/reports'
    REQUESTS_ENDPOINT = '/requests'
    TESTS_ENDPOINT = '/tests'

    def __init__(self, service_url: str, api_key: str):
        self.service_url = service_url
        self.api_key = api_key

    @property
    def default_headers(self):
        headers = {
            'X-API-KEY': self.api_key,
        }

        if not os.environ.get(env_vars.AGENT_SELF_INTERCEPT_ENABLED):
            headers[custom_headers.DO_PROXY] = '1'

        return headers

    # Request

    def from_project_key(self, project_key, handler):
        key = ProjectKey(project_key)
        return handler(key.id)

    def from_scenario_key(self, scenario_key, handler):
        key = ScenarioKey(scenario_key)
        return handler(key.project_id, {
            'scenario_id': key.id,
        })

    def with_report_key(self, report_key, params):
        try:
            key = ReportKey(report_key)
            params['report_id'] = key.id
        except InvalidReportKey:
            pass

        return self

    def with_scenario_key(self, scenario_key, params):
        try:
            key = ScenarioKey(scenario_key)
            params['scenario_id'] = key.id
        except InvalidScenarioKey:
            pass

        return self