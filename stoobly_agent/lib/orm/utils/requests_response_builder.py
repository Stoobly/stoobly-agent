from io import BytesIO
from requests import Response

class RequestsResponseBuilder():

  def __init__(self):
    self.__response = Response()

  def with_header(self, name, value):
    self.__response.headers[name] = value
    return self

  def with_body(self, content: bytes):
    self.__response.raw = BytesIO(content)
    return self

  def with_status_code(self, code: int):
    self.__response.status_code = code
    return self

  def with_reason(self, reason: str):
    self.__response.reason = reason
    return self

  def with_content_encoding(self, encoding):
    self.__response.encoding = encoding
    return self

  def build(self):
    return self.__response