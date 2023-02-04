import pdb

from stoobly_agent.app.models.adapters.raw_http_response_adapter import RawHttpResponseAdapter
from stoobly_agent.lib.api.interfaces import ResponseShowResponse

from ..response import Response as ORMResponse
from ..utils.response_parse_handler import Response as ResponseDict

class ORMToStooblyResponseTransformer():
  __response: ORMResponse = None

  def __init__(self, response: ORMResponse):
    self.__response = response

  @property
  def python_response(self):
    return RawHttpResponseAdapter(self.__response.raw).to_response()

  def transform(self) -> ResponseShowResponse:
    response_dict: ResponseDict = { 'body': self.__response.raw }

    return self.__response_dict_to_response(response_dict)

  def __response_dict_to_response(self, response_dict: ResponseDict) -> ResponseShowResponse:
    stoobly_response: ResponseShowResponse = {}
    stoobly_response['text'] = response_dict['body'] 

    return stoobly_response
  