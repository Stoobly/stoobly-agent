import pdb

from .python_adapter import PythonRequestAdapter
from .snapshot_adapter import SnapshotRequestAdapter

class RawJoinedRequestAdapterFactory():

  def __init__(self, joined_request: bytes):
    self.__request = joined_request

  def python_request(self):
    return PythonRequestAdapter(self.__request).adapt()

  def snapshot_request(self):
    return SnapshotRequestAdapter(self.__request).adapt()

  def snapshot_entry(self, slug_dir: str = None):
    from ..snapshot_entry_adapter import SnapshotEntryAdapter
    return SnapshotEntryAdapter.from_joined(self.__request, slug_dir).adapt()
