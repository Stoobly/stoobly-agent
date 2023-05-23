import pdb
import requests

from mitmproxy.http import Headers, Request as MitmproxyRequest

from stoobly_agent.app.models.schemas.request import Request
from stoobly_agent.lib.utils.decode import decode

class MitmproxyRequestAdapter():

  def __init__(self, request: Request):
    self.__http_version = request.http_version
    self.__request = request

  @property
  def headers(self):
    return Headers(**self.__decode_dict(self.__request.headers))

  def adapt(self):
    request = MitmproxyRequest.make(
      self.__request.method,
      self.__request.url,
      self.__request.body,
      self.headers,
    )
    request.http_version = self.__http_version
    return request

  def __decode_dict(self, d):
    new_d = {}
    for k, v in d.items():
      new_d[decode(k)] = decode(v)
    return new_d