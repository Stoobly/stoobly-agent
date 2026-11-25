from typing import Optional

from .joined_request_adapter import JoinedRequestAdapter
from .request import SnapshotRequestAdapterFactory
from .response import SnapshotResponseAdapterFactory


class SnapshotAdapterFactory():
  """
  Adapt a structured snapshot request entry (method/url/headers + nested response)
  into other representations.

  Pass `slug_dir` to `joined_request` to reconstitute body/header refs after adapting.
  """

  def __init__(self, entry: dict, uuid: Optional[str] = None):
    self.__entry = entry
    self.__uuid = uuid

  def joined_request(self, slug_dir: Optional[str] = None) -> bytes:
    joined = JoinedRequestAdapter(self.__entry, uuid=self.__uuid).adapt()
    if slug_dir is None:
      return joined
    # Lazy import: ref helpers depend on top-level JoinedRequestAdapter.
    from stoobly_agent.app.models.factories.resource.local_db.helpers.joined_request_ref import (
      reconstitute_joined_request,
    )
    return reconstitute_joined_request(joined, slug_dir)

  def request(self) -> SnapshotRequestAdapterFactory:
    return SnapshotRequestAdapterFactory(self.__entry, uuid=self.__uuid)

  def response(self) -> SnapshotResponseAdapterFactory:
    response = self.__entry.get('response') if isinstance(self.__entry, dict) else None
    return SnapshotResponseAdapterFactory(
      response if isinstance(response, dict) else {},
      uuid=self.__uuid,
    )
