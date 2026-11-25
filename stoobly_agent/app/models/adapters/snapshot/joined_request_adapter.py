from typing import Optional

from stoobly_agent.app.proxy.record.joined_request import REQUEST_DELIMITTER

from .request.raw_adapter import RawRequestAdapter
from .response.raw_adapter import RawResponseAdapter


class JoinedRequestAdapter():
  """
  Adapt a snapshot request entry (with nested `response`) to joined request bytes.

  Does not reconstitute body/header refs — callers that need inlined payloads
  should run reconstitution against a slug directory separately.
  """

  def __init__(self, entry: dict, uuid: Optional[str] = None):
    if not isinstance(entry, dict):
      raise ValueError('request entry must be a dict')

    response = entry.get('response') or {}
    if not isinstance(response, dict):
      raise ValueError('response must be a dict')

    self.__entry = entry
    self.__response = response
    self.__uuid = uuid

  def adapt(self) -> bytes:
    request_part = RawRequestAdapter(self.__entry, uuid=self.__uuid).adapt()
    response_part = RawResponseAdapter(self.__response, uuid=self.__uuid).adapt()
    return REQUEST_DELIMITTER.join([request_part, response_part])
