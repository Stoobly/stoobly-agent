import http
import pdb
import requests

from .mitmproxy_adapter import MitmproxyResponseAdapter

class PythonResponseAdapterFactory():

  def __init__(self, response: requests.Response):
    self.__response = response

  def mitmproxy_response(self, http_version: str):
    return MitmproxyResponseAdapter(http_version, self.__response).adapt()