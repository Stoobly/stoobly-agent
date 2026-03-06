import pdb

from typing import TYPE_CHECKING
from urllib.parse import parse_qs, urlparse

if TYPE_CHECKING:
    from requests import Request

from .mitmproxy_adapter import MitmproxyRequestAdapter
from .raw_adapter import RawRequestAdapter
from .stoobly_adapter import StooblyRequestAdapter

class PythonRequestAdapterFactory():

  def __init__(self, request: 'Request'):
    self.__request = request

  def mitmproxy_request(self, http_version: str = 'HTTP/1.1'):
    return MitmproxyRequestAdapter(self.__request, http_version).adapt()

  def raw_request(self, http_version: str = 'HTTP/1.1'):
    return RawRequestAdapter(self.__request, http_version).adapt()

  def stoobly_request(self):
    return StooblyRequestAdapter(self.__request).adapt()