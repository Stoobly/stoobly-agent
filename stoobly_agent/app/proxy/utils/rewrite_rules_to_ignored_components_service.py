from typing import List, TypedDict
from urllib import request

from stoobly_agent.app.settings.parameter_rule import ParameterRule
from stoobly_agent.app.settings.constants import request_component

from ..mock.hashed_request_decorator import COMPONENT_TYPES

class IgnoredComponent(TypedDict):
  name: str
  type: str

def rewrite_rules_to_ignored_components(rules: List[ParameterRule]) -> List[IgnoredComponent]:
  ignored_components = []

  for rule in rules:
    rule_name = rule.name
    rule_type = rule.type

    if rule_type == request_component.HEADER:
      ignored_components.append({
        'name': rule_name,
        'type': COMPONENT_TYPES['HEADER']
      })
    elif rule_type == request_component.QUERY_PARAM:
      ignored_components.append({
        'name': rule_name,
        'type': COMPONENT_TYPES['QUERY_PARAM']
      })
    elif rule_type == request_component.BODY_PARAM:
      ignored_components.append({
        'name': rule_name,
        'type': COMPONENT_TYPES['BODY_PARAM']
      })
  
  return ignored_components
