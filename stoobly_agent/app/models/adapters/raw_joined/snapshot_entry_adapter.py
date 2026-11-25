from typing import Optional

from .request.snapshot_adapter import SnapshotRequestAdapter
from .response.snapshot_adapter import SnapshotResponseAdapter


class SnapshotEntryAdapter():
  """
  Adapt joined request bytes to a structured snapshot request entry
  (request fields + nested `response`).

  Pass `slug_dir` to externalize body/header refs before adapting.
  """

  def __init__(self, joined_request: bytes):
    self.__joined_request = joined_request

  @classmethod
  def from_joined(cls, joined_request: bytes, slug_dir: Optional[str] = None):
    if slug_dir is not None:
      # Lazy import: ref helpers depend on top-level JoinedRequestAdapter.
      from stoobly_agent.app.models.factories.resource.local_db.helpers.joined_request_ref import (
        externalize_joined_request,
      )
      joined_request = externalize_joined_request(joined_request, slug_dir)
    return cls(joined_request)

  def adapt(self) -> dict:
    entry = SnapshotRequestAdapter(self.__joined_request).adapt()
    entry['response'] = SnapshotResponseAdapter(self.__joined_request).adapt()
    return entry
