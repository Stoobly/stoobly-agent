import pdb
import requests

from typing import List

from stoobly_agent.app.models.adapters.raw_http_response_adapter import RawHttpResponseAdapter
from stoobly_agent.lib.api.interfaces.header_show_response import HeaderShowResponse
from stoobly_agent.lib.orm.request import Request

class LocalDBResponseHeaderAdapter():
  __request_orm = None

  def __init__(self, request_orm: Request.__class__ = Request):
    self.__request_orm = request_orm

  def index(self, response_id, **query_params) -> List[HeaderShowResponse]:
    request = self.__request_orm.find(response_id)

    if not request:
      return []

    response = request.response

    if not response:
      return []

    response: requests.Response = RawHttpResponseAdapter(response.raw).to_response()

    headers = []
    for key, val in response.headers.items():
      headers.append({
        'name': key.decode(),
        'value': val.decode(),
      })

    return headers