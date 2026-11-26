import os
from typing import List, Optional, Tuple

from stoobly_agent.config.constants.custom_headers import CHUNK_REF
from stoobly_agent.config.data_dir import DATA_DIR_NAME

CHUNK_REF_HEADER = CHUNK_REF
CHUNK_REF_HEADER_LOWER = CHUNK_REF_HEADER.lower()

_REF_ROOT_PARTS = (DATA_DIR_NAME, 'snapshots', 'requests')
_REF_KIND = 'chunks'

def chunks_dir_path(slug_dir: str) -> str:
  return os.path.join(slug_dir, 'chunks')

def chunk_file_path(slug_dir: str, sequence: int) -> str:
  return os.path.join(chunks_dir_path(slug_dir), f"{sequence:06d}")

def relative_chunk_ref(slug: str) -> str:
  """
  Context-dir-relative chunk dir ref for YAML / PR navigation:

    .stoobly/snapshots/requests/<slug>/chunks
  """
  _validate_slug(slug)
  return f"{DATA_DIR_NAME}/snapshots/requests/{slug}/chunks"

def is_chunk_ref(ref: str) -> bool:
  try:
    normalize_chunk_ref(ref)
    return True
  except ValueError:
    return False

def normalize_chunk_ref(ref: str, slug: Optional[str] = None) -> str:
  normalized = (ref or '').replace('\\', '/').rstrip('/').lstrip('/')
  if not normalized or '..' in normalized.split('/'):
    raise ValueError(f"Invalid chunk ref: {ref}")

  parts = normalized.split('/')
  if (
    len(parts) != 5
    or tuple(parts[:3]) != _REF_ROOT_PARTS
    or parts[4] != _REF_KIND
    or not parts[3]
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

def resolve_chunks_dir(slug_dir: str, ref: str) -> str:
  slug = os.path.basename(os.path.normpath(slug_dir))
  normalize_chunk_ref(ref, slug=slug)
  path = chunks_dir_path(slug_dir)
  if not _is_under_dir(path, slug_dir):
    raise ValueError(f"Invalid chunk ref: {ref}")
  return path

def write_chunks(slug_dir: str, payloads: List[bytes]) -> str:
  """
  Write ordered chunk payloads under chunks/000000, chunks/000001, ...
  Returns the relative chunk ref for the request slug.
  """
  chunks_dir = chunks_dir_path(slug_dir)
  os.makedirs(chunks_dir, exist_ok=True)
  for sequence, payload in enumerate(payloads):
    path = chunk_file_path(slug_dir, sequence)
    with open(path, 'wb') as fp:
      fp.write(payload or b'')
  slug = os.path.basename(os.path.normpath(slug_dir))
  return relative_chunk_ref(slug)

def read_chunks(slug_dir: str, ref: str) -> List[Tuple[int, bytes]]:
  """Read ordered (sequence, payload) pairs from a chunk ref under slug_dir."""
  chunks_dir = resolve_chunks_dir(slug_dir, ref)
  if not os.path.isdir(chunks_dir):
    return []

  entries = []
  for name in sorted(os.listdir(chunks_dir)):
    if not name.isdigit():
      continue
    sequence = int(name)
    path = os.path.join(chunks_dir, name)
    if not os.path.isfile(path):
      continue
    with open(path, 'rb') as fp:
      entries.append((sequence, fp.read()))
  return entries
