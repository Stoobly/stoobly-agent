import os
import pathlib
import tempfile
from urllib.parse import urlparse

import pytest
import yaml
from click.testing import CliRunner

from stoobly_agent.app.cli.scaffold.constants import (
  WORKFLOW_DEVELOP_TYPE,
  WORKFLOW_MOCK_TYPE,
  WORKFLOW_RECORD_TYPE,
  WORKFLOW_TEST_TYPE,
)
from stoobly_agent.app.cli.scaffold.workflow_filter import (
  HTTP_METHODS,
  build_include_filter_rule_for_service_url,
  upsert_filter_rule,
  workflow_template_to_filter_mode,
)
from stoobly_agent.app.cli.scaffold_cli import scaffold
from stoobly_agent.app.settings.constants import filter_action
from stoobly_agent.config.constants import mode
from stoobly_agent.config.data_dir import DATA_DIR_NAME
from stoobly_agent.test.test_helper import reset


def build_workflow_filter_rules(
  *,
  existing_filter_rules: list,
  service_urls: list,
  workflow_template: str,
):
  """
  Test-only helper that mirrors the CLI behavior for filter rule application.
  """
  filter_mode = workflow_template_to_filter_mode(workflow_template)
  filter_rules = list(existing_filter_rules)

  for service_url in service_urls:
    if not service_url:
      continue

    new_rule = build_include_filter_rule_for_service_url(
      service_url=service_url,
      filter_mode=filter_mode,
    )
    upsert_filter_rule(filter_rules=filter_rules, new_rule=new_rule)

  return filter_rules


@pytest.mark.parametrize(
  "workflow_template,expected_mode",
  [
    (WORKFLOW_DEVELOP_TYPE, mode.DEVELOP),
    (WORKFLOW_MOCK_TYPE, mode.MOCK),
    (WORKFLOW_RECORD_TYPE, mode.RECORD),
    (WORKFLOW_TEST_TYPE, mode.MOCK),
  ],
)
def test_build_workflow_filter_rules_applied_for_each_service(
  workflow_template: str,
  expected_mode: str,
):
  existing_rules = []
  service_urls = [
    "http://external-api",
    "https://external-secure-api",
    "http://local-service",
  ]

  updated_rules = build_workflow_filter_rules(
    existing_filter_rules=existing_rules,
    service_urls=service_urls,
    workflow_template=workflow_template,
  )

  assert len(updated_rules) == len(service_urls)

  for url in service_urls:
    expected_pattern = f"{url}/?.*?"
    assert any(
      rule.action == filter_action.INCLUDE
      and rule.pattern == expected_pattern
      and rule.methods == HTTP_METHODS
      and rule.modes == [expected_mode]
      for rule in updated_rules
    )


def test_build_workflow_filter_rules_upserts_on_pattern_and_methods():
  # Start with an incorrect mode for an existing rule.
  service_url = "http://external-api"
  expected_pattern = f"{service_url}/?.*?"

  existing_rules = build_workflow_filter_rules(
    existing_filter_rules=[],
    service_urls=[service_url],
    workflow_template=WORKFLOW_MOCK_TYPE,
  )
  assert existing_rules[0].modes == [mode.MOCK]

  updated_rules = build_workflow_filter_rules(
    existing_filter_rules=existing_rules,
    service_urls=[service_url],
    workflow_template=WORKFLOW_RECORD_TYPE,
  )

  assert len(updated_rules) == 1
  assert updated_rules[0].pattern == expected_pattern
  assert updated_rules[0].methods == HTTP_METHODS
  assert updated_rules[0].action == filter_action.INCLUDE
  assert updated_rules[0].modes == [mode.RECORD]


def _read_settings(context_dir: pathlib.Path) -> dict:
  settings_path = context_dir / DATA_DIR_NAME / 'settings.yml'
  with open(settings_path, 'r') as fp:
    return yaml.safe_load(fp)


def _filter_patterns(settings: dict) -> list:
  # proxy.filter is a map of project_id -> [rule dicts]
  filter_section = ((settings or {}).get('proxy') or {}).get('filter') or {}
  patterns = []
  if not isinstance(filter_section, dict):
    return patterns
  for value in filter_section.values():
    rules = value if isinstance(value, list) else [value]
    for rule in rules:
      if isinstance(rule, dict) and rule.get('pattern'):
        patterns.append(rule['pattern'])
  return patterns


def _pattern_hostname(pattern):
  if not pattern or not isinstance(pattern, str):
    return None

  parsed = urlparse(pattern)
  if parsed.hostname:
    return parsed.hostname

  # Handle URL-like patterns without scheme, e.g. "api.example.com/path"
  parsed = urlparse(f'//{pattern}')
  return parsed.hostname


def test_workflow_filter_writes_settings_to_context_dir_not_cwd():
  """With --context-dir-path != cwd, filter rules must land in that context's settings.yml."""
  reset()
  runner = CliRunner()
  temp_dir = tempfile.mkdtemp()
  app_dir = pathlib.Path(temp_dir) / 'app'
  context_dir = pathlib.Path(temp_dir) / 'e2e'
  app_dir.mkdir()
  context_dir.mkdir()
  (app_dir / DATA_DIR_NAME).mkdir()
  (app_dir / 'docker.sock').touch()

  try:
    result = runner.invoke(scaffold, [
      'app', 'create',
      '--apply',
      '--docker-socket-path', str(app_dir / 'docker.sock'),
      '--app-dir-path', str(app_dir),
      '--context-dir-path', str(context_dir),
      '--quiet',
      'filter-context-app',
    ])
    assert result.exit_code == 0, result.output

    result = runner.invoke(scaffold, [
      'service', 'create',
      '--apply',
      '--app-dir-path', str(app_dir),
      '--context-dir-path', str(context_dir),
      '--hostname', 'api.example.com',
      '--quiet',
      'api',
    ])
    assert result.exit_code == 0, result.output

    original_cwd = os.getcwd()
    try:
      os.chdir(app_dir)
      result = runner.invoke(scaffold, [
        'workflow', 'filter',
        '--app-dir-path', str(app_dir),
        '--context-dir-path', str(context_dir),
        '--service', 'api',
        'record',
      ])
      assert result.exit_code == 0, result.output
    finally:
      os.chdir(original_cwd)

    context_patterns = _filter_patterns(_read_settings(context_dir))
    assert any(_pattern_hostname(pattern) == 'api.example.com' for pattern in context_patterns)

    app_settings_path = app_dir / DATA_DIR_NAME / 'settings.yml'
    if app_settings_path.exists():
      app_patterns = _filter_patterns(_read_settings(app_dir))
      assert not any(_pattern_hostname(pattern) == 'api.example.com' for pattern in app_patterns)
  finally:
    import shutil
    shutil.rmtree(temp_dir, ignore_errors=True)

