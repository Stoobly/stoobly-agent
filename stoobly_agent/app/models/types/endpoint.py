from typing import Literal, TypedDict

OPENAPI_FORMAT = 'openapi'

class EndpointCreateParams(TypedDict):
  format: Literal[f"{OPENAPI_FORMAT}"]
  path: str
