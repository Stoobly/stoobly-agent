import pdb

from stoobly_agent.app.models.adapters.joined_request_adapter import JoinedRequestAdapter
from stoobly_agent.app.models.adapters.raw_http_response_adapter import RawHttpResponseAdapter

class PythonResponseAdapter():

  def __init__(self, joined_request: bytes):
    self.__request = joined_request

  def adapt(self):
    if not self.__request:
      return None

    adapter = JoinedRequestAdapter(self.__request)
    response_string = adapter.build_response_string().get()
    return RawHttpResponseAdapter(response_string).to_response()