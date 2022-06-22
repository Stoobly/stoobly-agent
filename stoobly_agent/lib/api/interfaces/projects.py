from typing import List, TypedDict

from .pagination_query_params import PaginationQueryParams

class ProjectsIndexQueryParams(PaginationQueryParams):
  organization_id: str

class ProjectDetails(TypedDict):
  name: str
  description: str

class ProjectCreateParams(ProjectDetails):
  organization_id: str
  project: ProjectDetails

class ProjectShowResponse(ProjectDetails):
  created_at: str
  key: str
  updated_at: str

class ProjectsIndexResponse(TypedDict):
  list: List[ProjectShowResponse]
  total: int
