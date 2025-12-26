import pdb

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from requests import Response

from .python_adapter import PythonResponseAdapter

class MitmproxyResponseAdapterFactory():

  def __init__(self, response: 'Response'):
    self.__response = response

  def python_response(self):
    return PythonResponseAdapter(self.__response).adapt()