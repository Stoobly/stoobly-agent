from typing import Any, Dict, List, Optional, Tuple, Union

from stoobly_agent.app.models.adapters.joined_request_adapter import JoinedRequestAdapter
from stoobly_agent.app.models.adapters.raw_http_request_adapter import RawHttpRequestAdapter
from stoobly_agent.app.models.adapters.raw_http_response_adapter import RawHttpResponseAdapter
from stoobly_agent.app.proxy.record.joined_request import REQUEST_DELIMITTER
from stoobly_agent.app.proxy.record.request_string import CLRF as RequestStringCLRF
from stoobly_agent.app.proxy.record.request_string_control import RequestStringControl
from stoobly_agent.app.proxy.record.response_string import CLRF as ResponseStringCLRF
from stoobly_agent.app.proxy.record.response_string_control import ResponseStringControl
from stoobly_agent.config.constants.custom_headers import BODY_REF, HEADER_REF
from stoobly_agent.lib.utils.decode import decode

from .joined_request_ref import externalize_joined_request, reconstitute_joined_request
from .snapshot_format import UUID_RE

HEADER_SEP = b'\r\n'
HEADER_BODY_SEP = b'\r\n\r\n'
HEADER_COOKIE = 'cookie'
HEADER_COOKIE_SEPARATOR = '; '
HEADER_SEPARATOR = ', '


def joined_to_entry(
  joined: bytes,
  slug_dir: str,
  uuid: str = None,
) -> dict:
  """
  Externalize bodies/headers under slug_dir, then parse into a structured YAML entry.

  `uuid` is accepted for control-line fidelity when rebuilding later but is **not**
  stored in the entry (standalone files use the filename; scenario embeds use the dict key).
  """
  externalized = externalize_joined_request(joined, slug_dir)
  adapter = JoinedRequestAdapter(externalized)
  request_string = adapter.build_request_string()
  response_string = adapter.build_response_string()

  req_control = RequestStringControl(request_string.control)
  res_control = ResponseStringControl(response_string.control)

  req_raw = request_string.get(control=False)
  res_raw = response_string.get(control=False)

  method, url, req_http_version, req_headers = _parse_request_raw(req_raw)
  status, res_http_version, res_headers = _parse_response_raw(res_raw)

  return {
    'method': method,
    'url': url,
    'http_version': req_http_version,
    'timestamp': req_control.timestamp,
    'headers': req_headers,
    'response': {
      'status': status,
      'latency': res_control.latency,
      'http_version': res_http_version,
      'timestamp': res_control.timestamp,
      'headers': res_headers,
    },
  }


def entry_to_joined(entry: dict, slug_dir: str, uuid: str = None) -> bytes:
  """
  Rebuild joined request bytes from a structured entry, then reconstitute refs.

  `uuid` is the request identity used in Stoobly control lines (from filename or
  scenario dict key) — not a field on the entry itself.
  """
  if not isinstance(entry, dict):
    raise ValueError('request entry must be a dict')

  response = entry.get('response') or {}
  if not isinstance(response, dict):
    raise ValueError('response must be a dict')

  entry_uuid = str(uuid or '')
  req_timestamp = entry.get('timestamp')
  res_timestamp = response.get('timestamp')

  req_control = RequestStringControl()
  req_control.id = entry_uuid
  req_control.timestamp = int(req_timestamp) if req_timestamp is not None else 0

  res_control = ResponseStringControl()
  res_control.id = entry_uuid
  res_control.timestamp = int(res_timestamp) if res_timestamp is not None else 0
  res_control.latency = int(response.get('latency') or 0)

  method = entry.get('method') or 'GET'
  url = entry.get('url') or '/'
  req_version = _format_http_version(entry.get('http_version'))
  request_line = f"{method} {url} {req_version}".encode()

  res_version = _format_http_version(response.get('http_version'))
  status = int(response.get('status') or 0)
  response_line = f"{res_version} {status}".encode()

  req_headers = _headers_dict_to_lines(entry.get('headers') or {})
  res_headers = _headers_dict_to_lines(response.get('headers') or {})

  request_raw = _join_start_and_headers(request_line, req_headers)
  response_raw = _join_start_and_headers(response_line, res_headers)

  request_part = req_control.serialize().encode() + RequestStringCLRF + request_raw
  response_part = res_control.serialize().encode() + ResponseStringCLRF + response_raw
  joined = REQUEST_DELIMITTER.join([request_part, response_part])
  return reconstitute_joined_request(joined, slug_dir)


