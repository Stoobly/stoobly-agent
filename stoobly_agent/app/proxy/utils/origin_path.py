import re

from os.path import expanduser
from typing import List, Tuple, Dict, Optional, Literal

from ..mock.types import LifecycleHooksPath, PublicDirectoryPath, ResponseFixturesPath

def parse_origin_path_item(path_item: str) -> Tuple[str, str]:
  """
  Parse a single 'path[:origin]' item and return (path, origin).
  Origin supports:
    - scheme://hostname[:port]
    - hostname:port
  """
  s = (path_item or '').strip()
  if not s:
    return (None, None)

  # Handle 'path:scheme://host[:port]' by finding colon before scheme
  if '://' in s:
    scheme_idx = s.rfind('://')
    if scheme_idx > 0:
      colon_before_scheme = s.rfind(':', 0, scheme_idx)
      if colon_before_scheme != -1:
        path = s[:colon_before_scheme].strip()
        path = expanduser(path)
        origin = s[colon_before_scheme + 1:].strip()
        return (path, origin)
    return (s, None)

  # Handle 'path:hostname:port' (no scheme)
  colons = [i for i, ch in enumerate(s) if ch == ':']
  if len(colons) >= 2:
    first = colons[0]
    path = s[:first].strip()
    path = expanduser(path)
    origin = s[first + 1:].strip()
    return (path, origin)

  # No origin specified
  return (expanduser(s), None)

def parse_origin_paths(
  raw: str,
  kind: Optional[Literal['plain', 'public', 'fixtures', 'lifecycle_hooks']] = 'plain'
) -> List[Dict[str, str]]:
  """
  Parse comma-separated 'path[:origin]' items into a list of dicts:
    [{ 'path': str, 'origin': Optional[str] }, ...]
  If kind is:
    - 'plain' or None: returns List[Dict[str, str]]
    - 'lifecycle_hooks': returns List[LifecycleHooksPath]
    - 'public': returns List[PublicDirectoryPath]
    - 'fixtures': returns List[ResponseFixturesPath]
  """
  if not raw:
    return []
    
  items: List[Dict[str, str]] = []
  for token in str(raw).split(','):
    path, origin = parse_origin_path_item(token)
    if path:
      items.append({'path': path, 'origin': origin})

  if kind == 'lifecycle_hooks':
    return [LifecycleHooksPath(origin=i.get('origin'), path=i.get('path')) for i in items]  # type: ignore
  elif kind == 'public':
    return [PublicDirectoryPath(origin=i.get('origin'), path=i.get('path')) for i in items]  # type: ignore
  elif kind == 'fixtures':
    return [ResponseFixturesPath(origin=i.get('origin'), path=i.get('path')) for i in items]  # type: 
  else:
    return items

def parse_public_directory_paths(raw: str) -> List[PublicDirectoryPath]:
  """
  Convenience wrapper returning List[PublicDirectoryPath] using parse_origin_paths.
  """
  return parse_origin_paths(raw, kind='public')  # type: ignore

def parse_response_fixtures_paths(raw: str) -> List[ResponseFixturesPath]:
  """
  Convenience wrapper returning List[ResponseFixturesPath] using parse_origin_paths.
  """
  return parse_origin_paths(raw, kind='fixtures')  # type: ignore

def parse_lifecycle_hooks_script_paths(raw: str) -> List[LifecycleHooksPath]:
  """
  Convenience wrapper returning List[{'path': str, 'origin': Optional[str]}]
  for lifecycle hooks scripts.
  """
  return parse_origin_paths(raw, kind='lifecycle_hooks')  # type: ignore

def request_origin_from_url(url: str) -> str:
  """
  Build origin from URL string: 'scheme://host[:port]'
  """
  try:
    from urllib.parse import urlparse
    parsed = urlparse(url)
    # Guard against malformed URLs where hostname or scheme may be missing
    if not parsed.scheme or not parsed.hostname:
      return ''
    host = parsed.hostname
    port = parsed.port
    return f"{parsed.scheme}://{host}" + (f":{port}" if port else "")
  except Exception:
    return ''

def request_origin_from_request(request) -> str:
  """
  Extract origin from a mitmproxy Request.
  """
  try:
    return request_origin_from_url(request.url)
  except Exception:
    return ''

def origin_matches(pattern: str, req_origin: str) -> bool:
  """
  Regex match origin pattern to request origin.
  
  Security note:
  - The `pattern` is expected to come from a trusted configuration source, not untrusted user input.
  - Catastrophic backtracking in regular expressions can cause performance issues; if the pattern
    is untrusted, validate or constrain it before use.
  
  Falls back to equality on invalid regex.
  """
  try:
    return bool(re.fullmatch(pattern, req_origin))
  except re.error:
    return pattern == req_origin
