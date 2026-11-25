from typing import Optional

from stoobly_agent.app.proxy.record.request_string import CLRF as RequestStringCLRF
from stoobly_agent.app.proxy.record.request_string_control import RequestStringControl

from ..control_timestamp import parse_control_timestamp
from ..headers import format_http_version, headers_to_lines, join_start_and_headers


class RawRequestAdapter():
  """
  Adapt a snapshot request entry (method/url/http_version/timestamp/headers) to a
  Stoobly request string: control line + CRLF + raw HTTP request.

  `headers` is a multiline string (raw header block). Legacy dict maps are still
  accepted for older YAML.
  """

  def __init__(self, entry: dict, uuid: Optional[str] = None):
    if not isinstance(entry, dict):
      raise ValueError('request entry must be a dict')
    self.__entry = entry
    self.__uuid = str(uuid or '')

  def adapt(self) -> bytes:
    entry = self.__entry

    control = RequestStringControl()
    control.id = self.__uuid
    control.timestamp = parse_control_timestamp(entry.get('timestamp'))

    method = entry.get('method') or 'GET'
    url = entry.get('url') or '/'
    version = format_http_version(entry.get('http_version'))
    request_line = f"{method} {url} {version}".encode()

    headers = headers_to_lines(entry.get('headers'))
    request_raw = join_start_and_headers(request_line, headers)
    return control.serialize().encode() + RequestStringCLRF + request_raw
