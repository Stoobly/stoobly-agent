import requests

from mitmproxy.http import Request as MitmproxyRequest, Response as MitmproxyResponse
from typing import Union

from stoobly_agent.app.models.adapters.python import PythonRequestAdapterFactory, PythonResponseAdapterFactory
from stoobly_agent.app.models.adapters.raw_http_request_adapter import DEFAULT_HTTP_VERSION

class MitmproxyFlowMock():

  def __init__(self):
    self.__request: MitmproxyRequest = None
    self.__response: MitmproxyResponse = None

  @property
  def request(self):
    return self.__request

  @property
  def response(self):
    return self.__response

  @request.setter
  def request(self, _request: Union[MitmproxyRequest, requests.Request]):
    if isinstance(_request, requests.Request):
      self.__request = PythonRequestAdapterFactory(_request).mitmproxy_request(DEFAULT_HTTP_VERSION)
    else:
      self.__request = _request

  @response.setter
  def response(self, _response: Union[MitmproxyResponse, requests.Response]):
    if isinstance(_response, requests.Response):
      self.__response = PythonResponseAdapterFactory(_response).mitmproxy_response()
    else:
      self.__response = _response