import pdb

from typing import TYPE_CHECKING
from urllib.parse import urlparse

if TYPE_CHECKING:
    from requests import Request
    from mitmproxy.http import Headers, Request as MitmproxyRequest

from stoobly_agent.lib.utils.decode import decode

class MitmproxyRequestAdapter():

  def __init__(self, request: 'Request', http_version: str = 'HTTP/1.1'):
    self.__http_version = http_version
    self.__request = request

  @property
  def url(self):
    parsed_url = urlparse(self.__request.url)

    if not parsed_url.netloc:
      parsed_url = parsed_url._replace(netloc=parsed_url.path, path='')

    if not parsed_url.scheme:
      parsed_url = parsed_url._replace(scheme='https')

    return parsed_url.geturl()

  @property
  def headers(self):
    # Lazy import for runtime usage
    from mitmproxy.http import Headers
    return Headers(**self.__decode_dict(self.__request.headers))

  @property
  def data(self):
    _data = self.__request.data

    # If no data is provided to python requests.Request, it is sent to []
    if _data == []:
      return b''

    return _data

  def adapt(self):
    # Lazy import for runtime usage
    from mitmproxy.http import Request as MitmproxyRequest
    request = MitmproxyRequest.make(
      self.__request.method,
      self.url,
      self.data,
      self.headers,
    )
    request.http_version = self.__http_version
    return request

  def __decode_dict(self, d):
    new_d = {}
    for k, v in d.items():
      new_d[decode(k)] = decode(v) if isinstance(v, bytes) else v
    return new_d
