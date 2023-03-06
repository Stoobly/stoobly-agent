import pdb
import requests

from .python_adapter import PythonResponseAdapter

class MitmproxyResponseAdapterFactory():

  def __init__(self, response: requests.Response):
    self.__response = response

  def python_response(self):
    return PythonResponseAdapter(self.__response).adapt()