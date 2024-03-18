from base64 import b64encode
import pdb

from httptools import parse_url
from typing import List
from urllib.parse import parse_qs

from stoobly_agent.app.models.adapters.raw_http_request_adapter import RawHttpRequestAdapter
from stoobly_agent.app.models.types import RequestShowParams
from stoobly_agent.lib.api.interfaces import QueryParam, RequestShowResponse
from stoobly_agent.lib.utils.decode import decode

from ..request import Request as ORMRequest
from ..response import Response
from .orm_to_stoobly_response_transformer import ORMToStooblyResponseTransformer

FILTER_LIST = [
  'headers_hash',
  'body_text_hash',
  'query_params_hash',
  'body_params_hash',
  'control',
  'raw',
] 

class ORMToStooblyRequestTransformer():
  __options: RequestShowParams
  __request: ORMRequest = None

  # TODO: filter by options
  def __init__(self, request: ORMRequest, options: RequestShowParams):
    self.__options = options
    self.__request = request

  def transform(self) -> RequestShowResponse:
    stoobly_request: RequestShowResponse = self.__request.to_dict()

    self.__decorate_with_request(stoobly_request, self.__request)
    self.__decorate_with_response(stoobly_request, self.__request.response)
    self.__decorate_with_components(stoobly_request, self.__request)
    self.__decorate_with_scenario(stoobly_request, self.__request)
    
    return self.__filter_properties(stoobly_request)

  def __filter_properties(self, stoobly_request: RequestShowResponse):
    allowed_keys = list(RequestShowResponse.__annotations__.keys()) + [
      'pushed_at', 'body_params_hash', 'body_text_hash', 'key', 'query', 'query_params_hash'
    ]

    filter_keys = lambda request: dict((key, value) for key, value in request.items() if key in allowed_keys)
    return filter_keys(stoobly_request)

  def __decorate_with_scenario(self, stoobly_request: RequestShowResponse, request: ORMRequest):
    if not request.scenario_id:
      return

    scenario = request.scenario

    if scenario:
      stoobly_request['scenario'] = scenario.name

  def __decorate_with_components(self, stoobly_request: RequestShowResponse, request: ORMRequest):
    components = []
    if len(request.query_params_hash) != 0:
      components.append('query_params')

    if len(request.body_params_hash) != 0:
      components.append('body_params')

    if len(request.body_text_hash) != 0:
      components.append('body')

    if len(request.headers_hash) != 0:
      components.append('headers')

    if len(request.response_hash) != 0:
      components.append('response')

    if len(request.response_headers_hash) != 0:
      components.append('response_headers')

    stoobly_request['components'] = components

  def __decorate_with_request(self, stoobly_request: RequestShowResponse, request: ORMRequest):
    python_request = RawHttpRequestAdapter(request.raw).to_request()

    stoobly_request['method'] = python_request.method
    stoobly_request['url'] = python_request.url
    stoobly_request['is_deleted'] = bool(stoobly_request.get('is_deleted'))

    parsed_url = parse_url(python_request.url.encode())

    stoobly_request['scheme'] = parsed_url.schema.decode()

    if parsed_url.query == None:
      if 'query_params' in self.__options:
        stoobly_request['query_params'] = [] 
    else:
      stoobly_request['query'] = decode(parsed_url.query)

      if 'query_params' in self.__options:
        stoobly_request['query_params'] = self.__transform_query_params(stoobly_request['query'])

    if 'headers' in self.__options:
      stoobly_request['headers'] = self.__transform_headers(python_request.headers)

    if 'body' in self.__options:
      stoobly_request['body'] = b64encode(python_request.data)

  def __transform_headers(self, headers: dict):
    headers_list = []
    for key, val in headers.items():
      headers_list.append({
        'name': key,
        'value': val,
      })
    return headers_list

  def __transform_query_params(self, query_params):
    query_params_list: List[QueryParam] = []

    for key, val in parse_qs(query_params).items():
      query_params_list.append({
        'name': key,
        'value': val,
      })
    return query_params_list
  
  def __decorate_with_response(self, stoobly_request: RequestShowResponse, orm_response: Response):
    if not orm_response:
      return

    transformer = ORMToStooblyResponseTransformer(orm_response)
    stoobly_request['status'] = self.__request.status

    if 'response' in self.__options:
      stoobly_response = transformer.transform()
      stoobly_request['response'] = stoobly_response
