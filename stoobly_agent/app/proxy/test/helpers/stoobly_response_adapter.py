from urllib.request import Request
from stoobly_agent.lib.api.interfaces.request_show_response import RequestShowResponse
from stoobly_agent.lib.api.interfaces.response_show_response import ResponseShowResponse

from ..context_response import TestContextResponse

class StooblyResponseAdapter():

  def __init__(self, request: RequestShowResponse, response: ResponseShowResponse) -> None:
      self._request = request
      self._response = response

  def adapt(self):
    response = TestContextResponse()

    response.with_content(self._response['text'])
    response.with_status_code(self._request['status'])

    return response