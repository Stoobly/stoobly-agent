from typing import Optional

from .raw_adapter import RawResponseAdapter


class SnapshotResponseAdapterFactory():

  def __init__(self, response: dict, uuid: Optional[str] = None):
    self.__response = response
    self.__uuid = uuid

  def raw_response(self) -> bytes:
    return RawResponseAdapter(self.__response, uuid=self.__uuid).adapt()
