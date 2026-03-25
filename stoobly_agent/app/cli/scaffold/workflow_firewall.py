"""
Shared helpers for building firewall rules for scaffold workflows.

This keeps the `scaffold workflow firewall` command thin and makes it easy
to unit test the rule construction/upsert behavior without running workflows.
"""

from typing import List

from stoobly_agent.app.cli.scaffold.constants import (
  WORKFLOW_MOCK_TYPE,
  WORKFLOW_RECORD_TYPE,
  WORKFLOW_TEST_TYPE,
)
from stoobly_agent.app.settings.constants import firewall_action
from stoobly_agent.app.settings.firewall_rule import FirewallRule
from stoobly_agent.config.constants import method, mode

HTTP_METHODS: List[str] = [
  method.GET,
  method.PATCH,
  method.POST,
  method.PUT,
  method.DELETE,
  method.OPTIONS,
]

WORKFLOW_FIREWALL_MODE_MAP = {
  WORKFLOW_MOCK_TYPE: mode.MOCK,
  WORKFLOW_RECORD_TYPE: mode.RECORD,
  WORKFLOW_TEST_TYPE: mode.MOCK,  # `test` workflows use mock interception mode
}


def workflow_template_to_firewall_mode(workflow_template: str) -> str:
  firewall_mode = WORKFLOW_FIREWALL_MODE_MAP.get(workflow_template)
  if not firewall_mode:
    raise ValueError(
      f"Unsupported workflow template for firewall mode mapping: '{workflow_template}'"
    )
  return firewall_mode

def build_include_firewall_rule_for_service_url(
  *,
  service_url: str,
  firewall_mode: str,
  methods: List[str] = HTTP_METHODS,
) -> FirewallRule:
  pattern = f'{service_url}/?.*?'
  return FirewallRule({
    'action': firewall_action.INCLUDE,
    'methods': methods,
    'modes': [firewall_mode],
    'pattern': pattern,
  })

def upsert_firewall_rule(
  *,
  firewall_rules: List[FirewallRule],
  new_rule: FirewallRule,
) -> None:
  """
  Upsert by matching `pattern` + `methods`.
  """
  for i, rule in enumerate(firewall_rules):
    if rule.pattern == new_rule.pattern and rule.methods == new_rule.methods:
      firewall_rules[i] = new_rule
      return

  firewall_rules.append(new_rule)
