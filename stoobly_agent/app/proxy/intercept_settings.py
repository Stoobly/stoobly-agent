import os
import pdb
import yaml

from runpy import run_path
from typing import List, Union

from mitmproxy.http import Request as MitmproxyRequest

from stoobly_agent.app.settings.constants import firewall_action, intercept_mode
from stoobly_agent.app.settings.rewrite_rule import RewriteRule
from stoobly_agent.app.settings.firewall_rule import FirewallRule
from stoobly_agent.app.settings import Settings
from stoobly_agent.app.settings.types import IgnoreRule, MatchRule
from stoobly_agent.config.constants import custom_headers, env_vars, mode, request_origin, test_filter
from stoobly_agent.lib.api.keys.project_key import InvalidProjectKey, ProjectKey
from stoobly_agent.lib.logger import Logger

class InterceptSettings:

  def __init__(self, settings: Settings, request: MitmproxyRequest = None):
    self.__settings = settings
    self.__request = request
    self.__headers: MitmproxyRequest.headers = request.headers if request else None
    self.__for_response = False

    parsed_project_key = self.parsed_project_key
    project_id = parsed_project_key.id if parsed_project_key else None

    # If no valid project key is provided, use default settings,
    # Otherwise, set settings for the project
    self.__data_rules = self.__settings.proxy.data.data_rules(project_id)
    self.__rewrite_rules = self.__settings.proxy.rewrite.rewrite_rules(project_id)
    self.__firewall_rules = self.__settings.proxy.firewall.firewall_rules(project_id)
    self.__intercept_settings = self.__settings.proxy.intercept 
    self.__match_rules = self.__settings.proxy.match.match_rules(project_id)

    self.__lifecycle_hooks = None
    self.__initialize_lifecycle_hooks()

    self.__response_fixtures = None
    self.__initialize_response_fixtures()

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
  def lifecycle_hooks_path(self):
    if self.__headers and custom_headers.LIFECYCLE_HOOKS_PATH in self.__headers:
      return self.__headers[custom_headers.LIFECYCLE_HOOKS_PATH]

    if os.environ.get(env_vars.AGENT_LIFECYCLE_HOOKS_PATH):
      return os.environ[env_vars.AGENT_LIFECYCLE_HOOKS_PATH] 

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
  def parsed_project_key(self):
    try: 
      return ProjectKey(self.project_key)
    except InvalidProjectKey:
      pass

  @property
  def public_directory_path(self):
    if self.__headers and custom_headers.PUBLIC_DIRECTORY_PATH in self.__headers:
      return self.__headers[custom_headers.PUBLIC_DIRECTORY_PATH]

    if os.environ.get(env_vars.AGENT_PUBLIC_DIRECTORY_PATH):
      return os.environ[env_vars.AGENT_PUBLIC_DIRECTORY_PATH] 

  @property
  def remote_project_key(self):
    # When not local project, don't return set remote project_key
    project_key = self.parsed_project_key
    if project_key and not project_key.is_local:
      return 

    if self.__headers and custom_headers.REMOTE_PROJECT_KEY in self.__headers:
      return self.__headers[custom_headers.REMOTE_PROJECT_KEY]

    return self.__settings.remote.project_key

  @property
  def response_fixtures_path(self):
    if self.__headers and custom_headers.RESPONSE_FIXTURES_PATH in self.__headers:
      return self.__headers[custom_headers.RESPONSE_FIXTURES_PATH]

    if os.environ.get(env_vars.AGENT_RESPONSE_FIXTURES_PATH):
      return os.environ[env_vars.AGENT_RESPONSE_FIXTURES_PATH] 

  @property
  def response_fixtures(self):
    return self.__response_fixtures or {}

  @property
  def parsed_remote_project_key(self):
    try: 
      return ProjectKey(self.remote_project_key)
    except InvalidProjectKey:
      pass
    
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
  def record_rewrite_rules(self) -> List[RewriteRule]:
    return self.__select_rewrite_rules(mode.RECORD)

  @property
  def mock_rewrite_rules(self) -> List[RewriteRule]:
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
  def test_save_results(self):
    if self.__headers and custom_headers.TEST_SAVE_RESULTS in self.__headers:
      return not not int(self.__headers[custom_headers.TEST_SAVE_RESULTS])

    return False

  @property
  def test_skip(self):
    if self.__headers and custom_headers.TEST_SKIP in self.__headers:
      return True
    
    return False
  
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
      # If url rule applies, then update .url_rules with url_rule
      url_rules = self.__select_url_rules(rewrite_rule)

      # If parameters rules apply, then update .parameter_rules with applicable parameter_rules
      parameter_rules = self.__select_parameter_rules(rewrite_rule, mode)

      if len(url_rules) > 0 or len(parameter_rules) > 0:
        # Build a new RewriteRule object contain only parameter rules matching intercept mode
        rewrite_rule = RewriteRule(rewrite_rule.to_dict())
        rewrite_rule.url_rules = url_rules
        rewrite_rule.parameter_rules = parameter_rules
        rules.append(rewrite_rule)

    return rules

  def __select_parameter_rules(self, rewrite_rule: RewriteRule, mode = None):
    mode = mode or self.mode
    return list(filter(
      lambda parameter: mode in parameter.modes and parameter.name, 
      rewrite_rule.parameter_rules or []
    ))

  def __select_url_rules(self, rewrite_rule: RewriteRule, mode = None):
    mode = mode or self.mode
    return list(filter(
      lambda url: mode in url.modes,
      rewrite_rule.url_rules or []
    ))

  def __initialize_lifecycle_hooks(self):
    script_path = self.lifecycle_hooks_path

    if not script_path:
        return

    if not os.path.exists(script_path):
        return Logger.instance().error(f"Lifecycle hooks script {script_path} does not exist")

    try:
        self.__lifecycle_hooks = run_path(script_path)
    except Exception as e:
        return Logger.instance().error(e)

  def __initialize_response_fixtures(self):
    fixtures_path = self.response_fixtures_path

    if not fixtures_path:
        return

    if not os.path.exists(fixtures_path):
        return Logger.instance().error(f"Response fixtures {fixtures_path} does not exist")

    with open(fixtures_path, 'r') as stream:
        try:
            self.__response_fixtures = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            Logger.instance().error(exc)
        
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