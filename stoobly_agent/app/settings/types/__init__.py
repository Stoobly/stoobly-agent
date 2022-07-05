from .cli_settings import *
from .proxy_settings import *
from .remote_settings import *
from .ui_settings import *

from typing import List, Optional, TypedDict, Union

class Ignore(TypedDict):
    name: str
    type: str

class Redact(TypedDict):
    name: str
    type: str

class Rewrite(TypedDict):
    name: Optional[str]
    type: str
    value: str

class IgnoreRule(TypedDict):
    ignores: List[Ignore]
    method: str
    pattern: str

class RedactRule(TypedDict):
    redacts: List[Redact]
    method: str
    pattern: str

class RewriteRule(TypedDict):
    rewrites: List[Rewrite]
    method: str
    pattern: str

class IProjectRecordSettings(TypedDict):
    enabled: bool
    exclude_patterns: list
    rewrite_rules: list
    include_patterns: list
    policy: str
    project_key: str
    service_url: str
    scenario_key: str

class IProjectMockSettings(TypedDict):
    enabled: bool
    exclude_patterns: list
    include_patterns: list
    policy: str
    project_key: str
    service_url: str
    scenario_key: str

class IProjectTestSettings(TypedDict):
    exclude_patterns: list
    include_patterns: list
    policy: str
    project_key: str
    rewrite_rules: list
    service_url: str
    scenario_key: str
    test_strategy: str
    enabled: bool

class IRecordSettings(TypedDict):
    enabled: bool
    project_key: str
    settings: dict

class IMockSettings(TypedDict):
    enabled: bool
    project_key: str
    settings: dict

class ITestSettings(TypedDict):
    enabled: bool
    project_key: str
    settings: dict

class ISettingsMode(TypedDict):
    active: str
    record: IRecordSettings
    mock: IMockSettings
    test: ITestSettings

class ISettings(TypedDict):
    agent_url: str
    api_url: str
    api_key: str
    mode: ISettingsMode
    proxy_config_path: str

Component = {
    'Header': 'Header',
    'BodyParam': 'Body Param',
    'QueryParam': 'Query Param',
}
IProjectModeSettings = Union[IProjectMockSettings, IProjectRecordSettings, IProjectTestSettings]
Rule = Union[IgnoreRule, RedactRule, RewriteRule]