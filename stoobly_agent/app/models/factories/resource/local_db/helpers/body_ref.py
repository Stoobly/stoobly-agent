import hashlib
import os
from typing import List, Optional, Tuple
from urllib.parse import urlparse

from stoobly_agent.app.models.adapters.joined_request_adapter import JoinedRequestAdapter
from stoobly_agent.app.models.adapters.raw_http_request_adapter import RawHttpRequestAdapter
from stoobly_agent.app.proxy.record.joined_request import REQUEST_DELIMITTER
from stoobly_agent.app.proxy.record.request_string import CLRF as RequestStringCLRF
from stoobly_agent.app.proxy.record.response_string import CLRF as ResponseStringCLRF
from stoobly_agent.config.constants.custom_headers import BODY_REF

BODY_REF_HEADER = BODY_REF
BODY_REF_HEADER_LOWER = BODY_REF_HEADER.lower()
HEADER_SEP = b'\r\n'
HEADER_BODY_SEP = b'\r\n\r\n'

def content_hash(body: bytes) -> str:
  return hashlib.sha256(body or b'').hexdigest()

def bodies_dir_path(slug_dir: str) -> str:
  return os.path.join(slug_dir, 'bodies')

def body_file_path(slug_dir: str, hash_value: str) -> str:
  return os.path.join(bodies_dir_path(slug_dir), hash_value)

def relative_body_ref(hash_value: str) -> str:
  return f"bodies/{hash_value}"

def normalize_body_ref(ref: str) -> str:
  """
  Normalize a body ref to a relative bodies/<...> path under slug_dir.

  Rejects absolute paths and '..' segments so joins cannot escape the slug dir.
  """
  normalized = (ref or '').replace('\\', '/').lstrip('/')
  if not normalized.startswith('bodies/') or '..' in normalized.split('/'):
    raise ValueError(f"Invalid body ref: {ref}")
  return normalized

def _is_under_dir(path: str, parent: str) -> bool:
  """True if realpath(path) is parent or a descendant (follows symlinks)."""
  real_path = os.path.realpath(path)
  real_parent = os.path.realpath(parent)
  return real_path == real_parent or real_path.startswith(real_parent + os.sep)

def resolve_body_path(slug_dir: str, ref: str) -> str:
  """
  Resolve a validated body ref to a path under slug_dir/bodies.

  After join, require realpath(path) stays under realpath(bodies_dir) so a
  planted bodies/<name> symlink cannot escape the slug tree.
  """
  path = os.path.join(slug_dir, normalize_body_ref(ref))
  bodies_dir = bodies_dir_path(slug_dir)
  if not _is_under_dir(bodies_dir, slug_dir) or not _is_under_dir(path, bodies_dir):
    raise ValueError(f"Invalid body ref: {ref}")
  return path

def write_body(slug_dir: str, body: bytes) -> str:
  """Write body bytes under bodies/<sha256>. Returns content hash."""
  hash_value = content_hash(body)
  bodies_dir = bodies_dir_path(slug_dir)
  os.makedirs(bodies_dir, exist_ok=True)
  path = body_file_path(slug_dir, hash_value)
  if not os.path.exists(path):
    with open(path, 'wb') as fp:
      fp.write(body)
  return hash_value

def read_body(slug_dir: str, ref: str) -> bytes:
  """Read body from a relative bodies/<hash> ref under slug_dir."""
  path = resolve_body_path(slug_dir, ref)
  with open(path, 'rb') as fp:
    return fp.read()

def externalize_joined_request(joined: bytes, slug_dir: str) -> bytes:
  """
  Convert joined request bytes to v2 form: strip bodies, write them under
  slug_dir/bodies, and append X-Stoobly-Body-Ref as the last header.
  """
  adapter = JoinedRequestAdapter(joined)
  request_string = adapter.build_request_string()
  response_string = adapter.build_response_string()

  request_raw = _externalize_http(request_string.get(control=False), slug_dir)
  response_raw = _externalize_http(response_string.get(control=False), slug_dir)

  request_part = request_string.control + RequestStringCLRF + request_raw
  response_part = response_string.control + ResponseStringCLRF + response_raw

  return REQUEST_DELIMITTER.join([request_part, response_part])

def reconstitute_joined_request(joined: bytes, slug_dir: str) -> bytes:
  """
  Convert v2 joined request bytes back to inline-body form by resolving
  X-Stoobly-Body-Ref headers relative to slug_dir.
  """
  adapter = JoinedRequestAdapter(joined)
  request_string = adapter.build_request_string()
  response_string = adapter.build_response_string()

  request_raw = _reconstitute_http(request_string.get(control=False), slug_dir)
  response_raw = _reconstitute_http(response_string.get(control=False), slug_dir)

  request_part = request_string.control + RequestStringCLRF + request_raw
  response_part = response_string.control + ResponseStringCLRF + response_raw

  return REQUEST_DELIMITTER.join([request_part, response_part])

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

def _externalize_http(raw: bytes, slug_dir: str) -> bytes:
  head, body = _split_head_body(raw)

  # No body: leave bytes unchanged for round-trip fidelity
  if not body:
    return raw

  lines = head.split(HEADER_SEP)
  if not lines:
    return raw

  start_line = lines[0]
  header_lines = _drop_headers(lines[1:], {BODY_REF_HEADER_LOWER})
  header_lines = _set_or_add_content_length(header_lines, 0)

  hash_value = write_body(slug_dir, body)
  # Body-ref must be the last header
  header_lines.append(f"{BODY_REF_HEADER}: {relative_body_ref(hash_value)}".encode())

  return HEADER_SEP.join([start_line] + header_lines) + HEADER_BODY_SEP

def _reconstitute_http(raw: bytes, slug_dir: str) -> bytes:
  head, _body = _split_head_body(raw)
  lines = head.split(HEADER_SEP)
  if not lines:
    return raw

  start_line = lines[0]
  header_lines = lines[1:]
  ref = _find_header_value(header_lines, BODY_REF_HEADER_LOWER)

  if not ref:
    return raw

  restored_body = read_body(slug_dir, ref)
  header_lines = _drop_headers(header_lines, {BODY_REF_HEADER_LOWER})
  header_lines = _set_or_add_content_length(header_lines, len(restored_body))

  return HEADER_SEP.join([start_line] + header_lines) + HEADER_BODY_SEP + restored_body

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
