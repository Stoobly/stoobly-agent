import pdb

from typing import Tuple

from stoobly_agent.app.models.types import ScenarioDestroyParams, ScenarioCreateParams
from stoobly_agent.lib.api.interfaces import ScenariosIndexQueryParams, ScenariosIndexResponse, ScenarioShowResponse
from stoobly_agent.lib.orm import ORM
from stoobly_agent.lib.orm.scenario import Scenario

from .helpers.search import search_scenario
from .helpers.snapshot_service import snapshot_scenario
from .local_db_adapter import LocalDBAdapter

class LocalDBScenarioAdapter(LocalDBAdapter):
  __scenario_orm = None

  def __init__(self, scenario_orm: Scenario.__class__ = Scenario):
    self.__scenario_orm = scenario_orm

  def create(self, **params: ScenarioCreateParams) -> Tuple[ScenarioShowResponse, int]:
    with ORM.instance().db.transaction():
      scenario_record = self.__scenario_orm.create(params)
      return self.success(scenario_record.to_dict())

  def show(self, scenario_id: str) -> Tuple[ScenarioShowResponse, int]:
    scenario_record = self.__scenario(scenario_id)
    if not scenario_record:
      return self.__scenario_not_found()
    return self.success(self.__to_show_response(scenario_record))

  def index(self, **query_params: ScenariosIndexQueryParams) -> Tuple[ScenariosIndexResponse, int]:
    page = int(query_params.get('page') or 0)
    query = query_params.get('q')
    size = int(query_params.get('size') or 20)
    sort_by = query_params.get('sort_by') or 'id'
    sort_order = query_params.get('sort_order') or 'desc'

    filter = query_params.get('filter')
    is_deleted = filter == 'is_deleted'

    scenarios = Scenario.where('is_deleted', is_deleted)

    if filter == 'starred':
      scenarios = scenarios.where('starred', True)
    elif filter == 'high_priority':
      scenarios = scenarios.where('priority', 3)
    elif filter == 'medium_priority':
      scenarios = scenarios.where('priority', 2)
    elif filter == 'low_priority':
      scenarios = scenarios.where('priority', 1)
    elif filter == 'none_priority':
      scenarios = scenarios.where('priority', 0)

    if query:
      scenarios = search_scenario(scenarios, query)

    total = scenarios.count()
    scenarios = scenarios.offset(page * size).limit(size).order_by(sort_by, sort_order).get()

    return self.success({
      'list': list(map(lambda scenario: self.__to_show_response(scenario), scenarios.items)),
      'total': total,
    })

  def update(self, scenario_id: int, **params: ScenarioCreateParams) -> Tuple[ScenarioShowResponse, int]:
    scenario = self.__scenario(scenario_id)

    if not scenario:
      return self.__scenario_not_found()

    if scenario.update(params):
      return self.success(self.__to_show_response(scenario))

    return self.internal_error('Could not update scenario')

  def destroy(self, scenario_id: int, **params: ScenarioDestroyParams) -> Tuple[ScenarioShowResponse, int]:
    scenario = self.__scenario(scenario_id)

    if not scenario:
      return self.__scenario_not_found()

    if params.get('force') or scenario.is_deleted:
      scenario.delete()
    else:
      scenario.update({'is_deleted': True})

    return self.success(self.__to_show_response(scenario))

  def snapshot(self, scenario_id: str, **params):
    scenario = self.__scenario(scenario_id)

    if not scenario:
      return self.__scenario_not_found()

    file_path = snapshot_scenario(scenario, **params)
    if not file_path:
      return self.internal_error()

    return self.success(file_path)

  def __scenario(self, scenario_id: str):
    if self.validate_uuid(scenario_id):
      return self.__scenario_orm.find_by(uuid=scenario_id)
    else:
      return self.__scenario_orm.find(scenario_id)

  def __to_show_response(self, scenario: Scenario) -> ScenarioShowResponse:
    res = scenario.to_dict()
    return res

  def __scenario_not_found(self):
    return self.not_found('Scenario not found')