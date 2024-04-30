from typing import TypedDict

from stoobly_agent.config.constants import alias_resolve_strategy, test_filter, test_output_level, test_strategy
from stoobly_agent.lib import logger

class TestOptions(TypedDict):
  aggregate_failures: bool
  alias_resolve_strategy: alias_resolve_strategy.AliasResolveStrategy
  assign: str
  filter: test_filter.TestFilter
  format: str
  group_by: str
  host: str
  key: str
  lifecycle_hooks_path: str
  log_level: logger.LogLevel
  output_level: test_output_level.TestOutputLevel
  public_directory_path: str
  remote_project_key: str
  report_key: str
  response_fixtures_path: str
  save: str
  scheme: str
  strategy: test_strategy.TestStrategy
  trace_id: str
  validate: str