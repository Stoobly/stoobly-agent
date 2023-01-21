from typing import TypedDict

class QueryParam(TypedDict):
  name: str
  value: str

class QueryParamShowResponse(QueryParam):
  id: str