from typing import Dict, List, Literal, TypedDict

from ..constants.firewall_action import FirewallAction
from ..constants.intercept_mode import Mode
from ..constants.request_component import RequestComponent

Method = Literal['DELETE,GET,OPTIONS,POST,PUT']
MockPolicy = Literal['all', 'found', 'none']
RecordPolicy = Literal['all','found','none']
TestPolicy = Literal['all','found','none']

class ParameterRule(TypedDict):
  modes: List[Mode]
  name: str
  type: str
  value: str

class UrlRule(TypedDict):
  hostname: str
  modes: List[Mode]
  port: str
  scheme: str

class DataRules(TypedDict):
  mock_policy: MockPolicy
  record_policy: RecordPolicy
  scenario_id: str
  test_policy: TestPolicy

class MatchRule(TypedDict):
  components: List[RequestComponent]
  modes: List[Mode]
  pattern: str

class RewriteRule(TypedDict):
  methods: List[Method]
  pattern: str
  parameter_rules: List[ParameterRule]
  url_rule: List[UrlRule]

class FirewallRule(TypedDict):
  action: List[FirewallAction]
  modes: List[Mode]
  pattern: str

class InterceptSettings(TypedDict):
  active: bool
  mode: Mode
  project_id: str
  scenario_id: str
  upstream_url: str

DataSettings = Dict[str, DataRules]
MatchRules = Dict[str, List[MatchRule]]
MatchSettings = Dict[str, MatchRules]
RewriteRules = List[RewriteRule]
RewriteSettings = Dict[str, RewriteRules]
FirewallRules = Dict[str, List[FirewallRule]]
FirewallSettings = Dict[str, FirewallRules]

class ProxySettings(TypedDict):
  data: DataSettings
  filter: RewriteSettings
  firewall: FirewallSettings
  intercept: InterceptSettings
  match: MatchSettings
  url: str