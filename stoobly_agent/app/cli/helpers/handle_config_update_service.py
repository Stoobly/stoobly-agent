import pdb

from typing import TypedDict

from stoobly_agent.app.models.scenario_model import ScenarioModel
from stoobly_agent.app.settings.constants import intercept_mode
from stoobly_agent.app.settings.constants.intercept_mode import Mode
from stoobly_agent.app.settings import ProxySettings, Settings
from stoobly_agent.config.constants import record_policy
from stoobly_agent.lib.api.keys.project_key import ProjectKey
from stoobly_agent.lib.api.keys.scenario_key import ScenarioKey

class Context(TypedDict):
  current_proxy_settings: ProxySettings
  mode: Mode

def context() -> Context:
  return {
    'current_proxy_settings': __current_proxy_settings()
  }

def handle_intercept_active_update(new_settings: Settings, context: Context = None):
  data_rule = __data_rule(new_settings.proxy)
  is_active = new_settings.proxy.intercept.active
  old_proxy_settings = __current_proxy_settings(context)
  was_active = old_proxy_settings.intercept.active
  _mode = context['mode'] if context and context.get('mode') else new_settings.proxy.intercept.mode

  if not was_active and is_active:
    if _mode == intercept_mode.RECORD:
      new_policy = data_rule.record_policy
      scenario_key = data_rule.scenario_key
      _scenario_key = __parse_scenario_key(scenario_key)

      if _scenario_key:
        scenario_model = ScenarioModel(new_settings)

        if new_policy == record_policy.OVERWRITE:
          # If policy is overwrite when recording, whenever intercept is enabled,
          # set active scenario to be overwritable
          scenario_model.update(_scenario_key.id, **{ 'overwritable': True })[1]
        else:
          scenario_model.update(_scenario_key.id, **{ 'overwritable': False })[1]
  elif was_active and not is_active:
    if _mode == intercept_mode.RECORD:
      old_proxy_settings = __current_proxy_settings(context)
      old_policy = __data_rule(old_proxy_settings).record_policy

      if old_policy == record_policy.OVERWRITE:
        scenario_key = data_rule.scenario_key
        _scenario_key = __parse_scenario_key(scenario_key)

        if _scenario_key:
          scenario_model = ScenarioModel(new_settings)

          # If policy is overwrite when recording, whenever intercept is disabled,
          # set active scenario to not be overwritable
          scenario_model.update(_scenario_key.id, **{ 'overwritable': False })[1]
    elif _mode == intercept_mode.MOCK:
      # When mock is stopped, clear request access counts
      from stoobly_agent.app.models.factories.resource.local_db.helpers.tiebreak_scenario_request import reset

      reset()

def handle_scenario_update(new_settings: Settings, context = None):
  new_scenario_key = __scenario_key(new_settings.proxy)
  if not new_scenario_key:
    return

  old_proxy_settings = __current_proxy_settings(context)
  old_scenario_key = __scenario_key(old_proxy_settings)

  if old_scenario_key != new_scenario_key:
    data_rule = __data_rule(new_settings.proxy)

    if data_rule.record_policy == record_policy.OVERWRITE:
      scenario_model = ScenarioModel(new_settings)

      _old_scenario_key = __parse_scenario_key(old_scenario_key)
      if _old_scenario_key:
        scenario_model.update(_old_scenario_key.id, **{ 'overwritable': False })[1]

      _new_scenario_key = __parse_scenario_key(new_scenario_key)
      if new_scenario_key:
        scenario_model.update(_new_scenario_key.id, **{ 'overwritable': True })[1]

def handle_project_update(new_settings: Settings, context: Context = None):
  new_project_key = new_settings.proxy.intercept.project_key
  if not new_project_key:
    return

  old_proxy_settings = __current_proxy_settings(context)
  old_project_key = __project_key(old_proxy_settings)

  # If the active project changed, stop intercepting 
  if new_project_key != old_project_key:
    if old_proxy_settings.intercept.active:
        new_settings.proxy.intercept.active = False

  # Check to see if scenario belongs to current project
  data_rule = __data_rule(old_proxy_settings)
  new_scenario_key = data_rule.scenario_key

  _new_scenario_key = __parse_scenario_key(new_scenario_key)
  if _new_scenario_key:
    _project_key = ProjectKey(new_project_key)
    
    if _project_key.id != _new_scenario_key.project_id:
      data_rule.scenario_key = None

def handle_policy_update(new_settings: Settings, context: Context = None):
  data_rule = __data_rule(new_settings.proxy)
  _mode = context['mode'] if context and context.get('mode') else new_settings.proxy.intercept.mode

  old_proxy_settings = __current_proxy_settings(context)
  old_data_rule = __data_rule(old_proxy_settings)

  if _mode == intercept_mode.RECORD:
    new_policy = data_rule.record_policy
    old_policy = old_data_rule.record_policy

    if new_policy != old_policy and old_policy == record_policy.OVERWRITE:
      scenario_key = data_rule.scenario_key
      _scenario_key = __parse_scenario_key(scenario_key)

      if _scenario_key:
        scenario_model = ScenarioModel(new_settings)
        scenario_model.update(_scenario_key.id, **{ 'overwritable': False })[1]

def __current_proxy_settings(context: Context = None):
  if context and context.get('current_proxy_settings'):
    return context['current_proxy_settings']

  old_proxy_settings_raw = Settings.instance().read().get('proxy')
  return ProxySettings(old_proxy_settings_raw)

def __data_rule(proxy_settings: ProxySettings):
  project_key = proxy_settings.intercept.project_key
  
  _project_key = ProjectKey(project_key)
  return proxy_settings.data.data_rules(_project_key.id)

def __parse_scenario_key(scenario_key: str):
  try:
    return ScenarioKey(scenario_key)
  except Exception as e:
    return

def __project_key(proxy_settings: ProxySettings):
  return proxy_settings.intercept.project_key

def __scenario_key(proxy_settings: ProxySettings):
  data_rule = __data_rule(proxy_settings)
  return data_rule.scenario_key