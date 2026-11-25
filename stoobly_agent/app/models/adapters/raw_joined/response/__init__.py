import pdb

from .python_adapter import PythonResponseAdapter
from .snapshot_adapter import SnapshotResponseAdapter

class RawJoinedResponseAdapterFactory():

  def __init__(self, joined_request: bytes):
    self.__request = joined_request

  def python_response(self):
    return PythonResponseAdapter(self.__request).adapt()

  def snapshot_response(self):
    return SnapshotResponseAdapter(self.__request).adapt()
