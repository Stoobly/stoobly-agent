import pdb
import requests

from typing import List
from urllib.parse import parse_qs

from stoobly_agent.lib.api.interfaces import QueryParamShowResponse
from stoobly_agent.lib.orm.request import Request

class LocalDBQueryParamAdapter():
  __request_orm = None

  def __init__(self, request_orm: Request.__class__ = Request):
    self.__request_orm = request_orm

  def index(self, request_id, **query_params) -> List[QueryParamShowResponse]:
    request = self.__request_orm.find(request_id)

    if not request:
      return []

    request_dict = request.to_dict()
    parsed_query = parse_qs(request_dict['query'])

    query_params = []
    for key, params in parsed_query.items():
      for param in params:
        query_params.append({
          'name': key,
          'value': param,
        })

    return query_params