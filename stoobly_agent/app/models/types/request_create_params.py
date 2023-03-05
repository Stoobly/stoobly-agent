from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow
from typing import TypedDict

from stoobly_agent.app.proxy.upload.joined_request import JoinedRequest

class RequestCreateParams(TypedDict):
  flow: MitmproxyHTTPFlow
  project_id: str
  joined_request: JoinedRequest
  scenario_id: str