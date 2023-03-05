from lib.api.interfaces.requests import RequestShowResponse

from .mitmproxy_adapter import MitmproxyRequestAdapter

class StooblyRequestAdapterFactory():

  def __init__(self, request: RequestShowResponse):
    self.__request = request

  def mitmproxy_request(self):
    return MitmproxyRequestAdapter(self.__request)