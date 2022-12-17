import pdb
import requests

from typing import List

from stoobly_agent.app.models.adapters.raw_http_request_adapter import RawHttpRequestAdapter
from stoobly_agent.lib.api.interfaces.header_show_response import HeaderShowResponse
from stoobly_agent.lib.orm.request import Request

class LocalDBHeaderAdapter():
  __request_orm = None

  def __init__(self, request_orm: Request.__class__ = Request):
    self.__request_orm = request_orm

  def index(self, request_id, **query_params) -> List[HeaderShowResponse]:
    request = self.__request_orm.find(request_id)

    if not request:
      return []

    request: requests.Request = RawHttpRequestAdapter(request.raw).to_request()

    headers = []
    for key, val in request.headers.items():
      headers.append({
        'name': key.decode(),
        'value': val.decode(),
      })

    return headers