from typing import List, TypedDict

from stoobly_agent.app.models.schemas.request import Request

class RequestsModelIndex(TypedDict):
  list: List[Request]
  total: int