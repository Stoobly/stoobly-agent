import mimetypes
import os
import pdb
import re
import yaml

from io import BytesIO
from typing import TYPE_CHECKING, List, Optional, Union
from urllib.parse import urlparse

if TYPE_CHECKING:
    from requests import Response
    from mitmproxy.http import Request as MitmproxyRequest

from stoobly_agent.lib.logger import bcolors, Logger
from stoobly_agent.config.constants.custom_headers import MOCK_FIXTURE_PATH

from .types import MockOptions, PublicDirectoryPath, ResponseFixturesPath

LOG_ID = 'Fixture'

def eval_fixtures(request: 'MitmproxyRequest', **options: MockOptions) -> Union['Response', None]:
  # Lazy import for runtime
  from requests import Response
  from requests.structures import CaseInsensitiveDict
  
  fixture_path = request.headers.get(MOCK_FIXTURE_PATH)
  headers = CaseInsensitiveDict()
  status_code = 200

  if fixture_path:
    if not os.path.exists(fixture_path):
      return
  else:
    response_fixtures = options.get('response_fixtures')
    
    # Try response fixtures in order of preference
    fixture = None

    if response_fixtures:
      fixture = __find_fixture_for_request(request, response_fixtures, request.method)

    if options.get('response_fixtures_path'):
      fixture = __eval_response_fixtures_from_paths(request, options['response_fixtures_path'])
    
    if not fixture:
      raw_paths = options.get('public_directory_path')
      public_directory_paths = __parse_public_directory_paths(raw_paths)
      
      if not public_directory_paths:
        return

      request_path = 'index' if request.path == '/' else request.path
      # Extract origin from request URL (e.g., https://example.com/path -> https://example.com)
      request_origin = __request_origin(request)
      
      # Try to find a matching file in the public directory paths
      fixture_path = None
      for dir_path_config in public_directory_paths:
        # Check if origin matches (if origin is specified)
        if dir_path_config.get('origin') and request_origin:
          if not __origin_matches(dir_path_config['origin'], request_origin):
            continue
        
        # Try to find the file in this directory
        fixture_path = os.path.join(dir_path_config['path'], request_path.lstrip('/'))
        if request.headers.get('accept'):
          fixture_path = __guess_file_path(fixture_path, request.headers['accept'])
        
        if os.path.isfile(fixture_path):
          break
        else:
          fixture_path = None
      
      if not fixture_path:
        return
    else:
      fixture_path = fixture.get('path')
      if not fixture_path:
        return

      if os.path.isdir(fixture_path):
        request_path = request.path
        match = re.match(fixture.get('path_pattern', request_path), request_path)

        if not match or match.end() == len(request_path):
          sub_path = 'index'
        else:
          sub_path = request_path[match.end():]

        fixture_path = os.path.join(fixture_path, sub_path.lstrip('/'))
        if request.headers.get('accept'):
          fixture_path = __guess_file_path(fixture_path, request.headers['accept'])
        
      if not os.path.isfile(fixture_path):
        return
        
      _headers = fixture.get('headers')
      headers = CaseInsensitiveDict(_headers if isinstance(_headers, dict) else {}) 

      if fixture.get('status_code'):
        status_code = fixture.get('status_code')

  with open(fixture_path, 'rb') as fp:
    response = Response()

    response.status_code = int(status_code)
    response.raw = BytesIO(fp.read()) 
    headers[MOCK_FIXTURE_PATH] = fixture_path
    response.headers = headers

    if not response.headers.get('content-type'):
      content_type = __guess_content_type(fixture_path)
      if content_type:
        response.headers['content-type'] = content_type
      else:
        # Default to highest priority accept header
        content_type = __choose_highest_priority_content_type(request.headers.get('accept'))
        if content_type:
          response.headers['content-type'] = content_type

    Logger.instance(LOG_ID).debug(f"{bcolors.OKBLUE}Resolved{bcolors.ENDC} fixture {fixture_path}")

    return response

def __eval_response_fixtures_from_paths(request: 'MitmproxyRequest', fixtures_paths: str):
  """Iterate through response fixtures paths and return the first matching fixture."""
  if not fixtures_paths:
    return None

  # Parse multiple response fixtures paths with optional origin specification
  parsed_paths = __parse_response_fixtures_paths(fixtures_paths)
  
  # Extract origin from request URL
  request_origin = __request_origin(request)
  method = request.method

  # Iterate through each fixtures path
  for path_config in parsed_paths:
    fixtures_path = path_config['path']
    origin = path_config.get('origin')
    
    # If origin is specified, check if it matches the request origin
    if origin and request_origin:
      if not __origin_matches(origin, request_origin):
        continue  # Skip this file if origin doesn't match
    elif origin and not request_origin:
      continue  # Skip origin-specific files if request has no origin
    
    # Load and parse this specific fixtures file
    if not os.path.exists(fixtures_path):
      Logger.instance(LOG_ID).error(f"Response fixtures {fixtures_path} does not exist")
      continue

    try:
      with open(fixtures_path, 'r') as stream:
        fixtures = yaml.safe_load(stream) or {}
        
        # Try to find a matching fixture in this file
        fixture = __find_fixture_for_request(request, fixtures, method)
        if fixture:
          # Convert fixture path to absolute path if it's a relative path and if 'path' exists in the fixture
          if fixture.get('path') and not os.path.isabs(fixture['path']):
            fixture['path'] = os.path.join(os.path.dirname(fixtures_path), fixture['path'])
          return fixture  # Return immediately on first match
          
    except yaml.YAMLError as exc:
      Logger.instance(LOG_ID).error(f"Error parsing {fixtures_path}: {exc}")
      continue
  
  return None  # No matching fixture found in any file