def entry_ref_paths(entry: dict) -> List[str]:
  """Collect relative body/header refs from an entry's header maps."""
  refs: List[str] = []
  if not isinstance(entry, dict):
    return refs

  for headers in (entry.get('headers'), (entry.get('response') or {}).get('headers')):
    if not isinstance(headers, dict):
      continue
    for name, value in headers.items():
      lower = str(name).lower()
      if lower in (BODY_REF.lower(), HEADER_REF.lower()) and value:
        refs.append(str(value).strip())
  return refs


def is_request_entry(value: Any) -> bool:
  """True if value looks like a structured request YAML entry (not a path string)."""
  return (
    isinstance(value, dict)
    and 'headers' in value
    and 'response' in value
    and 'method' in value
  )


def iter_scenario_request_entries(requests_field: Any):
  """
  Yield (uuid, entry) from scenario YAML `requests`.

  Current form is a uuid-keyed dict. Also accepts a legacy list of entries that
  still embedded `uuid` (entry returned without that field).
  """
  if isinstance(requests_field, dict):
    for request_uuid, entry in requests_field.items():
      if is_request_entry(entry) and UUID_RE.match(str(request_uuid)):
        yield str(request_uuid), entry
    return

  if not isinstance(requests_field, list):
    return

  for item in requests_field:
    if not is_request_entry(item):
      continue
    request_uuid = str(item.get('uuid') or '')
    if not UUID_RE.match(request_uuid):
      continue
    yield request_uuid, {k: v for k, v in item.items() if k != 'uuid'}


def _parse_request_raw(raw: bytes) -> Tuple[str, str, str, dict]:
  head, _body = _split_head_body(raw)
  lines = head.split(HEADER_SEP)
  if not lines:
    return 'GET', '/', '1.1', {}

  parsed = RawHttpRequestAdapter(lines[0] + HEADER_BODY_SEP)
  headers = _header_lines_to_dict(lines[1:])
  return parsed.method, parsed.url, _strip_http_prefix(parsed.protocol), headers


def _parse_response_raw(raw: bytes) -> Tuple[int, str, dict]:
  head, _body = _split_head_body(raw)
  lines = head.split(HEADER_SEP)
  if not lines:
    return 0, '1.1', {}

  parsed = RawHttpResponseAdapter(lines[0] + HEADER_BODY_SEP)
  headers = _header_lines_to_dict(lines[1:])
  return parsed.status, _strip_http_prefix(parsed.protocol), headers


def _split_head_body(raw: bytes) -> Tuple[bytes, bytes]:
  idx = raw.find(HEADER_BODY_SEP)
  if idx < 0:
    return raw, b''
  return raw[:idx], raw[idx + len(HEADER_BODY_SEP):]


def _header_lines_to_dict(lines: List[bytes]) -> dict:
  headers: Dict[str, str] = {}
  for line in lines:
    if not line:
      continue
    colon = line.find(b':')
    if colon < 0:
      continue
    name = decode(line[:colon]).strip()
    value = decode(line[colon + 1:]).strip()
    if name in headers:
      separator = HEADER_COOKIE_SEPARATOR if name.lower() == HEADER_COOKIE else HEADER_SEPARATOR
      headers[name] = separator.join([headers[name], value])
    else:
      headers[name] = value
  return headers


def _headers_dict_to_lines(headers: Union[dict, None]) -> List[bytes]:
  lines: List[bytes] = []
  if not isinstance(headers, dict):
    return lines
  for name, value in headers.items():
    if value is None:
      continue
    if isinstance(value, list):
      for item in value:
        lines.append(f"{name}: {item}".encode())
    else:
      lines.append(f"{name}: {value}".encode())
  return lines


def _join_start_and_headers(start_line: bytes, header_lines: List[bytes]) -> bytes:
  if header_lines:
    return start_line + HEADER_SEP + HEADER_SEP.join(header_lines) + HEADER_BODY_SEP
  return start_line + HEADER_BODY_SEP


def _strip_http_prefix(protocol: Union[str, bytes, None]) -> str:
  text = decode(protocol) if isinstance(protocol, (bytes, bytearray)) else str(protocol or 'HTTP/1.1')
  if text.upper().startswith('HTTP/'):
    return text.split('/', 1)[1]
  return text or '1.1'


def _format_http_version(version: Optional[Union[str, int, float]]) -> str:
  if version is None or version == '':
    return 'HTTP/1.1'
  text = str(version)
  if text.upper().startswith('HTTP/'):
    return text
  return f"HTTP/{text}"
