from typing import List, TypedDict, Union

from .pagination_query_params import PaginationQueryParams
from .responses import ResponseShowResponse

class RequestCreateParams(TypedDict):
  importer: str
  project_id: str
  requests: bytes
  scenario_id: str

class RequestResponseShowQueryParams(TypedDict):
  body_params_hash: str
  body_text_hash: str
  headers_hash: str
  host: str
  infer: str
  method: str
  path: str
  port: str
  project_id: str
  query_params_hash: str
  rety: str
  scenario_id: str

class RequestShowQueryParams():
  body: bool
  header: bool
  project_id: str
  query_param: bool
  response: bool

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
  query: str
  query_params: Union[list, None]
  response: ResponseShowResponse
  scenario: str
  scenario_id: int
  starred: bool
  status: int
  url: str

class RequestsIndexQueryParams(PaginationQueryParams):
  filter: str
  project_id: str
  scenario_id: str

class RequestsIndexResponse(TypedDict):
  list: List[RequestShowResponse]
  total: int