import pdb

from stoobly_agent.app.models.adapters.raw_http_request_adapter import RawHttpRequestAdapter
from stoobly_agent.lib.orm.request import Request

class PythonRequestAdapter():

  def __init__(self, request: Request):
    self.__request = request

  def adapt(self):
    raw_http_request_adapter = RawHttpRequestAdapter(self.__request.raw)
    return raw_http_request_adapter.to_request()