from stoobly_agent.app.models.adapters.joined_request_adapter import JoinedRequestAdapter
from stoobly_agent.app.models.adapters.snapshot.control_timestamp import format_control_timestamp
from stoobly_agent.app.proxy.record.request_string_control import RequestStringControl

from ..http_headers import parse_request_raw


class SnapshotRequestAdapter():
  """Adapt joined request bytes to snapshot request-entry fields (no nested response)."""

  def __init__(self, joined_request: bytes):
    self.__joined_request = joined_request

  def adapt(self) -> dict:
    adapter = JoinedRequestAdapter(self.__joined_request)
    request_string = adapter.build_request_string()
    control = RequestStringControl(request_string.control)
    method, url, http_version, headers = parse_request_raw(
      request_string.get(control=False)
    )
    return {
      'method': method,
      'url': url,
      'http_version': http_version,
      'timestamp': format_control_timestamp(control.timestamp),
      'headers': headers,
    }
