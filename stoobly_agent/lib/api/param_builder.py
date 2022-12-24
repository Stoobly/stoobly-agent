import pdb

from stoobly_agent.app.proxy.intercept_settings import InterceptSettings
from stoobly_agent.lib.api.keys.project_key import ProjectKey
from stoobly_agent.lib.api.keys.scenario_key import ScenarioKey

class ParamBuilder():
  def __init__(self, initial_params = {}):
    self.__params = initial_params

  def with_resource_scoping(self, _project_key: str, _scenario_key: str = None):
    # Try to see if a scenario is set, otherwise use project
    if _scenario_key and len(_scenario_key) > 0:
        scenario_key = ScenarioKey(_scenario_key)
        self.__params['scenario_id'] = scenario_key.id
        self.__params['project_id'] = scenario_key.project_id
    elif _project_key and len(_project_key) > 0:
        project_key = ProjectKey(_project_key)
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