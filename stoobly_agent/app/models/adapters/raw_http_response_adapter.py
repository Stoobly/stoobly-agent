import pdb

from httptools import HttpResponseParser
from io import BytesIO

from stoobly_agent.app.proxy.mitmproxy.response import Response
from stoobly_agent.lib.utils.decode import decode
from stoobly_agent.lib.orm.utils.response_parse_handler import Response as ResponseDict, ResponseParseHandler

CRLF = b'\r\n'
DEFAULT_HTTP_VERSION = b'HTTP/1.1'

HEADER_SEPARATOR = ', '
HEADER_SET_COOKIE = 'set-cookie'

class RawHttpResponseAdapter():

  def __init__(self, req_text: bytes):
    self.__req_text = req_text
    req_lines = self.__req_text.split(CRLF)

    self.__parse_response_line(req_lines[0])

    ind = 1
    # Lazy import for runtime usage
    from requests.structures import CaseInsensitiveDict
    self.headers = CaseInsensitiveDict()
    while ind < len(req_lines) and len(req_lines[ind]) > 0:
        colon_ind = req_lines[ind].find(b':')
        header_key = req_lines[ind][:colon_ind]
        header_value = req_lines[ind][colon_ind + 1:]

        decoded_key = decode(header_key)
        decoded_value = decode(header_value).strip()
        if decoded_key in self.headers:
          # Set-Cookie must not be comma-joined (Expires values contain commas).
          if decoded_key.lower() == HEADER_SET_COOKIE:
            existing = self.headers[decoded_key]
            if isinstance(existing, list):
              existing.append(decoded_value)
            else:
              self.headers[decoded_key] = [existing, decoded_value]
          else:
            self.headers[decoded_key] = HEADER_SEPARATOR.join([self.headers[decoded_key], decoded_value])
        else:
          self.headers[decoded_key] = decoded_value

        ind += 1

    ind += 1

    data_lines = req_lines[ind:] if ind < len(req_lines) else None
    self.body = CRLF.join(data_lines)

  def to_response(self):
    # Lazy import for runtime usage
    import requests
    from urllib3._collections import HTTPHeaderDict

    response = requests.Response()
    response.status_code = self.status

    # HTTPHeaderDict preserves repeated Set-Cookie; CaseInsensitiveDict cannot.
    headers = HTTPHeaderDict()
    for key, val in self.headers.items():
      if isinstance(val, list):
        for item in val:
          headers.add(key, item)
      else:
        headers.add(key, val)

    response.headers = headers

    # Enforce proper Content-Length header
    response.headers['Content-Length'] = str(len(self.body))

    from urllib3 import HTTPResponse
    response.raw = HTTPResponse(
      body=BytesIO(self.body),
      decode_content=False,
      headers=headers,
      preload_content=False
    )

    #response.raw = self.__decode_body(self.body, content_encoding)

    return response

  def to_response_from_http_response_parser(self):
    response_dict: ResponseDict = {}
    parser = self.__new_parser(response_dict)
    response_dict['status_code'] = parser.get_status_code()

    # Lazy import for runtime usage
    requests_response = Response()
    # Lazy import for runtime usage
    from requests.structures import CaseInsensitiveDict
    requests_response.headers = CaseInsensitiveDict()
    for key, val in response_dict['headers'].items():
      _key = decode(key) 
      _val = decode(key)
      requests_response.headers[_key] = _val

    # Unless we can create an object with the stream method, have to self decode
    content_encoding = requests_response.headers.get('content-encoding')
    requests_response.raw = self.__decode_body(response_dict.get('body'), content_encoding)

    requests_response.reason = response_dict.get('status')
    requests_response.status_code = response_dict['status_code']

    # TODO: parse cookies, url. Not high priority, these aren't used
    
    return requests_response

  def __parse_response_line(self, response_line):
    response_parts = response_line.split(b' ')
    # "HTTP/x STATUS" (no reason) is the wire form written by ResponseString;
    # still trust the protocol token when present.
    if len(response_parts) >= 2:
      self.protocol = decode(response_parts[0])
      self.status = int(decode(response_parts[1]))
      self.reason = decode(b' '.join(response_parts[2:])) if len(response_parts) > 2 else ''
    else:
      self.protocol = decode(DEFAULT_HTTP_VERSION)
      self.status = 0
      self.reason = ''

  def __str__(self):
    header_lines = []
    for key in self.headers:
      val = self.headers[key]
      if isinstance(val, list):
        for item in val:
          header_lines.append(f'{key}: {item}')
      else:
        header_lines.append(f'{key}: {val}')
    headers = '\r\n'.join(header_lines)
    body = decode(self.body) if isinstance(self.body, (bytes, bytearray)) else (self.body or '')
    status_line = f'{self.protocol} {self.status}'
    if self.reason:
      status_line = f'{status_line} {self.reason}'
    return f'{status_line}\r\n{headers}\r\n\r\n{body}'

  def __new_parser(self, response_dict):
    handler = ResponseParseHandler(response_dict)
    parser = HttpResponseParser(handler)
    parser.feed_data(memoryview(self.__req_text))
    return parser

  def __decode_body(self, body: bytes, content_encoding):
    if content_encoding:
      # Lazy import for runtime usage
      from mitmproxy.net import encoding
      decoded_response = encoding.decode(body, content_encoding)
    else:
      decoded_response = body 

    return BytesIO(decoded_response)