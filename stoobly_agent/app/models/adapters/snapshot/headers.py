from typing import List, Optional, Union

HEADER_SEP = b'\r\n'
HEADER_BODY_SEP = b'\r\n\r\n'


def format_http_version(version: Optional[Union[str, int, float]]) -> str:
  if version is None or version == '':
    return 'HTTP/1.1'
  text = str(version)
  if text.upper().startswith('HTTP/'):
    return text
  return f"HTTP/{text}"


def headers_dict_to_lines(headers: Union[dict, None]) -> List[bytes]:
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


def headers_string_to_lines(headers: Union[str, None]) -> List[bytes]:
  """Split a multiline header block into HTTP header lines."""
  if not isinstance(headers, str) or not headers.strip():
    return []
  lines: List[bytes] = []
  for line in headers.splitlines():
    if line.strip():
      lines.append(line.encode())
  return lines


def headers_to_lines(headers: Union[str, dict, None]) -> List[bytes]:
  """Accept request header string or legacy/response header dict."""
  if isinstance(headers, str):
    return headers_string_to_lines(headers)
  return headers_dict_to_lines(headers)


def join_start_and_headers(start_line: bytes, header_lines: List[bytes]) -> bytes:
  if header_lines:
    return start_line + HEADER_SEP + HEADER_SEP.join(header_lines) + HEADER_BODY_SEP
  return start_line + HEADER_BODY_SEP
