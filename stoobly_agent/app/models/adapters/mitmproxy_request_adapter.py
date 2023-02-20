import pdb
import requests

from mitmproxy.net.http import url
from mitmproxy.http import Headers, Request as MitmproxyRequest
from time import time
from urllib.parse import urlparse

class MitmproxyRequestAdapter():

  def __init__(self, http_version, request: requests.Request):
    self.__http_version = http_version
    self.__latency = 0 # Seconds
    self.__request = request
    self.__timestamp_start = time()

    self.url = request.url
    self.__parsed_url = urlparse(self.__request.url)

  @property
  def headers(self):
    return Headers(**self.__decode_dict(self.__request.headers))

  @property
  def authority(self):
    authority = ''

    if self.__parsed_url.hostname:
      authority = f"{self.__parsed_url.hostname}"

      if self.__parsed_url.port:
        authority = authority + f":{self.__parsed_url.port}"

    return authority

  @property
  def timestamp_end(self):
    return self.__timestamp_start + self.__latency

  def adapt(self):
    data = self.__request.data if isinstance(self.__request.data, bytes) else self.__request.data.encode() 
    return MitmproxyRequest(
      self.__parsed_url.hostname or '',
      self.__parsed_url.port or self.__default_port(),
      self.__request.method,
      self.__parsed_url.scheme,
      self.authority,
      self.__parsed_url.path or '/',
      self.__http_version,
      self.headers,
      data,
      Headers(), # Trailers
      self.__timestamp_start,
      self.timestamp_end
    )

  def __default_port(self):
    return 443 if self.__parsed_url.scheme.lower() == 'https' else 80

  def __decode_dict(self, d):
    new_d = {}
    for k, v in d.items():
      new_d[k.decode() if isinstance(k, bytes) else k] = v.decode() if isinstance(v, bytes) else v
    return new_d