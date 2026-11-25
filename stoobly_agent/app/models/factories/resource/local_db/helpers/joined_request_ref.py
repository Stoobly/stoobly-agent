import os
from typing import List, Optional, Set, Tuple
from urllib.parse import urlparse

from stoobly_agent.app.models.adapters.joined_request_adapter import JoinedRequestAdapter
from stoobly_agent.app.models.adapters.raw_http_request_adapter import RawHttpRequestAdapter
from stoobly_agent.app.proxy.record.joined_request import REQUEST_DELIMITTER
from stoobly_agent.app.proxy.record.request_string import CLRF as RequestStringCLRF
from stoobly_agent.app.proxy.record.response_string import CLRF as ResponseStringCLRF

from .body_ref import (
  BODY_REF_HEADER,
  BODY_REF_HEADER_LOWER,
  read_body,
  relative_body_ref,
  write_body,
)
from .header_ref import (
  HEADER_REF_HEADER,
  HEADER_REF_HEADER_LOWER,
  REQUEST_HEADER_DEDUP_LIST,
  RESPONSE_HEADER_DEDUP_LIST,
  extract_dedup_list_headers,
  read_headers,
  relative_header_ref,
  write_headers,
)

HEADER_SEP = b'\r\n'
HEADER_BODY_SEP = b'\r\n\r\n'

def externalize_joined_request(joined: bytes, slug_dir: str) -> bytes:
  """
  Convert joined request bytes to v2 form: strip dedup-list headers and bodies,
  write them under slug_dir/headers and slug_dir/bodies, and append
  X-Stoobly-Header-Ref / X-Stoobly-Body-Ref (body-ref last when both exist).

  Refs are context-dir-relative for PR navigation:
  .stoobly/snapshots/requests/<slug>/bodies|headers/<hash>
  """
  adapter = JoinedRequestAdapter(joined)
  request_string = adapter.build_request_string()
  response_string = adapter.build_response_string()
  slug = os.path.basename(os.path.normpath(slug_dir))

  request_raw = _externalize_http(
    request_string.get(control=False), slug_dir, slug, REQUEST_HEADER_DEDUP_LIST
  )
  response_raw = _externalize_http(
    response_string.get(control=False), slug_dir, slug, RESPONSE_HEADER_DEDUP_LIST
  )

  request_part = request_string.control + RequestStringCLRF + request_raw
  response_part = response_string.control + ResponseStringCLRF + response_raw

  return REQUEST_DELIMITTER.join([request_part, response_part])

def reconstitute_joined_request(joined: bytes, slug_dir: str) -> bytes:
  """
  Convert v2 joined request bytes back to inline form by resolving
  X-Stoobly-Header-Ref and X-Stoobly-Body-Ref against slug_dir
  (.stoobly/snapshots/requests/<slug>/bodies|headers/<hash>).
  """
  adapter = JoinedRequestAdapter(joined)
  request_string = adapter.build_request_string()
  response_string = adapter.build_response_string()

  request_raw = _reconstitute_http(request_string.get(control=False), slug_dir)
  response_raw = _reconstitute_http(response_string.get(control=False), slug_dir)

  request_part = request_string.control + RequestStringCLRF + request_raw
  response_part = response_string.control + ResponseStringCLRF + response_raw

  return REQUEST_DELIMITTER.join([request_part, response_part])

def extract_method_and_path_from_joined(joined: bytes) -> Tuple[str, str]:
  """Best-effort method + path from joined snapshot bytes (for migration)."""
  adapter = JoinedRequestAdapter(joined)
  request_string = adapter.build_request_string()
  raw = request_string.get(control=False)
  parsed = RawHttpRequestAdapter(raw)
  url = parsed.url or '/'
  if '://' in url:
    parsed_url = urlparse(url)
    path = parsed_url.path or '/'
  else:
    path = url.split('?', 1)[0] or '/'
  return parsed.method, path

