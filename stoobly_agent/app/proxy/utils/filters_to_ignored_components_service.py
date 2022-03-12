from typing import List, TypedDict

from stoobly_agent.lib.settings import Component, Rewrite
from ..mock.hashed_request_decorator import COMPONENT_TYPES

class IgnoredComponent(TypedDict):
  name: str
  type: str

def filters_to_ignored_components(filters: List[Rewrite]) -> List[IgnoredComponent]:
  ignored_components = []

  for filter in filters:
    filter_name = filter['name']
    filter_type = filter['type']

    if filter_type == Component['Header']:
      ignored_components.append({
        'name': filter_name,
        'type': COMPONENT_TYPES['HEADER']
      })
    elif filter_type == Component['QueryParam']:
      ignored_components.append({
        'name': filter_name,
        'type': COMPONENT_TYPES['QUERY_PARAM']
      })
    elif filter_type == Component['BodyParam']:
      ignored_components.append({
        'name': filter_name,
        'type': COMPONENT_TYPES['BODY_PARAM']
      })
  
  return ignored_components
