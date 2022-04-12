import pdb
import requests
from stoobly_agent.config.constants import test_strategy

from stoobly_agent.lib.api.scenarios_resource import ScenariosResource
from stoobly_agent.app.models.request_model import RequestModel
from stoobly_agent.config.constants import mode
from stoobly_agent.app.proxy.replay.replay_scenario_service import replay
from stoobly_agent.app.settings import Settings

class ScenarioFacade():

  def __init__(self, settings: Settings):
    self.settings = settings

  def create(self, project_key: str, name: str, description: str = ''):
    api = ScenariosResource(self.settings.remote.api_url, self.settings.remote.api_key)

    res: requests.Response = api.from_project_key(
      project_key, 
      lambda project_id: api.create(
        project_id, {
          'description': description,
          'name': name,
        }
      )
    )

    if not res.ok:
      raise AssertionError('Could not create report')

    return res.json()

  def index(self, project_key, **kwargs):
    api = ScenariosResource(self.settings.remote.api_url, self.settings.remote.api_key)
    res = api.from_project_key(
      project_key, lambda project_id: api.index(project_id, kwargs)
    ) 
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

