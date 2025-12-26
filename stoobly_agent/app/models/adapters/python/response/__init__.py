import pdb

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from requests import Response

from .mitmproxy_adapter import MitmproxyResponseAdapter
from .raw_adapter import RawResponseAdapter

class PythonResponseAdapterFactory():

  def __init__(self, response: 'Response'):
    self.__response = response

  def mitmproxy_response(self):
    return MitmproxyResponseAdapter(self.__response).adapt()

  def raw_response(self):
    return RawResponseAdapter(self.__response).adapt()