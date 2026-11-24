import hashlib
import os

from stoobly_agent.config.constants.custom_headers import BODY_REF

BODY_REF_HEADER = BODY_REF
BODY_REF_HEADER_LOWER = BODY_REF_HEADER.lower()
# Truncated SHA-256 hex (64 bits) — short filenames under bodies/
CONTENT_HASH_HEX_LEN = 16

def full_content_hash(body: bytes) -> str:
  return hashlib.sha256(body or b'').hexdigest()

def content_hash(body: bytes) -> str:
  return full_content_hash(body)[:CONTENT_HASH_HEX_LEN]

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
  """Read body from a relative bodies/<hash> ref under slug_dir."""
  path = resolve_body_path(slug_dir, ref)
  with open(path, 'rb') as fp:
    return fp.read()
