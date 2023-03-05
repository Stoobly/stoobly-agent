import requests

from stoobly_agent.app.models.adapters.python import PythonRequestAdapterFactory, PythonResponseAdapterFactory
from stoobly_agent.app.models.adapters.raw_http_request_adapter import DEFAULT_HTTP_VERSION

class MitmproxyFlowMock():

  def __init__(self):
    self.__request = None
    self.__response = None

  @property
  def request(self):
    return self.__request

  @property
  def response(self):
    return self.__response

  @request.setter
  def request(self, _request: requests.Request):
    self.__request = PythonRequestAdapterFactory(_request).mitmproxy_request(DEFAULT_HTTP_VERSION)

  @response.setter
  def response(self, _response: requests.Response):
    self.__response = PythonResponseAdapterFactory(_response).mitmproxy_response(DEFAULT_HTTP_VERSION)