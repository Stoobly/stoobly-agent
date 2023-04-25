import os
import pdb

from runpy import run_path
from typing import List, Union

from mitmproxy.http import Request as MitmproxyRequest

from stoobly_agent.app.settings.constants import firewall_action, intercept_mode
from stoobly_agent.app.settings.rewrite_rule import RewriteRule
from stoobly_agent.app.settings.firewall_rule import FirewallRule
from stoobly_agent.app.settings import Settings
from stoobly_agent.app.settings.types import IgnoreRule, MatchRule, RedactRule
from stoobly_agent.config.constants import custom_headers, mode, request_origin, test_filter
from stoobly_agent.lib.api.keys.project_key import InvalidProjectKey, ProjectKey
from stoobly_agent.lib.logger import Logger

class InterceptSettings:

  def __init__(self, settings: Settings, request: MitmproxyRequest = None):
    self.__settings = settings
    self.__request = request
    self.__headers: MitmproxyRequest.headers = request.headers if request else None
    self.__for_response = False

    project_id = None

    try: 
      project_key = ProjectKey(self.project_key)
      project_id = project_key.id
    except InvalidProjectKey:
      pass

    # If no valid project key is provided, use default settings,
    # Otherwise, set settings for the project
    self.__data_rules = self.__settings.proxy.data.data_rules(project_id)
    self.__rewrite_rules = self.__settings.proxy.rewrite.rewrite_rules(project_id)
    self.__firewall_rules = self.__settings.proxy.firewall.firewall_rules(project_id)
    self.__intercept_settings = self.__settings.proxy.intercept 
    self.__match_rules = self.__settings.proxy.match.match_rules(project_id)

    self.__lifecycle_hooks = None
    self.__initialize_lifecycle_hooks()

  @property
  def settings(self):
    return self.__settings

  @property
  def alias_resolve_strategy(self):
    if self.__headers and custom_headers.ALIAS_RESOLVE_STRATEGY in self.__headers:
      return self.__headers[custom_headers.ALIAS_RESOLVE_STRATEGY]

  @property
  def active(self):
    if self.__intercept_settings.active:
      return True

    if not self.__headers:
      return False
    
    return custom_headers.PROXY_MODE in self.__headers

  @property
  def lifecycle_hooks_script_path(self):
    if self.__headers and custom_headers.LIFECYCLE_HOOKS_SCRIPT_PATH in self.__headers:
      return self.__headers[custom_headers.LIFECYCLE_HOOKS_SCRIPT_PATH]

  @property
  def lifecycle_hooks(self):
    return self.__lifecycle_hooks or {}

  @property
  def mode(self):
    if self.__headers:
      if self.__for_response and custom_headers.RESPONSE_PROXY_MODE in self.__headers:
        return self.__headers[custom_headers.RESPONSE_PROXY_MODE]

      access_control_header = self.__headers.get('Access-Control-Request-Headers')
      do_proxy_header = custom_headers.DO_PROXY

      if access_control_header and do_proxy_header.lower() in access_control_header:
          return mode.NONE

      if do_proxy_header in self.__headers:
          return mode.NONE

      if custom_headers.PROXY_MODE in self.__headers:
          return self.__headers[custom_headers.PROXY_MODE]

    return self.__intercept_settings.mode

  @property
  def project_key(self):
    if self.__headers and custom_headers.PROJECT_KEY in self.__headers:
        return self.__headers[custom_headers.PROJECT_KEY]

    return self.__settings.proxy.intercept.project_key

  @property
  def scenario_key(self):
    if self.__headers and custom_headers.SCENARIO_KEY in self.__headers:
        return self.__headers[custom_headers.SCENARIO_KEY]

    return self.__data_rules.scenario_key

  @scenario_key.setter
  def scenario_key(self, v):
    self.__data_rules.scenario_key = v

  @property
  def report_key(self) -> Union[str, None]:
    if self.__headers and custom_headers.REPORT_KEY in self.__headers:
      return self.__headers[custom_headers.REPORT_KEY]

  @property
  def policy(self):
    return self.__policy(self.mode)

  @property
  def response_policy(self):
    if self.__headers and custom_headers.RESPONSE_PROXY_MODE in self.__headers:
      mode = self.__headers[custom_headers.RESPONSE_PROXY_MODE]
      return self.__policy(mode)

    return self.policy

  @property
  def exclude_rules(self) -> List[FirewallRule]:
    _mode = self.mode
    return list(filter(lambda rule: _mode in rule.modes and rule.action == firewall_action.EXCLUDE, self.__firewall_rules))

  @property
  def include_rules(self) -> List[FirewallRule]:
    _mode = self.mode
    return list(filter(lambda rule: _mode in rule.modes and rule.action == firewall_action.INCLUDE, self.__firewall_rules))

  @property
  def match_rules(self) -> List[MatchRule]:
    _mode = self.mode
    return list(filter(lambda rule: _mode in rule.modes, self.__match_rules))

  # TODO: explore if should support specifying components to ignore
  @property
  def ignore_rules(self) -> List[IgnoreRule]:
    return []

  @property
  def rewrite_rules(self) -> List[RewriteRule]:
    _mode = self.mode
    return self.__select_rewrite_rules(_mode)

  @property
  def record_rewrite_rules(self) -> List[RedactRule]:
    return self.__select_rewrite_rules(mode.RECORD)

  @property
  def mock_rewrite_rules(self) -> List[RedactRule]:
    return self.__select_rewrite_rules(mode.MOCK)

  @property
  def replay_rewrite_rules(self) -> List[RewriteRule]:
    return self.__select_rewrite_rules(mode.REPLAY)

  @property
  def test_rewrite_rules(self) -> List[RewriteRule]:
    return self.__select_rewrite_rules(mode.TEST)

  @property
  def upstream_url(self):
    if self.__headers and custom_headers.SERVICE_URL in self.__headers:
      return self.__headers[custom_headers.SERVICE_URL]

    settings_upstream_url = self.__intercept_settings.upstream_url
    if settings_upstream_url and len(settings_upstream_url) > 0:
      return self.__intercept_settings.upstream_url

    if self.__request:
      return f"{self.__request.scheme}://{self.__request.host}:{self.__request.port}"

  @property
  def test_filter(self):
    if self.__headers and custom_headers.TEST_FILTER in self.__headers:
      return self.__headers[custom_headers.TEST_FILTER]

    return test_filter.ALL
  
  @property
  def test_strategy(self):
    if self.__headers and custom_headers.TEST_STRATEGY in self.__headers:
      return self.__headers[custom_headers.TEST_STRATEGY]

    return self.__data_rules.test_strategy

  @property
  def request_origin(self):
    if self.__headers and custom_headers.REQUEST_ORIGIN in self.__headers:
      return self.__headers[custom_headers.REQUEST_ORIGIN]

    return request_origin.WEB

  def for_response(self):
    self.__for_response = True

  def __select_rewrite_rules(self, mode = None):
    rules = []

    # Filter only parameters matching active intercept mode
    for rewrite_rule in self.__rewrite_rules:
      parameter_rules = self.__select_parameter_rules(rewrite_rule, mode)

      # If no parameters rules were found, then this filter rule is not applied
      if len(parameter_rules) == 0:
        continue

      # Build a new RewriteRule object contain only parameter rules matching intercept mode
      rewrite_rule = RewriteRule({
        'methods': rewrite_rule.methods,
        'pattern': rewrite_rule.pattern,
        'parameters_rules': [], # Has to be dict form, manually set it
      })
      rewrite_rule.parameter_rules = parameter_rules

      rules.append(rewrite_rule)

    return rules

  def __select_parameter_rules(self, rewrite_rule: RewriteRule, mode = None):
    mode = mode or self.mode
    return list(filter(
      lambda parameter: mode in parameter.modes and parameter.name, 
      rewrite_rule.parameter_rules or []
    ))

  def __initialize_lifecycle_hooks(self):
    script_path = self.lifecycle_hooks_script_path

    if not script_path:
        return

    if not os.path.exists(script_path):
        return Logger.instance().error(f"Lifecycle hooks script {script_path} does not exist")

    try:
        self.__lifecycle_hooks = run_path(script_path)
    except Exception as e:
        return Logger.instance().error(e)

  def __policy(self, mode):
    if mode == intercept_mode.MOCK:
      if self.__headers and custom_headers.MOCK_POLICY in self.__headers:
        return self.__headers[custom_headers.MOCK_POLICY]

      return self.__data_rules.mock_policy
    elif mode == intercept_mode.RECORD:
      if self.__headers and custom_headers.RECORD_POLICY in self.__headers:
        return self.__headers[custom_headers.RECORD_POLICY]

      return self.__data_rules.record_policy
    elif mode == intercept_mode.TEST:
      return self.__data_rules.test_policy
    elif mode == intercept_mode.REPLAY:
      return self.__data_rules.replay_policy