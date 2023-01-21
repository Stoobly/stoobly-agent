from typing import List, TypedDict

from stoobly_agent.lib.api.interfaces.headers import Header
from stoobly_agent.lib.api.interfaces.query_params import QueryParam
from stoobly_agent.lib.api.interfaces.response_headers import ResponseHeader

class HeaderIndexResponse(TypedDict):
  list: List[Header]

class QueryParamIndexResponse(TypedDict):
  list: List[QueryParam]
  total: int

class ResponseHeaderIndexResponse(TypedDict):
  list: List[ResponseHeader]
  total: int