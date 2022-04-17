import pdb
import requests
from stoobly_agent.config.constants import test_strategy

from stoobly_agent.app.models.request_model import RequestModel
from stoobly_agent.app.proxy.replay.replay_scenario_service import replay
from stoobly_agent.app.settings import Settings
from stoobly_agent.config.constants import mode
from stoobly_agent.lib.api.interfaces.scenarios import ScenarioShowResponse, ScenariosIndexResponse
from stoobly_agent.lib.api.keys import ProjectKey, ScenarioKey
from stoobly_agent.lib.api.scenarios_resource import ScenariosResource

class ScenarioFacade():

  def __init__(self, settings: Settings):
    self.settings = settings
    self.__api = ScenariosResource(self.settings.remote.api_url, self.settings.remote.api_key)

  def create(self, project_key: str, name: str, description: str = ''):
    res: requests.Response = self.__api.from_project_key(
      project_key, 
      lambda project_id: self.__api.create(
        project_id, {
          'description': description,
          'name': name,
        }
      )
    )

    if not res.ok:
      raise AssertionError('Could not create report')

    return res.json()

  def index(self, project_key, **kwargs) -> ScenariosIndexResponse:
    key = ProjectKey(project_key)
    res = self.__api.index(**{ 'project_id': key.id, **kwargs})
    return res.json()

  def show(self, scenario_key: str) -> ScenarioShowResponse:
    key = ScenarioKey(scenario_key)
    res = self.__api.show(key.id)
    return res.json()

  def replay(self, scenario_key: str, **kwargs):
    kwargs['mode'] = mode.NONE
    self.__replay(scenario_key, **kwargs)

  def test(self, scenario_key: str, **kwargs):
    kwargs['mode'] = mode.TEST
    kwargs['report_key'] = kwargs.get('save_to_report')
    kwargs['strategy'] = kwargs.get('strategy') or test_strategy.DIFF

    self.__replay(scenario_key, **kwargs)

  def __replay(self, scenario_key: str, **kwargs):
    kwargs['scenario_key'] = scenario_key

    replay(
      RequestModel(self.settings), **kwargs
    )

