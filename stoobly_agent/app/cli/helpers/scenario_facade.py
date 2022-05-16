import pdb
import requests

from stoobly_agent.config.constants import request_origin, test_strategy
from typing import Callable, TypedDict

from stoobly_agent.app.models.request_model import RequestModel
from stoobly_agent.app.proxy.replay.replay_scenario_service import replay
from stoobly_agent.app.settings import Settings
from stoobly_agent.config.constants import mode
from stoobly_agent.lib.api.interfaces.scenarios import ScenarioShowResponse, ScenariosIndexResponse
from stoobly_agent.lib.api.keys import ProjectKey, ScenarioKey
from stoobly_agent.lib.api.scenarios_resource import ScenariosResource

class ReplayOptions(TypedDict):
  on_response: Callable
  record: bool
  scenario_key: str

class TestOptions(TypedDict):
  on_response: Callable
  report_key: str
  strategy: str

class ScenarioFacade():

  def __init__(self, settings: Settings):
    self.__settings = settings
    self.__api = ScenariosResource(self.__settings.remote.api_url, self.__settings.remote.api_key)

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
      raise AssertionError(res.content)

    return res.json()

  def index(self, project_key, kwargs: dict) -> ScenariosIndexResponse:
    key = ProjectKey(project_key)
    res = self.__api.index(**{ 'project_id': key.id, **kwargs})

    if not res.ok:
      raise AssertionError(res.content)

    return res.json()

  def show(self, scenario_key: str) -> ScenarioShowResponse:
    key = ScenarioKey(scenario_key)
    res = self.__api.show(key.id)

    if not res.ok:
      raise AssertionError(res.content)

    return res.json()

  def replay(self, source_key: str, kwargs: ReplayOptions):
    scenario_key = None

    # Scenario key has no meaning if mode is replay
    # Only set scenario key if mode is record
    if kwargs.get('record'):
      scenario_key = kwargs.get('scenario_key')

    return replay(source_key, RequestModel(self.__settings), {
      'mode': mode.RECORD if kwargs.get('record') else mode.REPLAY,
      'on_response': kwargs.get('on_response'),
      'request_origin': request_origin.CLI,
      'scenario_key': scenario_key
    })

  def test(self, scenario_key: str, kwargs: TestOptions):
    strategy = kwargs.get('strategy')
    if not strategy:
        data_rule = self.__data_rules()
        strategy = data_rule.test_strategy

    return replay(scenario_key, RequestModel(self.__settings), {
      'mode': mode.TEST,
      'on_response': kwargs.get('on_response'),
      'report_key': kwargs.get('report_key'),
      'request_origin': request_origin.CLI,
      'scenario_key': scenario_key, # Mock the request from the specified scenario instead of active scenario
      'test_strategy': strategy or test_strategy.DIFF
    })

  def __data_rules(self):
    project_key = ProjectKey(self.__settings.proxy.intercept.project_key)
    return self.__settings.proxy.data.data_rules(project_key.id)