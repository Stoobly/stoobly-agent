import pdb
import requests

from stoobly_agent.app.proxy.mitmproxy.request_facade import MitmproxyRequestFacade
from stoobly_agent.app.proxy.record.proxy_request import ProxyRequest
from stoobly_agent.app.proxy.record.request_string import RequestString

from .mitmproxy_adapter import MitmproxyRequestAdapter

class RawRequestAdapter():

  def __init__(self, http_version: str, request: requests.Request):
    self.__http_version = http_version
    self.__request = request

  def adapt(self):
    mitmproxy_request = MitmproxyRequestAdapter(self.__http_version, self.__request).adapt()
    adapted_request = MitmproxyRequestFacade(mitmproxy_request)
    proxy_request = ProxyRequest(adapted_request)
    request_string = RequestString(proxy_request) 
    return request_string.get()