from typing import Literal, TypedDict

OPENAPI_FORMAT = 'openapi'

class EndpointCreateParams(TypedDict):
  host: str
  method: str
  path_segments: str
  path: str
  port: str
  project_id: str

class HeaderNameCreateParams(TypedDict):
  name: str
  is_required: bool
  is_deterministic: bool
  project_id: str
  endpoint_id: int
	
class ParamNameCreateParams(TypedDict):
	name: str
	project_id: str
	endpoint_id: int
	inferred_type: str
	query: str
