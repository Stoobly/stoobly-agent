import pytest

from stoobly_agent.app.cli.scaffold.constants import (
  WORKFLOW_MOCK_TYPE,
  WORKFLOW_RECORD_TYPE,
  WORKFLOW_TEST_TYPE,
)
from stoobly_agent.app.cli.scaffold.workflow_firewall import (
  HTTP_METHODS,
  build_include_firewall_rule_for_service_url,
  upsert_firewall_rule,
  workflow_template_to_firewall_mode,
)
from stoobly_agent.app.settings.constants import firewall_action
from stoobly_agent.config.constants import mode


def build_workflow_firewall_rules(
  *,
  existing_firewall_rules: list,
  service_urls: list,
  workflow_template: str,
):
  """
  Test-only helper that mirrors the CLI behavior for firewall rule application.
  """
  firewall_mode = workflow_template_to_firewall_mode(workflow_template)
  firewall_rules = list(existing_firewall_rules)

  for service_url in service_urls:
    if not service_url:
      continue

    new_rule = build_include_firewall_rule_for_service_url(
      service_url=service_url,
      firewall_mode=firewall_mode,
    )
    upsert_firewall_rule(firewall_rules=firewall_rules, new_rule=new_rule)

  return firewall_rules


@pytest.mark.parametrize(
  "workflow_template,expected_mode",
  [
    (WORKFLOW_MOCK_TYPE, mode.MOCK),
    (WORKFLOW_RECORD_TYPE, mode.RECORD),
    (WORKFLOW_TEST_TYPE, mode.MOCK),
  ],
)
def test_build_workflow_firewall_rules_applied_for_each_service(
  workflow_template: str,
  expected_mode: str,
):
  existing_rules = []
  service_urls = [
    "http://external-api",
    "https://external-secure-api",
    "http://local-service",
  ]

  updated_rules = build_workflow_firewall_rules(
    existing_firewall_rules=existing_rules,
    service_urls=service_urls,
    workflow_template=workflow_template,
  )

  assert len(updated_rules) == len(service_urls)

  for url in service_urls:
    expected_pattern = f"{url}/?.*?"
    assert any(
      rule.action == firewall_action.INCLUDE
      and rule.pattern == expected_pattern
      and rule.methods == HTTP_METHODS
      and rule.modes == [expected_mode]
      for rule in updated_rules
    )


def test_build_workflow_firewall_rules_upserts_on_pattern_and_methods():
  # Start with an incorrect mode for an existing rule.
  service_url = "http://external-api"
  expected_pattern = f"{service_url}/?.*?"

  existing_rules = build_workflow_firewall_rules(
    existing_firewall_rules=[],
    service_urls=[service_url],
    workflow_template=WORKFLOW_MOCK_TYPE,
  )
  assert existing_rules[0].modes == [mode.MOCK]

  updated_rules = build_workflow_firewall_rules(
    existing_firewall_rules=existing_rules,
    service_urls=[service_url],
    workflow_template=WORKFLOW_RECORD_TYPE,
  )

  assert len(updated_rules) == 1
  assert updated_rules[0].pattern == expected_pattern
  assert updated_rules[0].methods == HTTP_METHODS
  assert updated_rules[0].action == firewall_action.INCLUDE
  assert updated_rules[0].modes == [mode.RECORD]

