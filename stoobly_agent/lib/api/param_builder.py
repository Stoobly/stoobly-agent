from stoobly_agent.lib.api.keys.project_key import ProjectKey
from stoobly_agent.lib.api.keys.scenario_key import ScenarioKey
from stoobly_agent.app.settings.types import IProjectModeSettings

class ParamBuilder():
  def __init__(self, initial_params = {}):
    self.__params = initial_params

  def with_resource_scoping(self, active_mode_settings):
    # Try to see if a scenario is set, otherwise use project
    scenario_key = ScenarioKey(active_mode_settings.get('scenario_key'))
    if scenario_key:
        self.__params['scenario_id'] = scenario_key.id
        self.__params['project_id'] = scenario_key.project_id
    else:
        project_key = ProjectKey(active_mode_settings.get('project_key'))
        self.__params['project_id'] = project_key.id

    return self

  def with_params(self, params):
    self.__params = { **self.__params, **params }
    return self

  def with_param(self, key, val):
    self.__params[key] = val
    return self

  def build(self) -> dict:
    return self.__params