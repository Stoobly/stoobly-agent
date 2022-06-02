import pdb
import requests

from stoobly_agent.app.cli.helpers.replay_facade import ReplayCliOptions, ReplayFacade, TestCliOptions
from stoobly_agent.app.proxy.replay.replay_scenario_service import inject_replay
from stoobly_agent.app.settings import Settings
from stoobly_agent.config.constants import mode
from stoobly_agent.lib.api.interfaces.scenarios import ScenarioShowResponse, ScenariosIndexResponse
from stoobly_agent.lib.api.keys import ProjectKey, ScenarioKey
from stoobly_agent.lib.api.scenarios_resource import ScenariosResource

class ScenarioFacade(ReplayFacade):

  def __init__(self, settings: Settings):
    self.__api = ScenariosResource(settings.remote.api_url, settings.remote.api_key)
    super().__init__(settings)

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

  def index(self, project_key, cli_options: dict) -> ScenariosIndexResponse:
    key = ProjectKey(project_key)
    res = self.__api.index(**{ 'project_id': key.id, **cli_options})

    if not res.ok:
      raise AssertionError(res.content)

    return res.json()

  def show(self, scenario_key: str) -> ScenarioShowResponse:
    key = ScenarioKey(scenario_key)
    res = self.__api.show(key.id)

    if not res.ok:
      raise AssertionError(res.content)

    return res.json()

  def replay(self, source_key: str, cli_options: ReplayCliOptions):
    return self.__replay(source_key, {
      'mode': mode.RECORD if cli_options.get('record') else mode.REPLAY,
      **self.common_replay_cli_options(cli_options)
    })

  def test(self, scenario_key: str, cli_options: TestCliOptions):
    return self.__replay(scenario_key, {
      'mode': mode.TEST,
      'report_key': cli_options.get('report_key'),
      'scenario_key': scenario_key, # Mock the request from the specified scenario instead of active scenario
      **self.common_test_cli_options(cli_options)
    })

  def __replay(self, scenario_key, replay_options):
    replay = inject_replay()
    replay(scenario_key, replay_options)