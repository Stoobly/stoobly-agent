import pdb

from mitmproxy.coretypes.multidict import MultiDict
from mitmproxy.http import Headers, Request as MitmproxyRequest

from stoobly_agent.app.models.schemas.request import Request
from stoobly_agent.lib.utils.decode import decode

class MitmproxyRequestAdapter():

  def __init__(self, request: Request):
    self.__http_version = request.http_version
    self.__request = request

  @property
  def headers(self):
    _headers = self.__request.headers
    return Headers(**self.__decode_dict(_headers))

  def adapt(self):
    request = MitmproxyRequest.make(
      self.__request.method,
      self.__request.url,
      self.__request.body,
      self.headers,
    )
    request.http_version = self.__http_version
    return request

  def __decode_dict(self, d: Headers) -> MultiDict:
    new_d = MultiDict()
    for k, v in d.items():
      new_d.add(decode(k), decode(v))
    return new_d