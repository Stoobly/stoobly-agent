from typing import List, Optional, TypedDict, Union

from .pagination_query_params import PaginationQueryParams

class EndpointsIndexQueryParams(PaginationQueryParams):
  ignored_components: str
  method: str
  project_id: str
  q: str

class RequestComponentName(TypedDict):
  id: int 
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
  body_param_name_id: Union[int, None]

class ResponseParamName(RequestComponentName):
  inferred_type: str
  query: str

class EndpointShowResponse(TypedDict):
  id: int
  method: str
  host: str
  ignored_components: Optional[list]
  port: str
  path: str
  match_pattern: Optional[str]
  aliases: List[Alias]
  body_param_names: List[BodyParamName]
  header_names: List[RequestComponentName]
  path_segment_names: List[RequestComponentName]
  query_param_names: List[RequestComponentName]
  response_param_names: List[ResponseParamName]
  response_header_names: List[RequestComponentName]
  literal_query_params: Optional[dict]
  literal_body_params: Optional[dict]
  literal_response_params: Optional[dict]

ARRAY_TYPE = 'Array'

