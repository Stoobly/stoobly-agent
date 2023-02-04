import requests

from httptools import HttpResponseParser
from io import BytesIO
from mitmproxy.net import encoding
from requests.structures import CaseInsensitiveDict

from stoobly_agent.app.proxy.mitmproxy.response import Response
from stoobly_agent.lib.orm.utils.response_parse_handler import Response as ResponseDict, ResponseParseHandler

CRLF = b'\r\n'
DEFAULT_HTTP_VERSION = b'HTTP/1.1'

class RawHttpResponseAdapter():

  def __init__(self, req_text):
    self.__req_text = req_text
    req_lines = self.__req_text.split(CRLF)
    self.__parse_response_line(req_lines[0])
    ind = 1
    self.headers = dict()
    while ind < len(req_lines) and len(req_lines[ind]) > 0:
        colon_ind = req_lines[ind].find(b':')
        header_key = req_lines[ind][:colon_ind]
        header_value = req_lines[ind][colon_ind + 1:]
        self.headers[header_key] = header_value
        ind += 1
    ind += 1
    data_lines = req_lines[ind:] if ind < len(req_lines) else None
    self.body = CRLF.join(data_lines)

  def to_response(self):
    response = requests.Response()
    response.status_code = self.status
    response._content = self.body
    response.headers = self.headers

    return response

  def to_response_from_http_response_parser(self):
    response_dict: ResponseDict = {}
    parser = self.__new_parser(response_dict)
    response_dict['status_code'] = parser.get_status_code()

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

  def __parse_response_line(self, response_line):
    response_parts = response_line.split(b' ')
    self.protocol = response_parts[0] if len(response_parts) > 2 else DEFAULT_HTTP_VERSION
    self.status = response_parts[1]

  def __str__(self):
    headers = CRLF.join(f'{key}: {self.headers[key]}' for key in self.headers)
    return f'{self.method} {self.url} {self.protocol}{CRLF}' \
            f'{headers}{CRLF}{CRLF}{self.body}'

  def __new_parser(self, response_dict):
    handler = ResponseParseHandler(response_dict)
    parser = HttpResponseParser(handler)
    parser.feed_data(memoryview(self.__req_text))
    return parser