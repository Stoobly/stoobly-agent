"""
Shared helpers for building filter rules for scaffold workflows.

This keeps the `scaffold workflow filter` command thin and makes it easy
to unit test the rule construction/upsert behavior without running workflows.
"""

from typing import List

from stoobly_agent.app.cli.scaffold.constants import (
  WORKFLOW_DEVELOP_TYPE,
  WORKFLOW_MOCK_TYPE,
  WORKFLOW_RECORD_TYPE,
  WORKFLOW_TEST_TYPE,
)
from stoobly_agent.app.settings.constants import filter_action
from stoobly_agent.app.settings.filter_rule import FilterRule
from stoobly_agent.config.constants import method, mode

HTTP_METHODS: List[str] = [
  method.GET,
  method.PATCH,
  method.POST,
  method.PUT,
  method.DELETE,
  method.OPTIONS,
]

WORKFLOW_FILTER_MODE_MAP = {
  WORKFLOW_MOCK_TYPE: mode.MOCK,
  WORKFLOW_DEVELOP_TYPE: mode.DEVELOP,
  WORKFLOW_RECORD_TYPE: mode.RECORD,
  WORKFLOW_TEST_TYPE: mode.MOCK,  # `test` workflows use mock interception mode
}


def workflow_template_to_filter_mode(workflow_template: str) -> str:
  filter_mode = WORKFLOW_FILTER_MODE_MAP.get(workflow_template)
  if not filter_mode:
    raise ValueError(
      f"Unsupported workflow template for filter mode mapping: '{workflow_template}'"
    )
  return filter_mode

def build_include_filter_rule_for_service_url(
  *,
  service_url: str,
  filter_mode: str,
  methods: List[str] = HTTP_METHODS,
) -> FilterRule:
  pattern = f'{service_url}/?.*?'
  return FilterRule({
    'action': filter_action.INCLUDE,
    'methods': methods,
    'modes': [filter_mode],
    'pattern': pattern,
  })

def upsert_filter_rule(
  *,
  filter_rules: List[FilterRule],
  new_rule: FilterRule,
) -> None:
  """
  Upsert by matching `pattern` + `methods`.
  """
  for i, rule in enumerate(filter_rules):
    if rule.pattern == new_rule.pattern and rule.methods == new_rule.methods:
      filter_rules[i] = new_rule
      return

  filter_rules.append(new_rule)
