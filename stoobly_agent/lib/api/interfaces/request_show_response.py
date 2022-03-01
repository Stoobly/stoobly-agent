from typing import TypedDict, Union

from .response_show_response import ResponseShowResponse

class RequestShowResponse(TypedDict):
  body: str
  headers: Union[list, None]
  id: str
  method: str
  query_params: Union[list, None]
  response: ResponseShowResponse
  status: int