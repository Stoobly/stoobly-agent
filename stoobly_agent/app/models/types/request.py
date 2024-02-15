from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow
from typing import List, Optional, TypedDict

from stoobly_agent.app.proxy.record.joined_request import JoinedRequest

class RequestCreateParams(TypedDict):
  flow: MitmproxyHTTPFlow
  project_id: str
  joined_request: JoinedRequest
  scenario_id: str
  uuid: str

class RequestDestroyParams(TypedDict):
  force: bool

class RequestDestroyAllParams(TypedDict):
  ids: List[int] 
  scenario_id: int

class RequestIndexSimilarParams(TypedDict):
  host: str
  port: str
  method: str
  pattern: str
  scenario_id: Optional[int]

class RequestShowParams(TypedDict):
  body: bool
  headers: bool
  project_id: str
  query_params: bool
  response: bool

