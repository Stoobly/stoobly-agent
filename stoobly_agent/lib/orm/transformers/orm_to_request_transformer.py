import pdb

from requests import Request

from stoobly_agent.app.models.adapters.raw_http_request_adapter import RawHttpRequestAdapter

from ..request import Request as ORMRequest

class ORMToRequestTransformer():

  def __init__(self, request: ORMRequest):
    self.__dirty = False

    self.__body = None
    self.__headers = None
    self.__method = None
    self.__request = request
    self.__url = None

  def transform(self) -> Request:
    adapter = RawHttpRequestAdapter(self.__request.raw)

    if self.__body:
      adapter.body = self.__body 

    if self.__headers:
      adapter.headers = self.__headers

    if self.__method:
      adapter.method = self.__method

    if self.__url:
      adapter.url = self.__url

    python_request = adapter.to_request()

    return python_request

  @property
  def dirty(self):
    return self.__dirty

  def with_body(self, body: str):
    self.__body = body
    self.__dirty = True
    return self

  def with_headers(self, headers: list):
    self.__headers = headers
    self.__dirty = True
    return self

  def with_method(self, method: str):
    _method = method.strip().upper()
    if not self.__validate_method(_method):
      return self
    self.__method = _method
    self.__dirty = True
    return self

  def with_url(self, url: str):
    self.__url = url
    self.__dirty = True
    return self

  def __validate_method(self, method: str):
    if not isinstance(method, str):
      return False

    return method.upper() in ['CONNECT', 'DELETE', 'GET', 'HEAD', 'OPTIONS', 'PATCH', 'POST', 'PUT', 'TRACE']