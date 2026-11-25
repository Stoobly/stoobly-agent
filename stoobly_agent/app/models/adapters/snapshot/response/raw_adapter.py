from typing import Optional

from stoobly_agent.app.proxy.record.response_string import CLRF as ResponseStringCLRF
from stoobly_agent.app.proxy.record.response_string_control import ResponseStringControl

from ..control_timestamp import coerce_legacy_us_to_ns, parse_control_timestamp
from ..headers import format_http_version, headers_to_lines, join_start_and_headers


class RawResponseAdapter():
  """
  Adapt a snapshot response dict (status/latency/http_version/timestamp/headers) to a
  Stoobly response string: control line + CRLF + raw HTTP response.

  `headers` is a multiline string (raw header block). Legacy dict maps are still
  accepted for older YAML.
  """

  def __init__(self, response: dict, uuid: Optional[str] = None):
    if not isinstance(response, dict):
      raise ValueError('response must be a dict')
    self.__response = response
    self.__uuid = str(uuid or '')

  def adapt(self) -> bytes:
    response = self.__response

    control = ResponseStringControl()
    control.id = self.__uuid
    # Coerce legacy µs ints so rewritten control lines are nanoseconds.
    control.timestamp = coerce_legacy_us_to_ns(
      parse_control_timestamp(response.get('timestamp'))
    )
    control.latency = int(response.get('latency') or 0)

    version = format_http_version(response.get('http_version'))
    status = int(response.get('status') or 0)
    # Match ResponseString: "HTTP/x STATUS" with no trailing reason/space.
    response_line = f"{version} {status}".encode()

    headers = headers_to_lines(response.get('headers'))
    response_raw = join_start_and_headers(response_line, headers)
    return control.serialize().encode() + ResponseStringCLRF + response_raw
