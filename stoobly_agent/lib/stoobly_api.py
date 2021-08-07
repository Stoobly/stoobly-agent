import base64
import json
import requests
import urllib
import pdb

from .logger import Logger

class StooblyApi:
    LOG_ID = 'lib.stoobly_api'
    REQUESTS_ENDPOINT = '/requests'

    def __init__(self, service_url, api_key):
        self.service_url = service_url
        self.api_key = api_key

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

    def request_create(self, project_key, raw_requests, params):
        url = f"{self.service_url}{self.REQUESTS_ENDPOINT}"

        self.__parse_scenario_key(params)

        project_data = self.decode_project_key(project_key)

        body = {
            'project_id': project_data.get('id'),
            **params,
        }

        return requests.post(url, headers=self.default_headers, data=body, files={ 'requests': raw_requests })

    def request_response(self, project_key, query_params):
        url = f"{self.service_url}{self.REQUESTS_ENDPOINT}/response"

        self.__parse_scenario_key(query_params)

        project_data = self.decode_project_key(project_key)

        params = {
            'project_id': project_data.get('id'),
            **query_params,
        }
        
        Logger.instance().debug(f"{self.LOG_ID}.request_response:{url}?{urllib.parse.urlencode(params)}")

        return requests.get(url, headers=self.default_headers, params=params)

    def __parse_scenario_key(self, params):
        if not 'scenario_key' in params:
            return

        if len(params['scenario_key']) != 0:
            scenario_data = self.decode_scenario_key(params['scenario_key'])

            if 'id' in scenario_data:
                scenario_id = scenario_data['id']
                params['scenario_id'] = scenario_id

        del params['scenario_key']
