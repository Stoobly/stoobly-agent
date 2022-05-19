from typing import List, TypedDict

from .pagination_query_params import PaginationQueryParams

class ProjectsIndexQueryParams(PaginationQueryParams):
  organization_id: str

class ProjectMutateParams(TypedDict):
  name: str
  description: str

class ProjectCreateParams(TypedDict):
  organization_id: str
  project: ProjectMutateParams

class ProjectShowResponse(TypedDict):
  created_at: str
  description: str
  key: str
  name: str
  updated_at: str

class ProjectsIndexResponse(TypedDict):
  list: List[ProjectShowResponse]
  total: int
