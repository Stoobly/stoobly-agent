from typing import List, TypedDict

from .pagination_query_params import PaginationQueryParams

class TestShowResponse(TypedDict):
  id: int
  project_id: str

class TestsIndexQueryParams(PaginationQueryParams):
  project_id: str
  report_id: str
  scenario_id: str

class TestCreateParams(TypedDict):
  log: str
  passed: bool
  report_id: str
  request: bytes
  request_id: str
  status: str
  strategy: str

class TestsIndexResponse(TypedDict):
  list: List[TestShowResponse]
  total: int