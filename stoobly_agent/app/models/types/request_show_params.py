from typing import TypedDict

class RequestShowParams(TypedDict):
  body: bool
  headers: bool
  project_id: str
  query_params: bool
  response: bool