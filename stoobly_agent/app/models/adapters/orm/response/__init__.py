import pdb

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from requests import Response

from .mitmproxy_adapter import MitmproxyResponseAdapter
from .python_adapter import PythonResponseAdapter

class OrmResponseAdapterFactory():

  def __init__(self, response: 'Response'):
    self.__response = response

  def mitmproxy_response(self):
    return MitmproxyResponseAdapter(self.__response).adapt()

  def python_response(self) -> 'Response':
    return PythonResponseAdapter(self.__response).adapt()