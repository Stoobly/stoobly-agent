import pdb
import requests

from typing import List

from stoobly_agent.lib.orm.request import Request
from stoobly_agent.lib.orm.transformers import ORMToRequestsResponseTransformer

class LocalDBResponseAdapter():
  __request_orm = None

  def __init__(self, request_orm: Request.__class__ = Request):
    self.__request_orm = request_orm

  def mock(self, request_id) -> requests.Response:
    request = self.__request_orm.find(request_id)

    if not request:
      return []

    response = request.response
    return ORMToRequestsResponseTransformer(response).transform()