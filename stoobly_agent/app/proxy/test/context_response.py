import pdb

from ..replay.body_parser_service import decode_response, encode_response

class TestContextResponse():

  def __init__(self):
    self._content = ''
    self._headers = {}
    self._status_code = None

  @property
  def content(self):
    return self._content  

  @property
  def content_type(self):
    return self.headers.get('content-type')

  @property
  def headers(self):
    return self._headers

  @property
  def status_code(self):
    return self._status_code

  def decode_content(self):
    content_type = self.content_type
    return decode_response(self.content, content_type)

  def encode_content(self):
    content_type = self.content_type
    return encode_response(self.content, content_type)

  def with_content(self, content):
    self._content = content
    return self

  def with_headers(self, headers):
    self._headers = headers
    return self

  def with_status_code(self, status_code):
    self._status_code = status_code
    return self
