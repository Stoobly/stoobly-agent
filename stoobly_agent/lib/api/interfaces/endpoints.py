from typing import List, TypedDict

from .pagination_query_params import PaginationQueryParams

class EndpointsIndexQueryParams(PaginationQueryParams):
  project_id: str

class RequestComponentName(TypedDict):
  alias_id: int
  name: str
  value: str

class Alias(TypedDict):
  id: int
  name: str

class ResponseParamName(RequestComponentName):
  query: str

class EndpointShowResponse(TypedDict):
  aliases: List[Alias]
  body_param_names: List[RequestComponentName]
  header_names: List[RequestComponentName]
  path_segment_names: List[RequestComponentName]
  query_param_names: List[RequestComponentName]
  response_param_names: List[ResponseParamName]