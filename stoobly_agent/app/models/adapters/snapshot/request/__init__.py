from typing import Optional

from .raw_adapter import RawRequestAdapter


class SnapshotRequestAdapterFactory():

  def __init__(self, entry: dict, uuid: Optional[str] = None):
    self.__entry = entry
    self.__uuid = uuid

  def raw_request(self) -> bytes:
    return RawRequestAdapter(self.__entry, uuid=self.__uuid).adapt()
