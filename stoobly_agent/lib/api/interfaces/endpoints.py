from typing import List, Optional, TypedDict

from .pagination_query_params import PaginationQueryParams

class EndpointsIndexQueryParams(PaginationQueryParams):
  project_id: str

class RequestComponentName(TypedDict):
  alias_id: int
  is_deterministic: bool
  is_required: bool
  name: str
  values: List[str] # Sample values for the component

class Alias(TypedDict):
  id: int
  name: str

class BodyParamName(RequestComponentName):
  inferred_type: str
  query: str

class ResponseParamName(RequestComponentName):
  inferred_type: str
  query: str

class EndpointShowResponse(TypedDict):
  method: str
  host: str
  port: str
  path: str
  match_pattern: Optional[str]
  aliases: List[Alias]
  body_param_names: List[BodyParamName]
  header_names: List[RequestComponentName]
  path_segment_names: List[RequestComponentName]
  query_param_names: List[RequestComponentName]
  response_param_names: List[ResponseParamName]

ARRAY_TYPE = 'Array'

