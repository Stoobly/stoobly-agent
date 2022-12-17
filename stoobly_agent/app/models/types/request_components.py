from typing import List, TypedDict

from stoobly_agent.lib.api.interfaces.header_show_response import Header
from stoobly_agent.lib.api.interfaces.query_param_show_response import QueryParam
from stoobly_agent.lib.api.interfaces.response_header_show_response import ResponseHeader

class HeaderIndexResponse(TypedDict):
  list: List[Header]

class QueryParamIndexResponse(TypedDict):
  list: List[QueryParam]
  total: int

class ResponseHeaderIndexResponse(TypedDict):
  list: List[ResponseHeader]
  total: int