import pdb
import requests

from .mitmproxy_adapter import MitmproxyResponseAdapter
from .raw_adapter import RawResponseAdapter

class PythonResponseAdapterFactory():

  def __init__(self, response: requests.Response):
    self.__response = response

  def mitmproxy_response(self):
    return MitmproxyResponseAdapter(self.__response).adapt()

  def raw_response(self):
    return RawResponseAdapter(self.__response).adapt()