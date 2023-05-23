import pdb
import requests

from typing import Tuple

from stoobly_agent.app.models.types import RequestCreateParams, RequestShowParams
from stoobly_agent.lib.api.requests_resource import RequestsResource
from stoobly_agent.lib.api.interfaces import RequestShowResponse, RequestsIndexResponse
from stoobly_agent.lib.orm.types.request_columns import RequestColumns

class StooblyRequestAdapter():

  def __init__(self, __api: RequestsResource):
    self.__api = __api

  def create(self, **params: RequestCreateParams):
    body_params = { **params }
    joined_request = body_params['joined_request']

    del body_params['flow']
    del body_params['joined_request']

    res = self.__api.create(**{ 'importer': 'gor', 'requests': joined_request.build(), **body_params })
    res.raise_for_status()  
    return res.json(), res.status_code

  def response(self, **query_params: RequestColumns):
    return self.__api.response(**query_params)

  def show(self, request_id: str, **params: RequestShowParams) -> Tuple[RequestShowResponse, int]:
    query_params = { **params } 

    res = self.__api.show(request_id, **query_params)
    res.raise_for_status()  
    return res.json(), res.status_code

  def index(self, **query_params) -> Tuple[RequestsIndexResponse, int]:
    res = self.__api.index(**query_params)
    res.raise_for_status()  
    return res.json(), res.status_code
