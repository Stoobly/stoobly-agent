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

class RequestShowParams(TypedDict):
  body: bool
  headers: bool
  project_id: str
  query_params: bool
  response: bool