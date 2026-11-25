from typing import Dict, List, Tuple, Union

from stoobly_agent.app.models.adapters.raw_http_request_adapter import RawHttpRequestAdapter
from stoobly_agent.app.models.adapters.raw_http_response_adapter import RawHttpResponseAdapter
from stoobly_agent.lib.utils.decode import decode

HEADER_SEP = b'\r\n'
HEADER_BODY_SEP = b'\r\n\r\n'
HEADER_COOKIE = 'cookie'
HEADER_SET_COOKIE = 'set-cookie'
HEADER_COOKIE_SEPARATOR = '; '
HEADER_SEPARATOR = ', '


def split_head_body(raw: bytes) -> Tuple[bytes, bytes]:
  idx = raw.find(HEADER_BODY_SEP)
  if idx < 0:
    return raw, b''
  return raw[:idx], raw[idx + len(HEADER_BODY_SEP):]


def header_lines_to_string(lines: List[bytes]) -> str:
  """Join raw header lines into a YAML-friendly multiline string (LF separators)."""
  parts: List[str] = []
  for line in lines:
    if not line:
      continue
    parts.append(decode(line).rstrip('\r'))
  return '\n'.join(parts)


def header_lines_to_dict(lines: List[bytes]) -> dict:
  # Values are str, or List[str] for repeated Set-Cookie (must not be combined).
  headers: Dict[str, Union[str, List[str]]] = {}
  for line in lines:
    if not line:
      continue
    colon = line.find(b':')
    if colon < 0:
      continue
    name = decode(line[:colon]).strip()
    value = decode(line[colon + 1:]).strip()
    if name in headers:
      lower = name.lower()
      if lower == HEADER_SET_COOKIE:
        existing = headers[name]
        if isinstance(existing, list):
          existing.append(value)
        else:
          headers[name] = [existing, value]
      else:
        separator = HEADER_COOKIE_SEPARATOR if lower == HEADER_COOKIE else HEADER_SEPARATOR
        headers[name] = separator.join([headers[name], value])
    else:
      headers[name] = value
  return headers


def strip_http_prefix(protocol: Union[str, bytes, None]) -> str:
  text = decode(protocol) if isinstance(protocol, (bytes, bytearray)) else str(protocol or 'HTTP/1.1')
  if text.upper().startswith('HTTP/'):
    return text.split('/', 1)[1]
  return text or '1.1'


def parse_request_raw(raw: bytes) -> Tuple[str, str, str, str]:
  head, _body = split_head_body(raw)
  lines = head.split(HEADER_SEP)
  if not lines:
    return 'GET', '/', '1.1', ''

  parsed = RawHttpRequestAdapter(lines[0] + HEADER_BODY_SEP)
  headers = header_lines_to_string(lines[1:])
  return parsed.method, parsed.url, strip_http_prefix(parsed.protocol), headers


def parse_response_raw(raw: bytes) -> Tuple[int, str, dict]:
  head, _body = split_head_body(raw)
  lines = head.split(HEADER_SEP)
  if not lines:
    return 0, '1.1', {}

  parsed = RawHttpResponseAdapter(lines[0] + HEADER_BODY_SEP)
  headers = header_lines_to_dict(lines[1:])
  return parsed.status, strip_http_prefix(parsed.protocol), headers
