from base64 import b64encode
import pdb

from httptools import HttpRequestParser, parse_url
from typing import List
from urllib.parse import parse_qs

from stoobly_agent.lib.api.interfaces import QueryParam, RequestShowResponse, ResponseShowResponse

from ..request import Request as ORMRequest
from .orm_to_stoobly_response_transformer import ORMTOStooblyResponseTransformer
from ..utils.request_parse_handler import Request as RequestDict, RequestParseHandler

class ORMTOStooblyRequestTransformer():
  __request: ORMRequest = None

  # TODO: filter by options
  def __init__(self, request: ORMRequest, options = {}):
    self.__request = request

    self.__request_dict: RequestDict = {}
    parser = self.__new_parser(self.__request_dict)
    self.__decorate_request_dict_with_parser(self.__request_dict, parser) 

  def transform(self) -> RequestShowResponse:
    stoobly_request = self.__request_dict_to_request(self.__request_dict)

    response = self.__request.response
    if response:
      transformer = ORMTOStooblyResponseTransformer(response)
      stoobly_response: ResponseShowResponse = transformer.transform()
      self.__decorate_with_stoobly_response(stoobly_request, stoobly_response)
      stoobly_request['status']  = transformer.response_dict['status_code']
    
    return stoobly_request

  def __request_dict_to_request(self, request_dict: RequestDict) -> RequestShowResponse:
    stoobly_request: RequestShowResponse = {}

    stoobly_request['headers'] = self.__transform_headers(request_dict['headers'])
    stoobly_request['method'] = request_dict['method'].decode()
    stoobly_request['body'] = b64encode(request_dict['body'])
    stoobly_request['url'] = request_dict['url'].decode()

    parsed_url = parse_url(request_dict['url'])
    stoobly_request['query_params'] = self.__transform_query_params(parsed_url.query)

    return stoobly_request

  def __transform_headers(self, headers: dict):
    headers_list = []
    for key, val in headers.items():
      headers_list.append({
        'name': key,
        'value': val,
      })

  def __transform_query_params(self, query_params):
    query_params_list: List[QueryParam] = []
    for key, val in parse_qs(query_params):
      query_params.append({
        'name': key,
        'value': val,
      })
    return query_params_list

  def __new_parser(self, request_dict: RequestDict):    
    handler = RequestParseHandler(request_dict)
    parser = HttpRequestParser(handler)
    parser.feed_data(memoryview(self.__request.raw))
    return parser
  
  def __decorate_request_dict_with_parser(self, stoobly_request: RequestShowResponse, parser):
    stoobly_request['method'] = parser.get_method()
  
  def __decorate_with_stoobly_response(self, stoobly_request: RequestShowResponse, stoobly_response: ResponseShowResponse):
    stoobly_request['response'] = stoobly_response