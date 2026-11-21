import re
from typing import Union

REQUEST_FILE_EXTENSION = '.http'

SAFE_NAME_RE = re.compile(r'[^A-Za-z0-9._-]+')

def build_request_slug(method: str, path: str) -> str:
  """
  Build v2 request directory slug: {METHOD}-{path-slug}.

  path-slug is path with leading/trailing slashes stripped and '/' replaced by '-'.
  Root path '/' yields method only.
  """
  method = (method or 'GET').upper()
  path = path or '/'
  path_slug = path.strip('/')
  if not path_slug:
    return method
  return f"{method}-{path_slug.replace('/', '-')}"

def request_relative_path(slug: str, uuid: str) -> str:
  return f"{slug}/{uuid}{REQUEST_FILE_EXTENSION}"

def sanitize_scenario_filename(name: str) -> str:
  """Filesystem-safe scenario YAML basename (without extension)."""
  name = (name or '').strip() or 'scenario'
  name = SAFE_NAME_RE.sub('-', name).strip('-._')
  return name or 'scenario'

def parse_request_relative_path(relative_path: str) -> Union[tuple, None]:
  """
  Parse `slug/<uuid>.http` into (slug, uuid).
  """
  if not relative_path:
    return None

  parts = relative_path.replace('\\', '/').split('/')
  if len(parts) != 2:
    return None

  slug, filename = parts
  if not filename.endswith(REQUEST_FILE_EXTENSION):
    return None

  uuid = filename[:-len(REQUEST_FILE_EXTENSION)]
  if not slug or not uuid:
    return None

  return slug, uuid
