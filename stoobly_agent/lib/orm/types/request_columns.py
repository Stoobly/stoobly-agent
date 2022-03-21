from typing import TypedDict

class RequestColumns(TypedDict):
  body_params_hash: str
  body_text_hash: str
  control: str
  headers_hash: str
  host: str
  method: str
  path: str
  port: int
  query_params_hash: str
  raw: bytes
  scheme: str