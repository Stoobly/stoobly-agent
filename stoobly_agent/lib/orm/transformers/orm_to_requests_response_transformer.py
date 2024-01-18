import pdb

from requests import Response

from stoobly_agent.config.constants import custom_headers
from stoobly_agent.app.models.adapters.raw_http_response_adapter import RawHttpResponseAdapter

from ..response import Response as ORMResponse

class ORMToRequestsResponseTransformer():

  def __init__(self, response: ORMResponse):
    self.__body = None
    self.__dirty = False
    self.__headers = None
    self.__response = response
    self.__status = None
    self.__with_response_id = False

  @property
  def dirty(self):
    return self.__dirty

  def transform(self) -> Response:
    adapter = RawHttpResponseAdapter(self.__response.raw)

    if self.__body:
      adapter.body = self.__body 

    if self.__headers:
      adapter.headers = { **adapter.headers, **self.__headers }

    if self.__status:
      adapter.status = self.__status

    python_response = adapter.to_response()

    if self.__with_response_id:
      python_response.headers[custom_headers.RESPONSE_ID] = self.__response.id

    return python_response

  def with_response_id(self):
    self.__with_response_id = True
    return self

  def with_body(self, body: str):
    self.__body = body
    self.__dirty = True

    self.with_headers({ 'Content-Length': str(len(body)) })

    return self

  def with_headers(self, headers: dict):
    _headers = self.__headers or {}
    self.__headers = { **_headers, **headers } 
    self.__dirty = True
    return self

  def with_status(self, status: int):
    self.__status = status
    self.__dirty = True
    return self