from typing import Literal, TypedDict

OPENAPI_FORMAT = 'open-api'

class EndpointCreateParams(TypedDict):
  format: Literal[f"{OPENAPI_FORMAT}"]
  path: str
