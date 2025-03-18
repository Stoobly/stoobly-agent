import mimetypes
import os
import pdb
import re

from io import BytesIO
from mitmproxy.http import Request as MitmproxyRequest
from requests import Response
from requests.structures import CaseInsensitiveDict
from typing import Union

from stoobly_agent.lib.logger import bcolors, Logger

from .types import Fixtures

LOG_ID = 'Fixture'

class Options():
  public_directory_path: str
  response_fixtures: Fixtures

def eval_fixtures(request: MitmproxyRequest, **options: Options) -> Union[Response, None]:
  fixture_path = None
  headers = CaseInsensitiveDict()
  status_code = 200

  response_fixtures = options.get('response_fixtures')
  fixture: dict = __eval_response_fixtures(request, response_fixtures)

  if not fixture:
    public_directory_path = options.get('public_directory_path')

    if not public_directory_path:
      return

    request_path = 'index' if request.path == '/' else request.path
    _fixture_path = os.path.join(public_directory_path, request_path.lstrip('/'))
    if request.headers.get('accept'):
      fixture_path = __guess_file_path(_fixture_path, request.headers['accept'])

    if not fixture_path:
      fixture_path = _fixture_path
      if not os.path.isfile(fixture_path):
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

    response.status_code = status_code
    response.raw = BytesIO(fp.read()) 
    response.headers = headers

    if not response.headers.get('content-type'):
      content_type = __guess_content_type(fixture_path)
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
