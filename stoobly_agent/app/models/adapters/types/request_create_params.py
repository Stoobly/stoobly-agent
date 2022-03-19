from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow
from typing import TypedDict

class RequestCreateParams(TypedDict):
  flow: MitmproxyHTTPFlow
  project_id: str
  requests: bytes
  scenario_id: str