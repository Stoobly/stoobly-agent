from typing import List, TypedDict

from .request_show_response import RequestShowResponse

class RequestsIndexResponse(TypedDict):
  list: List[RequestShowResponse]
  total: int