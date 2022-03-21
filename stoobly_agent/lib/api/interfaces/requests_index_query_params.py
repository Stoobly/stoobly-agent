from .pagination_query_params import PaginationQueryParams

class RequestsIndexQueryParams(PaginationQueryParams):
  project_id: str
  scenario_id: str