import pdb
import requests

from .python_adapter import PythonRequestAdapter

class MitmproxyRequestAdapterFactory():

  def __init__(self, request: requests.Request):
    self.__request = request

  def python_request(self):
    return PythonRequestAdapter(self.__request).adapt()