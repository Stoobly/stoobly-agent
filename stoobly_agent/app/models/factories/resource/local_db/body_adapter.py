import pdb

from typing import TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from requests import Request

from stoobly_agent.app.models.adapters.raw_http_request_adapter import RawHttpRequestAdapter
from stoobly_agent.lib.orm.request import Request

from .local_db_adapter import LocalDBAdapter 
from .request_adapter import LocalDBRequestAdapter

class LocalDBBodyAdapter(LocalDBAdapter):
  __request_orm = None

  def __init__(self, request_orm: Request.__class__ = Request):
    self.__request_orm = request_orm

  def update(self, request_id, text: str):
    request = self.__request_orm.find(request_id)
    
    if not request:
      return self.__request_not_found()

    return self.success(LocalDBRequestAdapter(self.__request_orm).update(request_id, body=text))

  def mock(self, request_id) -> Tuple['Request', int]:
    request = self.__request_orm.find(request_id)

    if not request:
      return self.__request_not_found()

    return self.success(RawHttpRequestAdapter(request.raw).to_request())
  
  def __request_not_found(self):
    return self.not_found('Request not found')  