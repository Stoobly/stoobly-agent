import pdb

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from requests import Request

from urllib.parse import urlparse, urlunparse

from stoobly_agent.app.models.adapters.raw_http_request_adapter import RawHttpRequestAdapter

from ..request import Request as ORMRequest

VALID_METHODS = ['CONNECT', 'DELETE', 'GET', 'HEAD', 'OPTIONS', 'PATCH', 'POST', 'PUT', 'TRACE']

class ORMToRequestTransformer():

  def __init__(self, request: ORMRequest):
    self.__dirty = False

    self.__body = None
    self.__headers = None
    self.__host = None
    self.__method = None
    self.__path = None
    self.__port = None
    self.__request = request
    self.__scheme = None
    self.__url = None

  def transform(self) -> 'Request':
    adapter = RawHttpRequestAdapter(self.__request.raw)

    if self.__body:
      adapter.body = self.__body 

    if self.__headers:
      adapter.headers = self.__headers

    if self.__method:
      adapter.method = self.__method

    if self.__url:
      adapter.url = self.__url

    if self.__scheme or self.__host or self.__port or self.__path:
      adapter.url = self.__update_url(
        adapter.url, self.__scheme, self.__host, self.__port, self.__path
      )

    python_request = adapter.to_request()

    return python_request

  @property
  def dirty(self):
    return self.__dirty

  def with_body(self, body: str):
    self.__body = body
    self.__dirty = True
    return self

  def with_headers(self, headers: list):
    self.__headers = headers
    self.__dirty = True
    return self

  def with_host(self, host: str):
    self.__host = host
    self.__dirty = True
    return self

  def with_method(self, method: str):
    _method = method.strip().upper()
    if not self.__validate_method(_method):
      raise ValueError(f"Method must be one of {', '.join(VALID_METHODS)}")
    self.__method = _method
    self.__dirty = True
    return self

  def with_port(self, port: str):
    try:
      _port = int(port)
    except Exception:
      raise ValueError('Port must be a number')
    
    if _port <= 0 or _port > 65535:
      raise ValueError('Port must be between 0 and 65535')

    self.__port = port
    self.__dirty = True
    return self

  def with_path(self, path: str):
    self.__path = path
    self.__dirty = True
    return self

  def with_scheme(self, scheme: str):
    if scheme != 'https' and scheme != 'http':
      raise ValueError('Scheme must be https or http')

    self.__scheme = scheme
    self.__dirty = True

    return self

  def with_url(self, url: str):
    self.__url = url
    self.__dirty = True
    return self

  def __update_url(self, url, scheme=None, hostname=None, port=None, path=None):
    parsed = urlparse(url)

    # Update netloc: preserve username, password, and port if present
    userinfo = ''
    if parsed.username:
        userinfo += parsed.username
        if parsed.password:
            userinfo += f':{parsed.password}'
        userinfo += '@'

    new_hostname = hostname or parsed.hostname
    new_port = port if port is not None else parsed.port

    # Compose the netloc
    if new_port:
        netloc = f"{userinfo}{new_hostname}:{new_port}"
    else:
        netloc = f"{userinfo}{new_hostname}"

    # Build the updated URL
    new_parts = parsed._replace(
        scheme=scheme or parsed.scheme,
        netloc=netloc,
        path=path or parsed.path
    )
    return urlunparse(new_parts)

  def __validate_method(self, method: str):
    if not isinstance(method, str):
      return False

    return method.upper() in VALID_METHODS