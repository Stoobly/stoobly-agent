import pdb
import requests

from urllib.parse import parse_qs, urlparse

from .mitmproxy_adapter import MitmproxyRequestAdapter
from .raw_adapter import RawRequestAdapter
from .stoobly_adapter import StooblyRequestAdapter

class PythonRequestAdapterFactory():

  def __init__(self, request: requests.Request):
    self.__request = request

  def mitmproxy_request(self, http_version: str = 'HTTP/1.1'):
    return MitmproxyRequestAdapter(http_version, self.__request).adapt()

  def raw_request(self, http_version: str = 'HTTP/1.1'):
    return RawRequestAdapter(http_version, self.__request).adapt()

  def stoobly_request(self):
    return StooblyRequestAdapter(self.__request).adapt()