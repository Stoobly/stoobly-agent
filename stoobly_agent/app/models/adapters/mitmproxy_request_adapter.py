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
    return MitmproxyRequest(
      self.__parsed_url.hostname or '',
      self.__parsed_url.port or 80,
      self.__request.method,
      self.__parsed_url.scheme,
      self.authority,
      self.__parsed_url.path,
      self.__http_version,
      self.headers,
      self.__request.data,
      Headers(), # Trailers
      self.__timestamp_start,
      self.timestamp_end
    )

  def __decode_dict(self, d):
    new_d = {}
    for k, v in d.items():
      new_d[k.decode()] = v.decode()
    return new_d