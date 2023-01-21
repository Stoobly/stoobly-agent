from typing import TypedDict

class PaginationQueryParams(TypedDict):
  filter: str
  page: str
  size: int
  sort_by: str
  sort_order: str