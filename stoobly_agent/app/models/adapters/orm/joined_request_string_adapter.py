import pdb

from stoobly_agent.lib.orm.request import Request
from stoobly_agent.lib.orm.response import Response
from stoobly_agent.app.proxy.record import REQUEST_DELIMITTER, RequestString, ResponseString

from ..python.response.raw_adapter import RawResponseAdapter
from ..raw_http_response_adapter import RawHttpResponseAdapter
from .response.python_adapter import PythonResponseAdapter

class JoinedRequestStringAdapter():

  def __init__(self, request: Request):
    self.__request = request
    self.__response: Response = request.response

  @property
  def response(self):
    return self.__response

  @response.setter
  def response(self, r: Response):
    self.__response = r

  def adapt(self, base: str = None):
    request_string = RequestString(None) 
    request_string.control = self.__request.control
    request_string.set(self.__request.raw)

    response = self.response
    response_string = ResponseString(None, None)
    response_string.control = response.control
    response_string.set(response.raw)

    toks = [request_string.get(control=True), response_string.get(control=True)]
    if base:
      return REQUEST_DELIMITTER.join([base] + toks)
    else:
      return REQUEST_DELIMITTER.join(toks)

  def decode_response(self):
    response = self.response
    python_response = PythonResponseAdapter(response).adapt()

    adapter = RawHttpResponseAdapter(response.raw)
    adapter.body = python_response.content

    content_encoding_header = 'content-encoding'
    if content_encoding_header in adapter.headers:
      del adapter.headers[content_encoding_header]

    python_response = adapter.to_response()
    response.raw = RawResponseAdapter(python_response).adapt()