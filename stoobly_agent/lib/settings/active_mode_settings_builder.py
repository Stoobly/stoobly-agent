from typing import List
from unittest import mock

from stoobly_agent.app.proxy.constants import modes
from stoobly_agent.app.proxy.constants import mock_policy
from stoobly_agent.app.proxy.constants import record_policy
from stoobly_agent.app.proxy.constants import test_strategies

class ActiveModeSettingsBuilder():
  exclude_patterns: list = []
  include_patterns: list = []
  policy: str = None
  project_key: str = None
  rewrite_rules: list = []
  service_url: str = None
  scenario_key: str = None
  test_strategy: str = None
  enabled: bool  = False

  def __init__(self, mode: List[modes.MOCK, modes.RECORD, modes.TEST]):
    if mode == modes.MOCK:
      self.policy = mock_policy.ALL
    elif mode == modes.RECORD:
      self.policy = record_policy.ALL
    elif mode == modes.TEST:
      self.policy = mock_policy.ALL
      self.test_strategy = test_strategies.DIFF

  def with_exclude_patterns(self, patterns: List[str]):
    self.exclude_patterns = patterns
    return self

  def with_include_patterns(self, patterns: List[str]):
    self.include_patterns = patterns
    return self

  def with_policy(self, policy: str):
    self.policy = policy
    return self

  def with_project_key(self, project_key: str):
    self.project_key = project_key
    return self

  def with_rewrite_rules(self, rules: List[str]):
    self.rewrite_rules = rules
    return self

  def with_service_url(self, service_url: str):
    self.service_url = service_url
    return self
  
  def with_scenario_key(self, scenario_key: str):
    self.scenario_key = scenario_key
    return self

  def with_test_strategy(self, test_strategy: str):
    self.test_strategy = test_strategy
    return self

  def with_enabled(self, enabled: bool):
    self.enabled = enabled
    return self

  def build(self):
    return {
      'exclude_patterns' : self.exclude_patterns,
      'include_patterns' : self.include_patterns,
      'policy' : self.policy,
      'project_key': self.project_key,
      'rewrite_rules': self.rewrite_rules,
      'service_url': self.service_url,
      'scenario_key': self.scenario_key,
      'test_strategy': self.test_strategy,
      'enabled': self.enabled,
    }