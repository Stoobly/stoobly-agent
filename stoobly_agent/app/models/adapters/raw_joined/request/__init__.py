import pdb

from .python_adapter import PythonRequestAdapter

class RawJoinedRequestAdapterFactory():

  def __init__(self, joined_request: bytes):
    self.__request = joined_request

  def python_request(self):
    return PythonRequestAdapter(self.__request).adapt()