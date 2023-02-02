import pdb

from httptools import HttpResponseParser
from io import BytesIO
from mitmproxy.net import encoding
from requests import Response
from requests.structures import CaseInsensitiveDict

from stoobly_agent.config.constants import custom_headers

from ..response import Response as ORMResponse
from ..utils.response_parse_handler import Response as ResponseDict, ResponseParseHandler

class ORMToRequestsResponseTransformer():

  def __init__(self, response: ORMResponse):
    self.__response = response
    self.__with_response_id = False

  def transform(self) -> Response:
    response_dict: ResponseDict = {}
    parser = self.__new_parser(response_dict)
    response_dict['status_code'] = parser.get_status_code()

    if 'headers' not in response_dict:
      response_dict['headers'] = {}

    if self.__with_response_id:
      response_dict['headers'][custom_headers.RESPONSE_ID] = self.__response.id

    return self.__response_dict_to_response(response_dict)

  def with_response_id(self):
    self.__with_response_id = True
    return self

  def __response_dict_to_response(self, response_dict: ResponseDict):
    requests_response = Response()
    requests_response.headers = CaseInsensitiveDict()
    for key, val in response_dict['headers'].items():
      _key = key if not isinstance(key, bytes) else key.decode()
      _val = val if not isinstance(val, bytes) else val.decode()
      requests_response.headers[_key] = _val

    # Unless we can create an object with the stream method, have to self decode
    content_encoding = requests_response.headers.get('content-encoding')
    if content_encoding:
      decoded_response = encoding.decode(response_dict.get('body'), content_encoding)
    else:
      decoded_response = response_dict.get('body')

    requests_response.raw = BytesIO(decoded_response)

    requests_response.reason = response_dict.get('status')
    requests_response.status_code = response_dict['status_code']

    # TODO: parse cookies, url. Not high priority, these aren't used
    
    return requests_response

  def __new_parser(self, response_dict: ResponseDict):    
    handler = ResponseParseHandler(response_dict)
    parser = HttpResponseParser(handler)
    parser.feed_data(memoryview(self.__response.raw))
    return parser
  