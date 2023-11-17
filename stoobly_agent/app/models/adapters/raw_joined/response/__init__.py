import pdb

from .python_adapter import PythonResponseAdapter

class RawJoinedResponseAdapterFactory():

  def __init__(self, joined_request: bytes):
    self.__request = joined_request

  def python_response(self):
    return PythonResponseAdapter(self.__request).adapt()