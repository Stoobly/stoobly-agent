from typing import Literal, Optional, TypedDict

from stoobly_agent.app.models.types import OPENAPI_FORMAT

class EndpointCreateCliOptions(TypedDict):
  format: Optional[Literal[f"{OPENAPI_FORMAT}"]]
  lifecycle_hooks_path: Optional[str]
  path: str
  project_key: Optional[str]
  scenario_key: Optional[str]

