import pdb
import requests

from stoobly_agent.app.models.adapters.raw_http_request_adapter import RawHttpRequestAdapter
from stoobly_agent.lib.orm.request import Request

class LocalDBBodyAdapter():
  __request_orm = None

  def __init__(self, request_orm: Request.__class__ = Request):
    self.__request_orm = request_orm

  def mock(self, request_id) -> requests.Request:
    request = self.__request_orm.find(request_id)

    if not request:
      return []

    return RawHttpRequestAdapter(request.raw).to_request()
    