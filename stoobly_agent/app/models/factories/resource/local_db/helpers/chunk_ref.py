import hashlib
import os
from typing import List, Optional, Tuple

from stoobly_agent.config.constants.custom_headers import CHUNK_REF
from stoobly_agent.config.data_dir import DATA_DIR_NAME

CHUNK_REF_HEADER = CHUNK_REF
CHUNK_REF_HEADER_LOWER = CHUNK_REF_HEADER.lower()
# Truncated SHA-256 hex (64 bits) — short filenames under chunks/
CONTENT_HASH_HEX_LEN = 16

# Context-dir-relative (PR-readable): .stoobly/snapshots/requests/<slug>/chunks/<hash>
_REF_ROOT_PARTS = (DATA_DIR_NAME, 'snapshots', 'requests')
_REF_KIND = 'chunks'

def full_content_hash(payload: bytes) -> str:
  return hashlib.sha256(payload or b'').hexdigest()

def content_hash(payload: bytes) -> str:
  return full_content_hash(payload)[:CONTENT_HASH_HEX_LEN]

def chunks_dir_path(slug_dir: str) -> str:
  return os.path.join(slug_dir, 'chunks')

def chunk_file_path(slug_dir: str, hash_value: str) -> str:
  return os.path.join(chunks_dir_path(slug_dir), hash_value)

def relative_chunk_ref(slug: str, hash_value: str) -> str:
  """
  Context-dir-relative chunk file ref for YAML / PR navigation:

    .stoobly/snapshots/requests/<slug>/chunks/<hash>
  """
  _validate_slug(slug)
  if not hash_value or '/' in hash_value or '\\' in hash_value or '..' in hash_value:
    raise ValueError(f"Invalid chunk hash: {hash_value}")
  return f"{DATA_DIR_NAME}/snapshots/requests/{slug}/chunks/{hash_value}"

def is_chunk_ref(ref: str) -> bool:
  try:
    normalize_chunk_ref(ref)
    return True
  except ValueError:
    return False

def normalize_chunk_ref(ref: str, slug: Optional[str] = None) -> str:
  """
  Normalize to .stoobly/snapshots/requests/<slug>/chunks/<hash>.

  Rejects absolute paths and '..' segments. When slug is provided, the ref's
  slug segment must match.
  """
  normalized = (ref or '').replace('\\', '/').rstrip('/').lstrip('/')
  if not normalized or '..' in normalized.split('/'):
    raise ValueError(f"Invalid chunk ref: {ref}")

  parts = normalized.split('/')
  if (
    len(parts) != 6
    or tuple(parts[:3]) != _REF_ROOT_PARTS
    or parts[4] != _REF_KIND
    or not parts[3]
    or not parts[5]
  ):
    raise ValueError(f"Invalid chunk ref: {ref}")

  if slug is not None and parts[3] != slug:
    raise ValueError(f"Invalid chunk ref: {ref}")

  return normalized

def _validate_slug(slug: str):
  if not slug or '/' in slug or '\\' in slug or slug in ('.', '..'):
    raise ValueError(f"Invalid slug: {slug}")

def _is_under_dir(path: str, parent: str) -> bool:
  real_path = os.path.realpath(path)
  real_parent = os.path.realpath(parent)
  return real_path == real_parent or real_path.startswith(real_parent + os.sep)

def resolve_chunk_path(slug_dir: str, ref: str) -> str:
  """
  Resolve a chunk ref to a path under slug_dir/chunks.

  Refs must be .stoobly/snapshots/requests/<slug>/chunks/<hash> with <slug>
  equal to this slug_dir's basename. After join, require realpath(path) stays
  under realpath(chunks_dir) so a planted chunks/<name> symlink cannot escape.
  """
  slug = os.path.basename(os.path.normpath(slug_dir))
  normalized = normalize_chunk_ref(ref, slug=slug)
  hash_value = normalized.rsplit('/', 1)[-1]
  path = chunk_file_path(slug_dir, hash_value)
  chunks_dir = chunks_dir_path(slug_dir)
  if not _is_under_dir(chunks_dir, slug_dir) or not _is_under_dir(path, chunks_dir):
    raise ValueError(f"Invalid chunk ref: {ref}")
  return path

def write_chunk(slug_dir: str, payload: bytes) -> str:
  """
  Write chunk bytes under chunks/<hash16>. Returns the hash used in the filename.

  On truncated-hash collision (same short name, different bytes), falls back to
  the full SHA-256 hex filename so content is never silently reused.
  """
  data = payload or b''
  full_digest = full_content_hash(data)
  short_hash = full_digest[:CONTENT_HASH_HEX_LEN]
  chunks_dir = chunks_dir_path(slug_dir)
  os.makedirs(chunks_dir, exist_ok=True)

  short_path = chunk_file_path(slug_dir, short_hash)
  if not os.path.exists(short_path):
    with open(short_path, 'wb') as fp:
      fp.write(data)
    return short_hash

  with open(short_path, 'rb') as fp:
    if fp.read() == data:
      return short_hash

  full_path = chunk_file_path(slug_dir, full_digest)
  if not os.path.exists(full_path):
    with open(full_path, 'wb') as fp:
      fp.write(data)
  return full_digest

def write_chunks(slug_dir: str, payloads: List[bytes]) -> List[str]:
  """
  Write ordered chunk payloads under chunks/<hash>.

  Returns ordered context-relative refs (one per payload) for X-Stoobly-Chunk-Ref.
  """
  slug = os.path.basename(os.path.normpath(slug_dir))
  refs: List[str] = []
  for payload in payloads:
    hash_value = write_chunk(slug_dir, payload)
    refs.append(relative_chunk_ref(slug, hash_value))
  return refs

def read_chunk(slug_dir: str, ref: str) -> bytes:
  """Read one chunk from a context-relative ref under slug_dir."""
  path = resolve_chunk_path(slug_dir, ref)
  with open(path, 'rb') as fp:
    return fp.read()

def read_chunks(slug_dir: str, refs: List[str]) -> List[Tuple[int, bytes]]:
  """Read ordered (sequence, payload) pairs from ordered chunk refs."""
  entries: List[Tuple[int, bytes]] = []
  for sequence, ref in enumerate(refs):
    entries.append((sequence, read_chunk(slug_dir, ref)))
  return entries
