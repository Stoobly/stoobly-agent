from requests import Response

from ..context_response import TestContextResponse

class RequestsResponseAdapter():

  def __init__(self, response: Response):
    self._response = response

  def adapt(self):
    response = TestContextResponse()

    response.with_content(self._response.content)
    response.with_headers(self._response.headers)
    response.with_status_code(self._response.status_code)

    return response