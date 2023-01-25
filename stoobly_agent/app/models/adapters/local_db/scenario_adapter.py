import pdb

from stoobly_agent.app.models.adapters.types.scenario_create_params import ScenarioCreateParams
from stoobly_agent.lib.api.interfaces import ScenariosIndexQueryParams, ScenariosIndexResponse, ScenarioShowResponse
from stoobly_agent.lib.api.keys.scenario_key import ScenarioKey
from stoobly_agent.lib.orm import ORM
from stoobly_agent.lib.orm.scenario import Scenario

from ..types import ScenarioCreateParams

class LocalDBScenarioAdapter():
  __scenario_orm = None

  def __init__(self, scenario_orm: Scenario.__class__ = Scenario):
    self.__scenario_orm = scenario_orm

  def create(self, **params: ScenarioCreateParams) -> ScenarioShowResponse:
    with ORM.instance().db.transaction():
      scenario_record = self.__scenario_orm.create(params)
      return scenario_record.to_dict()

  def show(self, scenario_id: str) -> ScenarioShowResponse:
    scenario_record = self.__scenario_orm.find(scenario_id)
    return self.__to_show_response(scenario_record)

  def index(self, **query_params: ScenariosIndexQueryParams) -> ScenariosIndexResponse:
    page = int(query_params.get('page') or 0)
    query = query_params.get('q')
    size = int(query_params.get('size') or 20)
    sort_by = query_params.get('sort_by') or 'id'
    sort_order = query_params.get('sort_order') or 'desc'

    is_deleted = query_params.get('filter') == 'is_deleted'
    starred = query_params.get('filter') == 'starred'

    scenarios = Scenario.where('is_deleted', is_deleted)

    if starred:
      scenarios = scenarios.where('starred', starred)

    if query:
      scenarios = self.__search(scenarios, query)

    total = scenarios.count()
    scenarios = scenarios.offset(page * size).limit(size).order_by(sort_by, sort_order).get()

    return {
      'list': list(map(lambda scenario: self.__to_show_response(scenario), scenarios.items)),
      'total': total,
    }

  def update(self, scenario_id: int, **params: ScenarioCreateParams) -> ScenarioShowResponse:
    scenario = Scenario.find(scenario_id)

    if not scenario:
      return

    if scenario.update(params):
      return self.__to_show_response(scenario)

  def destroy(self, scenario_id: int) -> ScenarioShowResponse:
    scenario = Scenario.find(scenario_id)

    if not scenario:
      return

    if scenario.is_deleted:
      scenario.delete()
    else:
      scenario.update({'is_deleted': True})

    return self.__to_show_response(scenario)

  def __search(self, base_model: Scenario, query: str) -> Scenario:
    return base_model.where('name', 'like', f"%{query}%")

  def __to_show_response(self, scenario: Scenario) -> ScenarioShowResponse:
    res = scenario.to_dict()
    return res