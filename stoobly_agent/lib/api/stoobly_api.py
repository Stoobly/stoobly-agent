import base64
import json
import requests
import urllib
import pdb

from ..logger import Logger
from .api import Api

class StooblyApi(Api):
    LOG_ID = 'lib.api.stoobly_api'
    REPORTS_ENDPOINT = '/reports'
    REQUESTS_ENDPOINT = '/requests'
    TESTS_ENDPOINT = '/tests'

    def __init__(self, service_url: str, api_key: str):
        self.service_url = service_url
        self.api_key = api_key

    @staticmethod
    def decode_key(key):
        try:
            key = base64.b64decode(key)
        except:
            return {}

        # TODO: add specific error catching
        try:
            return json.loads(key)
        except:
            return {}

    @staticmethod
    def decode_report_key(key):
        try:
            key = base64.b64decode(key)
        except:
            return {}

        # TODO: add specific error catching
        try:
            return json.loads(key)
        except:
            return {}

    @staticmethod
    def decode_project_key(key):
        # TODO: add specific error catching
        try:
            key = base64.b64decode(key)
        except:
            return {}

        # TODO: add specific error catching
        try:
            return json.loads(key)
        except:
            return {}

    @staticmethod
    def decode_scenario_key(key):
        try:
            key = base64.b64decode(key)
        except:
            return {}

        try:
            return json.loads(key)
        except:
            return {}

    @property
    def default_headers(self):
        return {
            'X-API-KEY': self.api_key,
            'X-Do-Proxy': '1',
        }

    # Request

    def from_project_key(self, project_key, handler):
        project_data = self.decode_project_key(project_key)
        return handler(project_data.get('i'))

    def from_scenario_key(self, scenario_key, handler):
        scenario_data = self.decode_scenario_key(scenario_key)
        return handler(scenario_data.get('p'), {
            'scenario_id': scenario_data['i']
        })

    def with_report_key(self, report_key, params):
        if not report_key:
            return

        report_data = self.decode_report_key(report_key)
        params['report_id'] = report_data.get('i')

        return self

    def with_scenario_key(self, scenario_key, params):
        if scenario_key and len(scenario_key) != 0:
            scenario_data = self.decode_scenario_key(scenario_key)

            if 'id' in scenario_data:
                scenario_id = scenario_data['i']
                params['scenario_id'] = scenario_id

        return self