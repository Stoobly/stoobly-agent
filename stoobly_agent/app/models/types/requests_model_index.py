from typing import List, TypedDict

from stoobly_agent.lib.models.schemas.request import Request

class RequestsModelIndex(TypedDict):
  list: List[Request]
  total: int