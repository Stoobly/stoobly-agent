from typing import TypedDict, Union

from .response_show_response import ResponseShowResponse

class RequestShowResponse(TypedDict):
  body: str
  created_at: str
  endpoint_id: int
  headers: Union[list, None]
  host: str
  id: str
  is_deleted: bool
  latency: int
  method: str
  path: str
  port: str
  query_params: Union[list, None]
  response: ResponseShowResponse
  starred: bool
  status: int
  url: str