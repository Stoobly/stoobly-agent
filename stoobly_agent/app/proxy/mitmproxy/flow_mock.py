import requests

from stoobly_agent.app.models.adapters.mitmproxy_request_adapter import MitmproxyRequestAdapter
from stoobly_agent.app.models.adapters.mitmproxy_response_adapter import MitmproxyResponseAdapter
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
    self.__request = MitmproxyRequestAdapter(DEFAULT_HTTP_VERSION, _request).adapt()

  @response.setter
  def response(self, _response: requests.Response):
    self.__response = MitmproxyResponseAdapter(DEFAULT_HTTP_VERSION, _response).adapt()