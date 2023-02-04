import pdb

from requests import Response

from stoobly_agent.config.constants import custom_headers

from stoobly_agent.app.models.adapters.raw_http_response_adapter import RawHttpResponseAdapter

from ..response import Response as ORMResponse

class ORMToRequestsResponseTransformer():

  def __init__(self, response: ORMResponse):
    self.__response = response
    self.__with_response_id = False

  def transform(self) -> Response:
    python_response = RawHttpResponseAdapter(self.__response.raw).to_response()

    if self.__with_response_id:
      python_response.headers[custom_headers.RESPONSE_ID] = self.__response.id

    return python_response

  def with_response_id(self):
    self.__with_response_id = True
    return self