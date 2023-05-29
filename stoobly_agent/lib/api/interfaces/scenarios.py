from typing import List, TypedDict

from .pagination_query_params import PaginationQueryParams

class ScenarioShowResponse(TypedDict):
  created_at: str
  description: str
  key: str
  name: str
  overwritable: bool
  updated_at: str

class ScenariosIndexQueryParams(PaginationQueryParams):
  pass

class ScenariosIndexResponse(TypedDict):
  list: List[ScenarioShowResponse]
  total: int
