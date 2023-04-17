import pdb
import requests

from stoobly_agent.app.models.adapters.raw_http_request_adapter import RawHttpRequestAdapter
from stoobly_agent.lib.orm.request import Request

from .request_adapter import LocalDBRequestAdapter

class LocalDBBodyAdapter():
  __request_orm = None

  def __init__(self, request_orm: Request.__class__ = Request):
    self.__request_orm = request_orm

  def update(self, request_id, text: str):
    request = self.__request_orm.find(request_id)
    
    if not request:
      return None

    return LocalDBRequestAdapter(self.__request_orm).update(request_id, body=text)

  def mock(self, request_id) -> requests.Request:
    request = self.__request_orm.find(request_id)

    if not request:
      return []

    return RawHttpRequestAdapter(request.raw).to_request()
    