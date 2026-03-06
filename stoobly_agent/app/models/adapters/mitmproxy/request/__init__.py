import pdb

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from requests import Request

from .python_adapter import PythonRequestAdapter

class MitmproxyRequestAdapterFactory():

  def __init__(self, request: 'Request'):
    self.__request = request

  def python_request(self):
    return PythonRequestAdapter(self.__request).adapt()