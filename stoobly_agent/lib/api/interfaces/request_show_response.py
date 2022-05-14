from typing import TypedDict, Union

from .response_show_response import ResponseShowResponse

class QueryParam(TypedDict):
  name: str
  value: str

class RequestShowResponse(TypedDict):
  body: str
  endpoint_id: int
  headers: Union[list, None]
  host: str
  id: str
  method: str
  path: str
  port: str
  query_params: Union[list, None]
  response: ResponseShowResponse
  status: int
  url: str