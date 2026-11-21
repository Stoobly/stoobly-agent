from typing import Optional, Tuple

from .request_slug import REQUEST_FILE_EXTENSION
from .snapshot_format import UUID_RE


def parse_resource_ref(ref: str) -> Tuple[Optional[str], str]:
  """
  Parse history resource field into (slug, uuid).

  Accepts bare uuid or `slug/<uuid>` / `slug/<uuid>.http`.
  """
  if not ref:
    return None, ref

  if '/' not in ref:
    return None, ref

  slug, rest = ref.rsplit('/', 1)
  if rest.endswith(REQUEST_FILE_EXTENSION):
    rest = rest[:-len(REQUEST_FILE_EXTENSION)]
  return slug or None, rest


def parse_scenario_resource_ref(ref: str) -> Tuple[Optional[str], str]:
  """
  Parse scenario history field into (name, identity).

  v2 uses name-only (unique). Legacy accepts `name/<uuid>`.
  v1 uses bare uuid. Identity for collapse is name when present, else uuid.
  """
  if not ref:
    return None, ref

  if '/' in ref:
    name, rest = ref.rsplit('/', 1)
    if rest.endswith('.yaml') or rest.endswith('.yml'):
      rest = rest.rsplit('.', 1)[0]
    # Name is the stable unique key; uuid kept only for legacy path resolve
    return name or None, name or rest

  if UUID_RE.match(ref):
    return None, ref

  return ref, ref
