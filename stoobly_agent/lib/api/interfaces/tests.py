from typing import List, TypedDict, Union

from stoobly_agent.config.constants import test_strategy

from .pagination_query_params import PaginationQueryParams

class TestShowResponse(TypedDict):
  expected_latency: int
  id: int
  passed: bool
  project_id: str
  strategy: Union[test_strategy.DIFF, test_strategy.CUSTOM, test_strategy.FUZZY] 

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