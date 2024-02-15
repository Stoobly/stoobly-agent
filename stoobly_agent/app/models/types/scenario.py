from typing import TypedDict

class ScenarioCreateParams(TypedDict):
  description: str
  name: str
  priority: int
  uuid: str
  
class ScenarioDestroyParams(TypedDict):
  force: bool