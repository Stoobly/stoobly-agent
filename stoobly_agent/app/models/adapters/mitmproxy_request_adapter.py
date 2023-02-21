import pdb
import requests

from mitmproxy.net.http import url
from mitmproxy.http import Headers, Request as MitmproxyRequest
from time import time
from urllib.parse import urlparse

class MitmproxyRequestAdapter():

  def __init__(self, http_version, request: requests.Request):
    self.__http_version = http_version
    self.__request = request

  @property
  def headers(self):
    return Headers(**self.__decode_dict(self.__request.headers))

  def adapt(self):
    request = MitmproxyRequest.make(
      self.__request.method,
      self.__request.url,
      self.__request.data,
      self.headers,
    )
    request.http_version = self.__http_version
    return request

  def __decode_dict(self, d):
    new_d = {}
    for k, v in d.items():
      new_d[k.decode() if isinstance(k, bytes) else k] = v.decode() if isinstance(v, bytes) else v
    return new_d