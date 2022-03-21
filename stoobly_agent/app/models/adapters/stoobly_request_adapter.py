import pdb
import requests

from stoobly_agent.lib.api.requests_resource import RequestsResource
from stoobly_agent.lib.api.interfaces.request_show_response import RequestShowResponse
from stoobly_agent.lib.api.interfaces.requests_index_response import RequestsIndexResponse

from .types import RequestCreateParams, RequestShowParams

class StooblyRequestAdapter():

  def __init__(self, __api: RequestsResource):
    self.__api = __api

  def create(self, **params: RequestCreateParams) -> RequestShowResponse:
    body_params = { **params }
    joined_request = body_params['joined_request']

    del body_params['flow']
    del body_params['joined_request']

    res = self.__api.create(**{ 'importer': 'gor', 'requests': joined_request.build(), **body_params })
    res.raise_for_status()  
    return res.json()

  def response(self, **query_params) -> requests.Response:
    return self.__api.response(**query_params)

  def show(self, request_id: str, **params: RequestShowParams) -> RequestShowResponse:
    query_params = { **params } 

    res = self.__api.show(request_id, **query_params)
    res.raise_for_status()  
    return res.json()

  def index(self, **query_params) -> RequestsIndexResponse:
    res = self.__api.index(**query_params)
    res.raise_for_status()  
    return res.json()
