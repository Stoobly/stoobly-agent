from typing import TypedDict

class PaginationQueryParams(TypedDict):
  page: str
  size: int
  sort_order: str