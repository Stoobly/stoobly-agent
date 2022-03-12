from stoobly_agent.lib.api.requests_resource import RequestsResource

class StooblyRequestAdapter():

  def __init__(self, api: RequestsResource):
    self.api = api

  def create(self, project_id: str, raw_requests, params):
    res = self.api.create(project_id, raw_requests, params)
    return res.json()

  def show(self, project_id: str, request_id: str, query_params):
    res = self.api.show(project_id, request_id, query_params)
    return res.json()

  def index(self, project_id: int, query_params):
    res = self.api.index(project_id, query_params)
    return res.json()
