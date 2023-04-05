from typing import TypedDict

from stoobly_agent.lib.api.interfaces.pagination_query_params import PaginationQueryParams

class ReplayedResponseIndexQueryParams(PaginationQueryParams):
  request_id: int

class ReplayeResponseCreateParams:
  latency: int
  raw: bytes
  request_id: int
  status: int

class ReplayedResponseShowParams:
  id: int
  latency: int
  raw: bytes
  request_id: int
  status: int