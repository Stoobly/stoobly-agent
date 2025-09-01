import mimetypes
import os
import pdb
import re

from io import BytesIO
from mitmproxy.http import Request as MitmproxyRequest
from requests import Response
from requests.structures import CaseInsensitiveDict
from typing import List, Optional, Union
from urllib.parse import urlparse

from stoobly_agent.lib.logger import bcolors, Logger
from stoobly_agent.config.constants.custom_headers import MOCK_FIXTURE_PATH

from .types import Fixtures, MockOptions, PublicDirectoryPath

LOG_ID = 'Fixture'

def __parse_public_directory_paths(raw_paths: str) -> List[PublicDirectoryPath]:
  """Parse public directory paths from comma-separated string."""
  if not raw_paths:
    return []
  
  paths = []
  for path_item in raw_paths.split(','):
    path_item = path_item.strip()
    if ':' in path_item:
      # Format: origin:path
      origin, path = path_item.split(':', 1)
      paths.append(PublicDirectoryPath(origin=origin.strip(), path=path.strip()))
    else:
      # Format: path (no origin specified)
      paths.append(PublicDirectoryPath(origin=None, path=path_item))
  
  return paths

def eval_fixtures(request: MitmproxyRequest, **options: MockOptions) -> Union[Response, None]:
  fixture_path = request.headers.get(MOCK_FIXTURE_PATH)
  headers = CaseInsensitiveDict()
  status_code = 200

  if fixture_path:
    if not os.path.exists(fixture_path):
      return
  else:
    response_fixtures = options.get('response_fixtures')
    fixture: dict = __eval_response_fixtures(request, response_fixtures)

    if not fixture:
      raw_paths = options.get('public_directory_path')
      public_directory_paths = __parse_public_directory_paths(raw_paths)
      
      if not public_directory_paths:
        return

      request_path = 'index' if request.path == '/' else request.path
      # Extract origin from request URL (e.g., https://example.com/path -> example.com)
      parsed_url = urlparse(request.url)
      request_origin = parsed_url.netloc
      
      # Try to find a matching file in the public directory paths
      fixture_path = None
      for dir_path_config in public_directory_paths:
        # Check if origin matches (if origin is specified)
        if dir_path_config.get('origin') and request_origin:
          if not __origin_matches(dir_path_config['origin'], request_origin):
            continue
        
        # Try to find the file in this directory
        _fixture_path = os.path.join(dir_path_config['path'], request_path.lstrip('/'))
        if request.headers.get('accept'):
          fixture_path = __guess_file_path(_fixture_path, request.headers['accept'])
        
        if not fixture_path:
          fixture_path = _fixture_path
        
        if os.path.isfile(fixture_path):
          break
        else:
          fixture_path = None
      
      if not fixture_path:
        return
    else:
      fixture_path = fixture.get('path')
      if not fixture_path or not os.path.isfile(fixture_path):
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

def __guess_content_type(file_path):
  file_extension = os.path.splitext(file_path)[1]
  if not file_extension:
    return
  return mimetypes.types_map.get(file_extension)

def __guess_file_path(file_path, content_type):
  file_extension = os.path.splitext(file_path)[1]
  if file_extension:
    return file_path

  if not content_type:
    return

  content_types = __parse_accept_header(content_type)

  for content_type in content_types:
    file_extension = mimetypes.guess_extension(content_type)

    if not file_extension:
      continue

    _file_path = f"{file_path}{file_extension}"
    if os.path.isfile(_file_path):
      return _file_path

def __eval_response_fixtures(request: MitmproxyRequest, response_fixtures: Fixtures):
  if not isinstance(response_fixtures, dict):
    return

  method = request.method
  routes = response_fixtures.get(method)

  if not isinstance(routes, dict):
    return

  for path_pattern in routes:
    if not re.match(path_pattern, request.path):
      continue
      
    fixture = routes[path_pattern]
    if not isinstance(fixture, dict):
      continue

    path = fixture.get('path')

    if path:
      return fixture

def __choose_highest_priority_content_type(accept_header: str) -> Optional[str]:
    if not accept_header:
        return None

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

def __parse_accept_header(accept_header):
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

def __origin_matches(pattern: str, request_origin: str) -> bool:
    """Check if the request origin matches the specified pattern using regex."""
    # Remove protocol if present
    pattern = pattern.replace('https://', '').replace('http://', '')
    request_origin = request_origin.replace('https://', '').replace('http://', '')
    
    # Convert pattern to regex
    # Escape special regex characters except * and ?
    regex_pattern = re.escape(pattern)
    
    # Convert wildcards to regex equivalents
    regex_pattern = regex_pattern.replace('\\*', '.*')  # * matches any characters
    regex_pattern = regex_pattern.replace('\\?', '.')   # ? matches any single character
    
    # Anchor the pattern to match the entire string
    regex_pattern = f'^{regex_pattern}$'
    
    # Perform regex match
    return bool(re.match(regex_pattern, request_origin))
