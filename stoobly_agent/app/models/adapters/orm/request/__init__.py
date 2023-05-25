import pdb

from stoobly_agent.lib.orm.request import Request

from .mitmproxy_adapter import MitmproxyRequestAdapter

class OrmRequestAdapterFactory():

  def __init__(self, request: Request):
    self.__request = request

  def mitmproxy_request(self):
    return MitmproxyRequestAdapter(self.__request).adapt()