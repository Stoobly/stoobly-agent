import pdb

from stoobly_agent.app.models.adapters.python.request.mitmproxy_adapter import MitmproxyRequestAdapter as PythonRequestMitmproxyRequestAdapter
from stoobly_agent.app.models.adapters.raw_http_request_adapter import RawHttpRequestAdapter
from stoobly_agent.lib.orm.request import Request

class MitmproxyRequestAdapter():

  def __init__(self, request: Request):
    self.__request = request

  def adapt(self):
    python_request = RawHttpRequestAdapter(self.__request.raw)
    return PythonRequestMitmproxyRequestAdapter(python_request).adapt()