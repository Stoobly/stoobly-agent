from mitmproxy.http import Response as MitmproxyResponse

from ..context_response import TestContextResponse

class MitmproxyResponseAdapter():

  def __init__(self, response: MitmproxyResponse) -> None:
    self._response = response

  def adapt(self):
    response = TestContextResponse()
    response.with_headers(self._response.headers)
    response.with_content(self._response.content)
    response.with_status_code(self._response.status_code)
    return response