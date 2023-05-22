from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow
from typing import TypedDict

from stoobly_agent.app.proxy.record.joined_request import JoinedRequest

class RequestCreateParams(TypedDict):
  flow: MitmproxyHTTPFlow
  project_id: str
  joined_request: JoinedRequest
  scenario_id: str

class RequestDestroyParams(TypedDict):
  force: bool

class RequestFindParams(TypedDict):
  host: str
  port: str
  method: str
  pattern: str

class RequestShowParams(TypedDict):
  body: bool
  headers: bool
  project_id: str
  query_params: bool
  response: bool

