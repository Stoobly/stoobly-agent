import pdb

from stoobly_agent.lib.settings import Settings
from stoobly_agent.lib.api.requests_resource import RequestsResource
from stoobly_agent.lib.intercept_handler.constants import modes, test_strategies
from stoobly_agent.lib.intercept_handler.replay.replay_scenario_service import replay

class Scenario():

  def __init__(self, settings: Settings, scenario_key: str):
    self.settings = settings
    self.scenario_key = scenario_key

  def replay(self, **kwargs):
    kwargs['mode'] = modes.NONE
    self.__replay(**kwargs)

  def test(self, **kwargs):
    kwargs['mode'] = modes.TEST
    kwargs['report_key'] = kwargs.get('report_key')
    kwargs['strategy'] = kwargs.get('strategy') or test_strategies.DIFF

    self.__replay(**kwargs)

  def __replay(self, **kwargs):
    kwargs['scenario_key'] = self.scenario_key

    replay(
      RequestsResource(self.settings.api_url, self.settings.api_key), **kwargs
    )

