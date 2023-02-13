import pdb
import requests

from typing import Union

CRLF = b'\r\n'
DEFAULT_HTTP_VERSION = b'HTTP/1.1'

class RawHttpRequestAdapter():

  def __init__(self, req_text):
    req_lines = req_text.split(CRLF)
    self.__parse_request_line(req_lines[0])
    ind = 1
    self.headers = dict()
    while ind < len(req_lines) and len(req_lines[ind]) > 0:
        colon_ind = req_lines[ind].find(b':')
        header_key = req_lines[ind][:colon_ind]
        header_value = req_lines[ind][colon_ind + 1:]
        self.headers[self.__decode(header_key)] = self.__decode(header_value).strip()
        ind += 1
    ind += 1
    data_lines = req_lines[ind:] if ind < len(req_lines) else None
    self.body = CRLF.join(data_lines)

  def to_request(self):
    req = requests.Request(
      method=self.method,
      url=self.url,
      headers=self.headers,
      data=self.body
    )

    return req

  def __parse_request_line(self, request_line):
    request_parts = request_line.split(b' ')
    self.method = self.__decode(request_parts[0])
    self.url = self.__decode(request_parts[1])
    self.protocol = self.__decode(request_parts[2]) if len(request_parts) > 2 else DEFAULT_HTTP_VERSION

  def __str__(self):
    headers = CRLF.join(f'{key}: {self.headers[key]}' for key in self.headers)
    return f'{self.method} {self.url} {self.protocol}{CRLF}' \
            f'{headers}{CRLF}{CRLF}{self.body}'


  def __decode(self, s: Union[bytes, str]) -> str:
    return s if isinstance(s, str) else s.decode()