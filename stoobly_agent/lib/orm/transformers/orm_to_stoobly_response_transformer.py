import pdb

from httptools import HttpResponseParser

from stoobly_agent.lib.api.interfaces import ResponseShowResponse

from ..response import Response as ORMResponse
from ..utils.response_parse_handler import Response as ResponseDict, ResponseParseHandler

class ORMToStooblyResponseTransformer():
  __response: ORMResponse = None
  __response_dict: ResponseDict = None

  def __init__(self, response: ORMResponse):
    self.__response = response
    self.__response_dict: ResponseDict = { 'body': response.raw }
    parser = self.__new_parser(self.__response_dict)
    self.__response_dict['status_code'] = parser.get_status_code()

  @property
  def response_dict(self):
    return self.__response_dict

  def transform(self) -> ResponseShowResponse:
    return self.__response_dict_to_response(self.__response_dict)

  def __response_dict_to_response(self, response_dict: ResponseDict) -> ResponseShowResponse:
    stoobly_response: ResponseShowResponse = {}
    stoobly_response['text'] = response_dict['body'] 

    return stoobly_response

  def __new_parser(self, response_dict: ResponseDict):    
    handler = ResponseParseHandler(response_dict)
    parser = HttpResponseParser(handler)
    parser.feed_data(memoryview(self.__response.raw))
    return parser
  