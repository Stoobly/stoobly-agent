import pdb
import requests

from .mitmproxy_adapter import MitmproxyResponseAdapter
from .python_adapter import PythonResponseAdapter

class OrmResponseAdapterFactory():

  def __init__(self, response: requests.Response):
    self.__response = response

  def mitmproxy_response(self):
    return MitmproxyResponseAdapter(self.__response).adapt()

  def python_response(self) -> requests.Response:
    return PythonResponseAdapter(self.__response).adapt()