def __guess_content_type(file_path):
  file_extension = os.path.splitext(file_path)[1]
  if not file_extension:
    return
  return mimetypes.types_map.get(file_extension)

def __guess_file_path(file_path: str, content_type):
  file_extension = os.path.splitext(file_path)[1]
  if file_extension:
    return file_path

  if not content_type:
    return file_path

  content_types = __parse_accept_header(content_type)

  for content_type in content_types:
    file_extension = mimetypes.guess_extension(content_type)

    if not file_extension:
      continue

    _file_path = f"{file_path}{file_extension}"
    if os.path.isfile(_file_path):
      return _file_path

  return file_path

def __find_fixture_for_request(request: 'MitmproxyRequest', fixtures: dict, method: str):
  """Find a fixture for the given request in the provided fixtures."""
  if not fixtures:
    return None
  
  return __find_fixture_in_routes(fixtures, method, request.path)

def __find_fixture_in_routes(fixtures: dict, method: str, request_path: str):
  """Find a fixture for the given method and path in the provided fixtures."""
  routes = fixtures.get(method)
  
  if not isinstance(routes, dict):
    return None

  for path_pattern in routes:
    if not re.fullmatch(path_pattern, request_path):
      continue
      
    fixture = routes[path_pattern]
    if not isinstance(fixture, dict):
      continue

    path = fixture.get('path')

    if path:
      fixture['path_pattern'] = path_pattern
      return fixture
  
  return None

def __choose_highest_priority_content_type(accept_header: str) -> Optional[str]:
    if not accept_header:
        return None

    if accept_header == '*/*':
      return 'text/plain'

    types = []
    for part in accept_header.split(","):
        media_range = part.strip()
        if ";" in media_range:
            mime, *params = media_range.split(";")
            q = 1.0  # default
            for param in params:
                param = param.strip()
                if param.startswith("q="):
                    try:
                        q = float(param[2:])
                    except ValueError:
                        q = 0.0  # invalid q values treated as lowest
        else:
            mime = media_range
            q = 1.0
        types.append((mime.strip(), q))

    # Sort by descending q
    types.sort(key=lambda x: -x[1])
    return types[0][0] if types else None

def __origin_matches(pattern: str, request_origin: str) -> bool:
    return bool(re.fullmatch(pattern, request_origin))

def __parse_accept_header(accept_header):
    # In the case accept_header is */*, default to html and json file types
    if accept_header == '*/*':
      return ['text/html', 'application/json']

    types = []
    for item in accept_header.split(","):
        parts = item.split(";")
        content_type = parts[0].strip()
        q_value = 1.0  # Default quality value
        if len(parts) > 1 and parts[1].strip().startswith("q="):
            try:
                q_value = float(parts[1].strip()[2:])
            except ValueError:
                pass  # Keep default q_value if parsing fails
        types.append((content_type, q_value))

    # Sort by quality factor in descending order
    return [content_type for content_type, _ in sorted(types, key=lambda x: x[1], reverse=True)]

def __parse_origin_path_item(path_item: str):
  """Parse a single path:origin item and return (path, origin) tuple."""
  path_item = path_item.strip()
  
  # Check if this looks like a path:origin format
  # Format: <FILE-PATH>:<ORIGIN> where ORIGIN is scheme:hostname:port
  # We need to find the colon that separates path from origin
  if '://' in path_item:
    # Find the colon that separates path from origin
    # Origin format: scheme:hostname:port (e.g., https://api.example.com:8080)
    origin_start = path_item.rfind('://')
    if origin_start > 0:
      # Look for the colon before the scheme
      colon_before_scheme = path_item.rfind(':', 0, origin_start)
      if colon_before_scheme != -1:
        # Format: path:origin
        path = path_item[:colon_before_scheme]
        origin = path_item[colon_before_scheme + 1:]
        return (path.strip(), origin.strip())
    
    # No colon before scheme found, treat entire string as path
    return (path_item, None)
  else:
    # Check for path:hostname:port format (without scheme)
    colons = [i for i, char in enumerate(path_item) if char == ':']
    
    if len(colons) >= 1:
      # Find the first colon that separates path from origin
      first_colon_idx = colons[0]
      potential_origin = path_item[first_colon_idx + 1:]
      
      # Check if this looks like a hostname:port format
      # A valid hostname:port should have another colon for the port
      if ':' in potential_origin:
        # Format: path:hostname:port
        path = path_item[:first_colon_idx]
        origin = potential_origin
        return (path.strip(), origin.strip())
    
    # No valid path:origin format found, treat entire string as path
    return (path_item, None)

def __parse_public_directory_paths(raw_paths: str) -> List[PublicDirectoryPath]:
  """Parse public directory paths from comma-separated string."""
  if not raw_paths:
    return []
  
  paths = []
  for path_item in raw_paths.split(','):
    path, origin = __parse_origin_path_item(path_item)
    paths.append(PublicDirectoryPath(origin=origin, path=path))
  
  return paths

def __parse_response_fixtures_paths(raw_paths: str) -> List[ResponseFixturesPath]:
  """Parse response fixtures paths from comma-separated string."""
  if not raw_paths:
    return []
  
  paths = []
  for path_item in raw_paths.split(','):
    path, origin = __parse_origin_path_item(path_item)
    paths.append(ResponseFixturesPath(origin=origin, path=path))
  
  return paths

def __request_origin(request: 'MitmproxyRequest') -> str:
  parsed_url = urlparse(request.url)
  return f"{parsed_url.scheme}://{parsed_url.hostname}" + (f":{parsed_url.port}" if parsed_url.port else "")
