from typing import Optional, TypedDict

class ResponseColumns(TypedDict):
  raw: bytes
  request_id: int
  stream_status: Optional[str]
