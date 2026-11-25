import hashlib
import os
from typing import Optional

from stoobly_agent.config.constants.custom_headers import BODY_REF
from stoobly_agent.config.data_dir import DATA_DIR_NAME

BODY_REF_HEADER = BODY_REF
BODY_REF_HEADER_LOWER = BODY_REF_HEADER.lower()
# Truncated SHA-256 hex (64 bits) — short filenames under bodies/
CONTENT_HASH_HEX_LEN = 16

# Context-dir-relative (PR-readable): .stoobly/snapshots/requests/<slug>/bodies/<hash>
_REF_ROOT_PARTS = (DATA_DIR_NAME, 'snapshots', 'requests')
_REF_KIND = 'bodies'

def full_content_hash(body: bytes) -> str:
  return hashlib.sha256(body or b'').hexdigest()

def content_hash(body: bytes) -> str:
  return full_content_hash(body)[:CONTENT_HASH_HEX_LEN]

def bodies_dir_path(slug_dir: str) -> str:
  return os.path.join(slug_dir, 'bodies')

def body_file_path(slug_dir: str, hash_value: str) -> str:
  return os.path.join(bodies_dir_path(slug_dir), hash_value)

def relative_body_ref(slug: str, hash_value: str) -> str:
  """
  Context-dir-relative body ref for YAML / PR navigation:

    .stoobly/snapshots/requests/<slug>/bodies/<hash>
  """
  _validate_slug(slug)
  if not hash_value or '/' in hash_value or '\\' in hash_value or '..' in hash_value:
    raise ValueError(f"Invalid body hash: {hash_value}")
  return f"{DATA_DIR_NAME}/snapshots/requests/{slug}/bodies/{hash_value}"

def is_body_ref(ref: str) -> bool:
  """True if ref looks like a context-relative body ref."""
  try:
    normalize_body_ref(ref)
    return True
  except ValueError:
    return False

def normalize_body_ref(ref: str, slug: Optional[str] = None) -> str:
  """
  Normalize to .stoobly/snapshots/requests/<slug>/bodies/<hash>.

  Rejects absolute paths and '..' segments. When slug is provided, the ref's
  slug segment must match.
  """
  normalized = (ref or '').replace('\\', '/').lstrip('/')
  if not normalized or '..' in normalized.split('/'):
    raise ValueError(f"Invalid body ref: {ref}")

  parts = normalized.split('/')
  if (
    len(parts) != 6
    or tuple(parts[:3]) != _REF_ROOT_PARTS
    or parts[4] != _REF_KIND
    or not parts[3]
    or not parts[5]
  ):
    raise ValueError(f"Invalid body ref: {ref}")

  if slug is not None and parts[3] != slug:
    raise ValueError(f"Invalid body ref: {ref}")

  return normalized

def _validate_slug(slug: str):
  if not slug or '/' in slug or '\\' in slug or slug in ('.', '..'):
    raise ValueError(f"Invalid slug: {slug}")

def _is_under_dir(path: str, parent: str) -> bool:
  """True if realpath(path) is parent or a descendant (follows symlinks)."""
  real_path = os.path.realpath(path)
  real_parent = os.path.realpath(parent)
  return real_path == real_parent or real_path.startswith(real_parent + os.sep)

def resolve_body_path(slug_dir: str, ref: str) -> str:
  """
  Resolve a body ref to a path under slug_dir/bodies.

  Refs must be .stoobly/snapshots/requests/<slug>/bodies/<hash> with <slug>
  equal to this slug_dir's basename. After join, require realpath(path) stays
  under realpath(bodies_dir) so a planted bodies/<name> symlink cannot escape.
  """
  slug = os.path.basename(os.path.normpath(slug_dir))
  normalized = normalize_body_ref(ref, slug=slug)
  hash_value = normalized.rsplit('/', 1)[-1]
  path = body_file_path(slug_dir, hash_value)
  bodies_dir = bodies_dir_path(slug_dir)
  if not _is_under_dir(bodies_dir, slug_dir) or not _is_under_dir(path, bodies_dir):
    raise ValueError(f"Invalid body ref: {ref}")
  return path

def write_body(slug_dir: str, body: bytes) -> str:
  """
  Write body bytes under bodies/<hash16>. Returns the hash used in the filename.

  On truncated-hash collision (same short name, different bytes), falls back to
  the full SHA-256 hex filename so content is never silently reused.
  """
  payload = body or b''
  full_digest = full_content_hash(payload)
  short_hash = full_digest[:CONTENT_HASH_HEX_LEN]
  bodies_dir = bodies_dir_path(slug_dir)
  os.makedirs(bodies_dir, exist_ok=True)

  short_path = body_file_path(slug_dir, short_hash)
  if not os.path.exists(short_path):
    with open(short_path, 'wb') as fp:
      fp.write(payload)
    return short_hash

  with open(short_path, 'rb') as fp:
    if fp.read() == payload:
      return short_hash

  full_path = body_file_path(slug_dir, full_digest)
  if not os.path.exists(full_path):
    with open(full_path, 'wb') as fp:
      fp.write(payload)
  return full_digest

def read_body(slug_dir: str, ref: str) -> bytes:
  """Read body from a context-relative ref under slug_dir."""
  path = resolve_body_path(slug_dir, ref)
  with open(path, 'rb') as fp:
    return fp.read()