def _split_head_body(raw: bytes) -> Tuple[bytes, bytes]:
  idx = raw.find(HEADER_BODY_SEP)
  if idx < 0:
    return raw, b''
  return raw[:idx], raw[idx + len(HEADER_BODY_SEP):]

def _header_name(line: bytes) -> bytes:
  colon = line.find(b':')
  if colon < 0:
    return line
  return line[:colon].strip()

def _header_name_lower(line: bytes) -> str:
  return _header_name(line).decode('latin-1', errors='replace').lower()

def _find_header_value(header_lines: List[bytes], name_lower: str) -> Optional[str]:
  for line in header_lines:
    if _header_name_lower(line) == name_lower:
      colon = line.find(b':')
      return line[colon + 1:].decode('latin-1', errors='replace').strip()
  return None

def _set_or_add_content_length(header_lines: List[bytes], length: int) -> List[bytes]:
  updated = []
  found = False
  for line in header_lines:
    if _header_name_lower(line) == 'content-length':
      updated.append(f"Content-Length: {length}".encode())
      found = True
    else:
      updated.append(line)
  if not found:
    updated.append(f"Content-Length: {length}".encode())
  return updated

def _drop_headers(header_lines: List[bytes], names_lower: set) -> List[bytes]:
  return [line for line in header_lines if _header_name_lower(line) not in names_lower]

def _parse_header_blob(payload: bytes) -> List[bytes]:
  if not payload:
    return []
  return [line for line in payload.split(HEADER_SEP) if line]

def _externalize_http(
  raw: bytes, slug_dir: str, slug: str, dedup_list: Set[str]
) -> bytes:
  head, body = _split_head_body(raw)

  lines = head.split(HEADER_SEP)
  if not lines:
    return raw

  start_line = lines[0]
  header_lines = _drop_headers(
    lines[1:],
    {BODY_REF_HEADER_LOWER, HEADER_REF_HEADER_LOWER},
  )

  header_lines, extracted_headers, header_ref_index = extract_dedup_list_headers(
    header_lines, dedup_list
  )
  if extracted_headers:
    header_hash = write_headers(slug_dir, extracted_headers)
    header_lines.insert(
      header_ref_index,
      f"{HEADER_REF_HEADER}: {relative_header_ref(slug, header_hash)}".encode(),
    )

  restored_body = body
  if body:
    body_hash = write_body(slug_dir, body)
    # Body-ref must be the last header
    header_lines.append(
      f"{BODY_REF_HEADER}: {relative_body_ref(slug, body_hash)}".encode()
    )
    restored_body = b''
  elif not extracted_headers:
    # No body and no dedup-list headers: leave bytes unchanged for round-trip fidelity
    return raw

  return HEADER_SEP.join([start_line] + header_lines) + HEADER_BODY_SEP + restored_body

def _reconstitute_http(raw: bytes, slug_dir: str) -> bytes:
  head, body = _split_head_body(raw)
  lines = head.split(HEADER_SEP)
  if not lines:
    return raw

  start_line = lines[0]
  header_lines = lines[1:]
  header_ref = _find_header_value(header_lines, HEADER_REF_HEADER_LOWER)
  body_ref = _find_header_value(header_lines, BODY_REF_HEADER_LOWER)

  if not header_ref and not body_ref:
    return raw

  restored_headers: List[bytes] = []
  if header_ref:
    restored_headers = _parse_header_blob(read_headers(slug_dir, header_ref))

  rebuilt: List[bytes] = []
  for line in header_lines:
    name = _header_name_lower(line)
    if name == HEADER_REF_HEADER_LOWER:
      rebuilt.extend(restored_headers)
    elif name == BODY_REF_HEADER_LOWER:
      continue
    else:
      rebuilt.append(line)

  restored_body = body
  if body_ref:
    restored_body = read_body(slug_dir, body_ref)
    rebuilt = _set_or_add_content_length(rebuilt, len(restored_body))

  return HEADER_SEP.join([start_line] + rebuilt) + HEADER_BODY_SEP + restored_body
