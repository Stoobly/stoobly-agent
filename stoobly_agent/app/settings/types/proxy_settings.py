from typing import Dict, List, Literal, TypedDict

from ..constants import firewall_action
from ..constants import intercept_mode

FirewallAction = Literal[firewall_action.EXCLUDE, firewall_action.INCLUDE]
Method = Literal['DELETE,GET,OPTIONS,POST,PUT']
MockPolicy = Literal['all', 'found', 'none']
Mode = Literal[intercept_mode.MOCK, intercept_mode.RECORD, intercept_mode.TEST]
RecordPolicy = Literal['all','found','none']
TestPolicy = Literal['all','found','none']

class ParameterRule(TypedDict):
  modes: List[Mode]
  name: str
  type: str
  value: str

class DataRules(TypedDict):
  MockPolicy: MockPolicy
  RecordPolicy: RecordPolicy
  scenario_id: str
  TestPolicy: TestPolicy

class FilterRule(TypedDict):
  methods: List[Method]
  pattern: str
  parameter_rules: List[ParameterRule]

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
FilterRules = List[FilterRule]
FilterSettings = Dict[str, FilterRules]
FirewallRules = Dict[str, List[FirewallRule]]
FirewallSettings = Dict[str, FirewallRules]

class ProxySettings(TypedDict):
  data: DataSettings
  filter: FilterSettings
  firewall: FirewallSettings
  intercept: InterceptSettings
  url: str