from .stoobly_api import StooblyApi

class TestsResource(StooblyApi):

  def create(self, project_id: str, raw_request, params = {}):
    url = f"{self.service_url}{self.TESTS_ENDPOINT}"

    body = {
        'project_id': project_id,
        **params,
    }

    return self.post(url, headers=self.default_headers, data=body, files={ 'request': raw_request })