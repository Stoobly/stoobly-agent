import pdb

from stoobly_agent.app.models.adapters.joined_request_adapter import JoinedRequestAdapter
from stoobly_agent.app.models.adapters.raw_http_request_adapter import RawHttpRequestAdapter

class PythonRequestAdapter():

  def __init__(self, joined_request: bytes):
    self.__request = joined_request

  def adapt(self):
    if not self.__request:
      return None

    adapter = JoinedRequestAdapter(self.__request)
    request_string = adapter.build_request_string().get()
    return RawHttpRequestAdapter(request_string).to_request()