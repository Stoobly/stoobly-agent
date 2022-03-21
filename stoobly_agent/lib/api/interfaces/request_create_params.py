from typing import TypedDict

class RequestCreateParams(TypedDict):
  importer: str
  project_id: str
  requests: bytes
  scenario_id: str