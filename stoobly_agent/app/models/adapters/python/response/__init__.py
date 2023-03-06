import http
import pdb
import requests

from .mitmproxy_adapter import MitmproxyResponseAdapter

class PythonResponseAdapterFactory():

  def __init__(self, response: requests.Response):
    self.__response = response

  def mitmproxy_response(self):
    return MitmproxyResponseAdapter(self.__response).adapt()