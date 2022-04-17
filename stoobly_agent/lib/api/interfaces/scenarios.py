from typing import List, TypedDict

class ScenarioShowResponse(TypedDict):
  created_at: str
  description: str
  key: str
  name: str
  updated_at: str

class ScenariosIndexResponse(TypedDict):
  list: List[ScenarioShowResponse]
  total: int