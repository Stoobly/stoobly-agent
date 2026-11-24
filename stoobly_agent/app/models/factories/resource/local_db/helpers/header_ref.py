import hashlib
import os
from typing import List, Set, Tuple

from stoobly_agent.config.constants.custom_headers import HEADER_REF

HEADER_REF_HEADER = HEADER_REF
HEADER_REF_HEADER_LOWER = HEADER_REF_HEADER.lower()
HEADER_SEP = b'\r\n'

REQUEST_HEADER_DEDUP_LIST: Set[str] = {
  'accept',
  'accept-encoding',
  'accept-language',
  'content-type',
  'origin',
  'referer',
  'sec-ch-ua',
  'sec-ch-ua-arch',
  'sec-ch-ua-bitness',
  'sec-ch-ua-form-factors',
  'sec-ch-ua-full-version',
  'sec-ch-ua-full-version-list',
  'sec-ch-ua-mobile',
  'sec-ch-ua-platform',
  'sec-ch-ua-platform-version',
  'sec-fetch-dest',
  'sec-fetch-mode',
  'sec-fetch-site',
  'user-agent',
}

RESPONSE_HEADER_DEDUP_LIST: Set[str] = {
  'access-control-allow-credentials',
  'access-control-allow-headers',
  'access-control-allow-methods',
  'access-control-allow-origin',
  'access-control-expose-headers',
  'cache-control',
  'content-encoding',
  'content-security-policy',
  'content-type',
  'cross-origin-opener-policy',
  'referrer-policy',
  'server',
  'strict-transport-security',
  'vary',
  'x-content-type-options',
  'x-frame-options',
}

# Truncated SHA-256 hex (64 bits) — short filenames under headers/
CONTENT_HASH_HEX_LEN = 16

def full_content_hash(payload: bytes) -> str:
  return hashlib.sha256(payload or b'').hexdigest()

def content_hash(payload: bytes) -> str:
  return full_content_hash(payload)[:CONTENT_HASH_HEX_LEN]

def headers_dir_path(slug_dir: str) -> str:
  return os.path.join(slug_dir, 'headers')

def header_file_path(slug_dir: str, hash_value: str) -> str:
  return os.path.join(headers_dir_path(slug_dir), hash_value)

def relative_header_ref(hash_value: str) -> str:
  return f"headers/{hash_value}"

def normalize_header_ref(ref: str) -> str:
  """
  Normalize a header ref to a relative headers/<...> path under slug_dir.

  Rejects absolute paths and '..' segments so joins cannot escape the slug dir.
  """
  normalized = (ref or '').replace('\\', '/').lstrip('/')
  if not normalized.startswith('headers/') or '..' in normalized.split('/'):
    raise ValueError(f"Invalid header ref: {ref}")
  return normalized

def _is_under_dir(path: str, parent: str) -> bool:
  """True if realpath(path) is parent or a descendant (follows symlinks)."""
  real_path = os.path.realpath(path)
  real_parent = os.path.realpath(parent)
  return real_path == real_parent or real_path.startswith(real_parent + os.sep)

def resolve_header_path(slug_dir: str, ref: str) -> str:
  """
  Resolve a validated header ref to a path under slug_dir/headers.

  After join, require realpath(path) stays under realpath(headers_dir) so a
  planted headers/<name> symlink cannot escape the slug tree.
  """
  path = os.path.join(slug_dir, normalize_header_ref(ref))
  headers_dir = headers_dir_path(slug_dir)
  if not _is_under_dir(headers_dir, slug_dir) or not _is_under_dir(path, headers_dir):
    raise ValueError(f"Invalid header ref: {ref}")
  return path

def write_headers(slug_dir: str, payload: bytes) -> str:
  """
  Write header bytes under headers/<hash16>. Returns the hash used in the filename.

  On truncated-hash collision (same short name, different bytes), falls back to
  the full SHA-256 hex filename so content is never silently reused.
  """
  data = payload or b''
  full_digest = full_content_hash(data)
  short_hash = full_digest[:CONTENT_HASH_HEX_LEN]
  headers_dir = headers_dir_path(slug_dir)
  os.makedirs(headers_dir, exist_ok=True)

  short_path = header_file_path(slug_dir, short_hash)
  if not os.path.exists(short_path):
    with open(short_path, 'wb') as fp:
      fp.write(data)
    return short_hash

  with open(short_path, 'rb') as fp:
    if fp.read() == data:
      return short_hash

  full_path = header_file_path(slug_dir, full_digest)
  if not os.path.exists(full_path):
    with open(full_path, 'wb') as fp:
      fp.write(data)
  return full_digest

def read_headers(slug_dir: str, ref: str) -> bytes:
  """Read headers from a relative headers/<hash> ref under slug_dir."""
  path = resolve_header_path(slug_dir, ref)
  with open(path, 'rb') as fp:
    return fp.read()

def _header_name(line: bytes) -> bytes:
  colon = line.find(b':')
  if colon < 0:
    return line
  return line[:colon].strip()

def _header_name_lower(line: bytes) -> str:
  return _header_name(line).decode('latin-1', errors='replace').lower()

def extract_dedup_list_headers(
  header_lines: List[bytes],
  dedup_list: Set[str],
) -> Tuple[List[bytes], bytes, int]:
  """
  Split header lines into remaining (non-dedup-list) and extracted dedup-list bytes.

  Appearance order among extracted lines is preserved. Missing dedup-list names
  are omitted (not written as empty placeholders).

  Returns (remaining_lines, extracted_bytes, insert_index) where insert_index is
  the position in remaining_lines at which the first dedup-list header was
  removed (0 if none extracted). Callers should insert Header-Ref there so
  reconstitution restores a contiguous dedup-list block in its original place.
  """
  remaining: List[bytes] = []
  extracted: List[bytes] = []
  insert_index = 0
  for line in header_lines:
    if not line:
      remaining.append(line)
      continue
    if _header_name_lower(line) in dedup_list:
      if not extracted:
        insert_index = len(remaining)
      extracted.append(line)
    else:
      remaining.append(line)

  if not extracted:
    return remaining, b'', 0

  return remaining, HEADER_SEP.join(extracted), insert_index
