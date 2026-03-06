import base64
import json
import os
import pdb
import re

from runpy import run_path
from typing import List, Optional, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from mitmproxy.http import Request as MitmproxyRequest

from stoobly_agent.app.settings.constants import firewall_action, intercept_mode
from stoobly_agent.app.settings.parameter_rule import ParameterRule as ParameterRuleClass
from stoobly_agent.app.settings.rewrite_rule import RewriteRule
from stoobly_agent.app.settings.firewall_rule import FirewallRule
from stoobly_agent.app.settings import Settings
from stoobly_agent.app.settings.match_rule import MatchRule as MatchRuleClass
from stoobly_agent.app.settings.types import IgnoreRule, MatchRule
from stoobly_agent.app.settings.url_rule import UrlRule as UrlRuleClass
from stoobly_agent.app.models.scenario_model import ScenarioModel
from stoobly_agent.config.constants import custom_headers, env_vars, mode, request_origin, test_filter
from stoobly_agent.lib.api.keys.project_key import InvalidProjectKey, ProjectKey
from stoobly_agent.lib.api.keys.scenario_key import InvalidScenarioKey, ScenarioKey
from stoobly_agent.lib.cache import Cache
from stoobly_agent.lib.logger import Logger

class InterceptSettings:

  def __init__(self, settings: Settings, request: 'MitmproxyRequest' = None, cache: Optional[Cache] = None, scenario_model: Optional[ScenarioModel] = None):
    self.__settings = settings
    self.__request = request
    # Lazy import for runtime usage
    from mitmproxy.http import Request as MitmproxyRequest
    self.__headers: 'MitmproxyRequest.headers' = request.headers if request else None
    self.__for_response = False
    self.__cache = cache
    self.__scenario_model = scenario_model

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

    self._mock_rewrite_rules = None
    self._record_rewrite_rules = None
    self._replay_rewrite_rules = None
    self._test_rewrite_rules = None

  def with_cache(self, cache: Cache):
    """Set cache using fluent interface pattern."""
    self.__cache = cache
    return self

  def with_scenario_model(self, scenario_model: ScenarioModel):
    """Set scenario_model using fluent interface pattern."""
    self.__scenario_model = scenario_model
    return self

  @property
  def settings(self):
    return self.__settings

  @property
  def alias_resolve_strategy(self):
    if self.__headers and custom_headers.ALIAS_RESOLVE_STRATEGY in self.__headers:
      return self.__headers[custom_headers.ALIAS_RESOLVE_STRATEGY]

  @property
  def active(self):
    # If proxy mode is explicitly set, use it to determine if intercept is active
    if self.__headers and custom_headers.PROXY_MODE in self.__headers:
      if custom_headers.INTERCEPT_ACTIVE in self.__headers and self.__headers[custom_headers.INTERCEPT_ACTIVE] == '0':
        return False
      
      return self.__headers[custom_headers.PROXY_MODE] != mode.NONE

    if self.__headers and custom_headers.INTERCEPT_ACTIVE in self.__headers:
      return self.__headers[custom_headers.INTERCEPT_ACTIVE] == '1'

    return self.__intercept_settings.active
    
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
      intercept_active_header = custom_headers.INTERCEPT_ACTIVE

      if access_control_header and intercept_active_header.lower() in access_control_header:
          return mode.NONE

      if self.__headers.get(intercept_active_header) == '0':
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
    """Returns comma-separated list of public directory paths, optionally with origin prefix.
    
    Examples:
      - Single path: '/path/to/public'
      - Multiple paths: '/path/to/public1,/path/to/public2'
      - With origin: 'https://example.com:/path/to/public'
      - Combined: 'https://api.example.com:/public1,/public2,https://other.com:/public3'
    """
    if self.__headers and custom_headers.PUBLIC_DIRECTORY_PATH in self.__headers:
      return self.__headers[custom_headers.PUBLIC_DIRECTORY_PATH]
    elif os.environ.get(env_vars.AGENT_PUBLIC_DIRECTORY_PATH):
      return os.environ[env_vars.AGENT_PUBLIC_DIRECTORY_PATH]
    return None

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
    """Returns comma-separated list of response fixtures paths, optionally with origin prefix.
    
    Examples:
      - Single path: '/path/to/fixtures.json'
      - Multiple paths: '/path/to/fixtures1.json,/path/to/fixtures2.json'
      - With origin: 'https://example.com:/path/to/fixtures.json'
      - Combined: 'https://api.example.com:/fixtures1.json,/fixtures2.json,https://other.com:/fixtures3.json'
    """
    if self.__headers and custom_headers.RESPONSE_FIXTURES_PATH in self.__headers:
      return self.__headers[custom_headers.RESPONSE_FIXTURES_PATH]

    if os.environ.get(env_vars.AGENT_RESPONSE_FIXTURES_PATH):
      return os.environ[env_vars.AGENT_RESPONSE_FIXTURES_PATH] 

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

    # Check if scenario name header is set
    if self.__headers and custom_headers.SCENARIO_NAME in self.__headers:
        scenario_name = self.__headers[custom_headers.SCENARIO_NAME]
        
        # Check cache first if available
        if self.__cache:
            parsed_project_key = self.parsed_project_key
            project_id = parsed_project_key.id if parsed_project_key else None

            if project_id is None:
                return None

            cache_key = f'scenario_name_index.{project_id}'
            cache_data = self.__cache.read(cache_key)
            
            # Get existing mapping or create new one
            if cache_data and cache_data.get('value'):
                scenario_name_to_key_map = cache_data['value']
            else:
                scenario_name_to_key_map = {}
            
            # Check if scenario name is already in cache, for None values, allow cache miss
            # This will ensure that if the user creates a new scenario after a cache miss, it will be cached.
            if scenario_name in scenario_name_to_key_map and scenario_name_to_key_map[scenario_name]:
                return scenario_name_to_key_map[scenario_name]
            
            # Cache miss, query ScenarioModel if available
            if self.__scenario_model:
                try:
                    scenario_key = None
                    
                    if project_id is not None:
                        response, status = self.__scenario_model.index(
                          project_id=project_id, q=scenario_name, sort_by='requests_count'
                        )
                        if status == 200 and response.get('list') and len(response['list']) > 0:
                            # Find first scenario that exactly matches the name
                            for scenario in response['list']:
                                if scenario.get('name') == scenario_name:
                                    scenario_key = scenario.get('key')
                                    break
                    
                    # Do not cache if scenario key is not found
                    # If the user is recording requests, they may create a new scenario after a cache miss
                    # This would result in a cache miss loop until the agent restarts, so we do not cache the result
                    if scenario_key:
                      scenario_name_to_key_map[scenario_name] = scenario_key
                      self.__cache.write(cache_key, scenario_name_to_key_map, timeout=None)

                    return scenario_key
                except Exception as e:
                    Logger.instance().error(f"Error querying scenario by name: {e}")
                    return None

    return self.__data_rules.scenario_key

  @property
  def parsed_scenario_key(self):
    _scenario_key = self.scenario_key
    if not _scenario_key:
      return None

    try: 
      return ScenarioKey(self.scenario_key)
    except InvalidScenarioKey:
      pass

  @scenario_key.setter
  def scenario_key(self, v):
    self.__data_rules.scenario_key = v

  @property
  def scenario_model(self):
    return self.__scenario_model

  @property
  def report_key(self) -> Union[str, None]:
    if self.__headers and custom_headers.REPORT_KEY in self.__headers:
      return self.__headers[custom_headers.REPORT_KEY]

  @property
  def order(self):
    return self.__order(self.mode)

  @property
  def order_from_header(self):
    return self.__order_from_header(self.mode)

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
  def record_strategy(self):
    if self.__headers and custom_headers.RECORD_STRATEGY in self.__headers:
      return self.__headers[custom_headers.RECORD_STRATEGY]

    return self.__data_rules.record_strategy

  @property
  def exclude_rules(self) -> List[FirewallRule]:
    _mode = self.mode
    return self.exclude_rules_for_mode(_mode)

  @property
  def include_rules(self) -> List[FirewallRule]:
    _mode = self.mode
    return self.include_rules_for_mode(_mode)

  @property
  def match_rules(self) -> List[MatchRule]:
    _mode = self.mode
    rules = list(filter(lambda rule: _mode in rule.modes, self.__match_rules))
    
    # Append rules from X-Stoobly-Request-Match-Rules header (base64-encoded JSON)
    # Expected format from stoobly-js:
    # [
    #   {
    #     modes: ['replay', 'mock'],
    #     components: 'Header'  // Single RequestParameter value
    #   }
    # ]
    if self.__headers and custom_headers.REQUEST_MATCH_RULES in self.__headers and self.__request:
      value = self.__headers[custom_headers.REQUEST_MATCH_RULES]
      if value:
        try:
          decoded = base64.b64decode(value).decode('utf-8')
          match_rules_data = json.loads(decoded)
          if isinstance(match_rules_data, list):
            for match_rule_data in match_rules_data:
              if not isinstance(match_rule_data, dict):
                continue
              
              # Get components - stoobly-js sends a single string, but agent expects array
              components_value = match_rule_data.get('components')
              if not components_value or not isinstance(components_value, str):
                continue
              
              # Convert single component to array (agent expects List[RequestComponent])
              components = [components_value.strip()]
              
              # Get modes (optional, defaults to current mode)
              modes = match_rule_data.get('modes', [_mode])
              if not isinstance(modes, list):
                modes = [_mode]
              
              header_rule = MatchRuleClass({
                'components': components,
                'methods': [self.__request.method.upper()],
                'modes': modes,
                'pattern': re.escape(self.__request.url),
              })
              rules.append(header_rule)
        except (json.JSONDecodeError, ValueError) as e:
          Logger.instance().warn(f"Invalid X-Stoobly-Request-Match-Rules header: {e}")
    return rules

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
    if not self._record_rewrite_rules:
      self._record_rewrite_rules = self.__select_rewrite_rules(mode.RECORD)
    return self._record_rewrite_rules

  @property
  def mock_rewrite_rules(self) -> List[RewriteRule]:
    if not self._mock_rewrite_rules:
      self._mock_rewrite_rules = self.__select_rewrite_rules(mode.MOCK)
    return self._mock_rewrite_rules

  @property
  def replay_rewrite_rules(self) -> List[RewriteRule]:
    if not self._replay_rewrite_rules:
      self._replay_rewrite_rules = self.__select_rewrite_rules(mode.REPLAY)
    return self._replay_rewrite_rules

  @property
  def test_rewrite_rules(self) -> List[RewriteRule]:
    if not self._test_rewrite_rules:
      self._test_rewrite_rules = self.__select_rewrite_rules(mode.TEST)
    return self._test_rewrite_rules

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

    return request_origin.PROXY

  def exclude_rules_for_mode(self, mode: str) -> List[FirewallRule]:
    return list(filter(lambda rule: mode in rule.modes and rule.action == firewall_action.EXCLUDE, self.__firewall_rules))

  def include_rules_for_mode(self, mode: str) -> List[FirewallRule]:
    return list(filter(lambda rule: mode in rule.modes and rule.action == firewall_action.INCLUDE, self.__firewall_rules))

  def for_response(self):
    self.__for_response = True

  def __select_rewrite_rules(self, mode = None):
    mode = mode or self.mode
    rules = []

    # Filter only parameters matching active intercept mode
    for rewrite_rule in self.__rewrite_rules:
      # If url rule applies, then update .url_rules with url_rule
      url_rules = self.__select_url_rules(rewrite_rule, mode)

      # If parameters rules apply, then update .parameter_rules with applicable parameter_rules
      parameter_rules = self.__select_parameter_rules(rewrite_rule, mode)

      if len(url_rules) > 0 or len(parameter_rules) > 0:
        # Build a new RewriteRule object contain only parameter rules matching intercept mode
        rewrite_rule = RewriteRule(rewrite_rule.to_dict())
        rewrite_rule.url_rules = url_rules
        rewrite_rule.parameter_rules = parameter_rules
        rules.append(rewrite_rule)

    # Append rules from X-Stoobly-Request-Rewrite-Rules header (base64-encoded JSON)
    # Expected format from stoobly-js (using snake_case):
    # [
    #   {
    #     url_rules: [{path: '/new-path', port: '8080', scheme: 'https'}],
    #     parameter_rules: [{type: 'header', name: 'foo', value: 'bar'}]
    #   }
    # ]
    if self.__headers and custom_headers.REQUEST_REWRITE_RULES in self.__headers and self.__request:
      try:
        value = self.__headers[custom_headers.REQUEST_REWRITE_RULES]
        if value:
          decoded = base64.b64decode(value).decode('utf-8')
          rewrite_rules_data = json.loads(decoded)
          if isinstance(rewrite_rules_data, list) and len(rewrite_rules_data) > 0:
            for rewrite_rule_data in rewrite_rules_data:
              if not isinstance(rewrite_rule_data, dict):
                continue
              
              # Parse parameter rules (using snake_case)
              parameter_rules = []
              parameter_rules_data = rewrite_rule_data.get('parameter_rules', [])
              if isinstance(parameter_rules_data, list):
                for item in parameter_rules_data:
                  if isinstance(item, dict) and item.get('type') and item.get('name') is not None and item.get('value') is not None:
                    parameter_rules.append(ParameterRuleClass({
                      'modes': [mode],
                      'name': str(item['name']),
                      'type': str(item['type']),
                      'value': str(item['value']),
                    }))
              
              # Parse URL rules (using snake_case)
              url_rules = []
              url_rules_data = rewrite_rule_data.get('url_rules', [])
              if isinstance(url_rules_data, list):
                for item in url_rules_data:
                  if isinstance(item, dict):
                    url_rule_dict = {'modes': [mode]}
                    if 'path' in item:
                      url_rule_dict['path'] = str(item['path'])
                    if 'port' in item:
                      url_rule_dict['port'] = str(item['port'])
                    if 'scheme' in item:
                      url_rule_dict['scheme'] = str(item['scheme'])
                    url_rules.append(UrlRuleClass(url_rule_dict))
              
              # Only create a rewrite rule if we have at least one parameter or URL rule
              if parameter_rules or url_rules:
                header_rewrite_rule = RewriteRule({
                  'methods': [self.__request.method.upper()],
                  'pattern': re.escape(self.__request.url),
                  'parameter_rules': [r.to_dict() for r in parameter_rules],
                  'url_rules': [r.to_dict() for r in url_rules],
                })
                rules.append(header_rewrite_rule)
      except (json.JSONDecodeError, ValueError, KeyError) as e:
        Logger.instance().warn(f"Invalid X-Stoobly-Request-Rewrite-Rules header: {e}")

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

  def __order(self, mode):
    if mode == intercept_mode.RECORD:
      if self.__headers and custom_headers.RECORD_ORDER in self.__headers:
        return self.__headers[custom_headers.RECORD_ORDER]

      return self.__data_rules.record_order

  def __order_from_header(self, mode):
    if mode == intercept_mode.RECORD:
      if self.__headers and custom_headers.RECORD_ORDER in self.__headers:
        return self.__headers[custom_headers.RECORD_ORDER]

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
      if self.__headers and custom_headers.TEST_POLICY in self.__headers:
        return self.__headers[custom_headers.TEST_POLICY]

      return self.__data_rules.test_policy
    elif mode == intercept_mode.REPLAY:
      return self.__data_rules.replay_policy
