import requests

from stoobly_agent.lib.api.requests_resource import RequestsResource
from stoobly_agent.lib.api.interfaces.request_show_response import RequestShowResponse
from stoobly_agent.lib.api.interfaces.requests_index_response import RequestsIndexResponse

from .types.request_create_params import RequestCreateParams

class StooblyRequestAdapter():

  def __init__(self, __api: RequestsResource):
    self.__api = __api

  def create(self, **body_params: RequestCreateParams) -> RequestShowResponse:
    del body_params['flow']

    res = self.__api.create({ 'importer': 'gor', **body_params })
    res.raise_for_status()  
    return res.json()

  def response(self, **query_params) -> requests.Response:
    return self.__api.response(**query_params)

  def show(self, project_id: str, request_id: str, query_params) -> RequestShowResponse:
    res = self.__api.show(project_id, request_id, query_params)
    res.raise_for_status()  
    return res.json()

  def index(self, project_id: int, query_params) -> RequestsIndexResponse:
    res = self.__api.index(project_id, query_params)
    res.raise_for_status()  
    return res.json()
