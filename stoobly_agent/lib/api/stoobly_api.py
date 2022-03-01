import base64
import json
import requests
import urllib
import pdb

from ..logger import Logger
from .interfaces.requests_index_query_params import RequestsIndexQueryParams

class StooblyApi:
    LOG_ID = 'lib.api.stoobly_api'
    REPORTS_ENDPOINT = '/reports'
    REQUESTS_ENDPOINT = '/requests'
    TESTS_ENDPOINT = '/tests'

    def __init__(self, service_url: str, api_key: str):
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

    # Request

    def requests_index(self, project_key: str, query_params: RequestsIndexQueryParams):
        url = f"{self.service_url}{self.REQUESTS_ENDPOINT}"

        project_data = self.decode_project_key(project_key)

        params = {
            'project_id': project_data.get('id'),
            **query_params,
        }

        Logger.instance().debug(f"{self.LOG_ID}.request_response:{url}?{urllib.parse.urlencode(params)}")

        return requests.get(url, headers=self.default_headers, params=params)


    def request_show(self, project_key: str, request_id: str, query_params) -> requests.Response:
        url = f"{self.service_url}{self.REQUESTS_ENDPOINT}/{request_id}"

        project_data = self.decode_project_key(project_key)

        params = {
            'project_id': project_data.get('id'),
            **query_params,
        }

        Logger.instance().debug(f"{self.LOG_ID}.request_response:{url}?{urllib.parse.urlencode(params)}")

        return requests.get(url, headers=self.default_headers, params=params)

    def request_create(self, project_key: str, raw_requests, params) -> requests.Response:
        url = f"{self.service_url}{self.REQUESTS_ENDPOINT}"

        self.__parse_scenario_key(params)

        project_data = self.decode_project_key(project_key)

        body = {
            'project_id': project_data.get('id'),
            **params,
        }

        return requests.post(url, headers=self.default_headers, data=body, files={ 'requests': raw_requests })

    def request_response(self, project_key: str, query_params) -> requests.Response:
        url = f"{self.service_url}{self.REQUESTS_ENDPOINT}/response"

        self.__parse_scenario_key(query_params)

        project_data = self.decode_project_key(project_key)

        params = {
            'project_id': project_data.get('id'),
            **query_params,
        }

        Logger.instance().debug(f"{self.LOG_ID}.request_response:{url}?{urllib.parse.urlencode(params)}")

        return requests.get(
            url,
            allow_redirects=False,
            headers=self.default_headers,
            params=params,
            stream=True
        )

    # Report

    def report_create(self, project_key: str, params) -> requests.Response:
        url = f"{self.service_url}{self.REPORTS_ENDPOINT}"

        self.__parse_scenario_key(params)

        project_data = self.decode_project_key(project_key)

        body = {
            'project_id': project_data.get('id'),
            **params,
        }

        return requests.post(url, headers=self.default_headers, json=body)

    # Test

    def test_create(self, project_key: str, raw_request, params) -> requests.Response:
        url = f"{self.service_url}{self.TESTS_ENDPOINT}"

        self.__parse_scenario_key(params)

        project_data = self.decode_project_key(project_key)

        body = {
            'project_id': project_data.get('id'),
            **params,
        }

        return requests.post(url, headers=self.default_headers, data=body, files={ 'request': raw_request })

    def __parse_scenario_key(self, params) -> None:
        if not 'scenario_key' in params:
            return

        if params['scenario_key'] and len(params['scenario_key']) != 0:
            scenario_data = self.decode_scenario_key(params['scenario_key'])

            if 'id' in scenario_data:
                scenario_id = scenario_data['id']
                params['scenario_id'] = scenario_id

        del params['scenario_key']
