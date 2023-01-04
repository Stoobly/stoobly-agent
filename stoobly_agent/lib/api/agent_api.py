import requests

from typing import Union

from .api import Api

class AgentApi(Api):
    STATUSES_ENDPOINT = '/api/v1/admin/statuses'

    def __init__(self, service_url):
        self.service_url = service_url

    @property
    def default_headers(self):
        return {
            'X-Do-Proxy': '1',
        }

    def update_status(self, status_id: str, project_id: Union[int, str]):
        url = f"{self.service_url}{self.STATUSES_ENDPOINT}/{status_id}"
        return self.put(url, data=str(project_id), headers=self.default_headers)
