import pdb

from typing import Tuple

from stoobly_agent.app.models.types import ScenarioCreateParams
from stoobly_agent.lib.api.scenarios_resource import ScenariosResource
from stoobly_agent.lib.api.interfaces.scenarios import ScenarioShowResponse, ScenariosIndexResponse

class StooblyScenarioAdapter():

  def __init__(self, __api: ScenariosResource):
    self.__api = __api

  def create(self, **params: ScenarioCreateParams) -> Tuple[ScenarioShowResponse, int]:
    res = self.__api.create(**params)
    res.raise_for_status()  
    return res.json(), res.status_code

  def show(self, scenario_id: str) -> Tuple[ScenarioShowResponse, int]:
    res = self.__api.show(scenario_id)
    res.raise_for_status()  
    return res.json(), res.status_code

  def index(self, **query_params) -> Tuple[ScenariosIndexResponse, int]:
    res = self.__api.index(**query_params)
    res.raise_for_status()  
    return res.json(), res.status_code

  def update(self, scenario_id: str, **params):
    res = self.__api.update(scenario_id, **params)
    res.raise_for_status()  
    return res.json(), res.status_code