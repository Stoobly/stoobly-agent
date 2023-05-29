import pdb

from stoobly_agent.app.models.adapters.python.request.mitmproxy_adapter import MitmproxyRequestAdapter as PythonRequestMitmproxyRequestAdapter
from stoobly_agent.app.models.adapters.raw_http_request_adapter import RawHttpRequestAdapter
from stoobly_agent.lib.orm.request import Request

class MitmproxyRequestAdapter():

  def __init__(self, request: Request):
    self.__request = request

  def adapt(self):
    raw_http_request_adapter = RawHttpRequestAdapter(self.__request.raw)
    python_request = raw_http_request_adapter.to_request()
    protocol = raw_http_request_adapter.protocol
    http_version = protocol.split('/')[1]

    return PythonRequestMitmproxyRequestAdapter(http_version, python_request).adapt()
