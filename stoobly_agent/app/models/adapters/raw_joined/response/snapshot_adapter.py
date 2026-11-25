from stoobly_agent.app.models.adapters.joined_request_adapter import JoinedRequestAdapter
from stoobly_agent.app.models.adapters.snapshot.control_timestamp import (
  coerce_legacy_us_to_ns,
  format_control_timestamp,
)
from stoobly_agent.app.proxy.record.response_string_control import ResponseStringControl

from ..http_headers import parse_response_raw


class SnapshotResponseAdapter():
  """Adapt joined request bytes to the nested snapshot `response` dict."""

  def __init__(self, joined_request: bytes):
    self.__joined_request = joined_request

  def adapt(self) -> dict:
    adapter = JoinedRequestAdapter(self.__joined_request)
    response_string = adapter.build_response_string()
    control = ResponseStringControl(response_string.control)
    status, http_version, headers = parse_response_raw(
      response_string.get(control=False)
    )
    return {
      'status': status,
      'latency': control.latency,
      'http_version': http_version,
      'timestamp': format_control_timestamp(
        coerce_legacy_us_to_ns(control.timestamp)
      ),
      'headers': headers,
    }
