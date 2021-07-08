import base64
import json
import requests
import pdb

class AgentApi:
    STATUSES_ENDPOINT = '/api/v1/admin/statuses'

    def __init__(self, service_url):
        self.service_url = service_url

    @property
    def default_headers(self):
        return {
            'X-Do-Proxy': '1',
        }

    def update_status(self, status_id, project_key):
        project_data = self.decode_project_key(project_key)
        url = f"{self.service_url}{self.STATUSES_ENDPOINT}/{status_id}"
        return requests.put(url, data=str(project_data.get('id')), headers=self.default_headers)

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
