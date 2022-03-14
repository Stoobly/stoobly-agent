import requests

from stoobly_agent.lib.api.requests_resource import RequestsResource
from stoobly_agent.lib.api.interfaces.request_show_response import RequestShowResponse
from stoobly_agent.lib.api.interfaces.requests_index_response import RequestsIndexResponse

class StooblyRequestAdapter():

  def __init__(self, api: RequestsResource):
    self.api = api

  def create(self, project_id: str, raw_requests, params) -> RequestShowResponse:
    res = self.api.create(project_id, raw_requests, params)
    res.raise_for_status()  
    return res.json()

  def show(self, project_id: str, request_id: str, query_params) -> RequestShowResponse:
    res = self.api.show(project_id, request_id, query_params)
    res.raise_for_status()  
    return res.json()

  def index(self, project_id: int, query_params) -> RequestsIndexResponse:
    res = self.api.index(project_id, query_params)
    res.raise_for_status()  
    return res.json()
