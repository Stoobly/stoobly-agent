import pdb
from stoobly_agent.config.constants import test_origin, test_strategy

from stoobly_agent.app.models.request_model import RequestModel
from stoobly_agent.app.models.schemas.request import Request
from stoobly_agent.app.proxy.replay.replay_request_service import replay
from stoobly_agent.app.settings import Settings
from stoobly_agent.lib.api.keys import ProjectKey, RequestKey
from stoobly_agent.lib.api.keys import InvalidProjectKey
from stoobly_agent.config.constants import mode
from stoobly_agent.lib.api.keys.scenario_key import ScenarioKey

class RequestFacade():

  def __init__(self, settings: Settings):
    self.__settings = settings
    self.__model = RequestModel(settings)

  def show(self, request_key: str, kwargs: dict):
    key = RequestKey(request_key)

    return self.__model.show(key.id, **{ 
      'project_id': key.project_id, 
      **kwargs 
    })

  def index(self, project_key, kwargs: dict):
    query_params = { **kwargs }

    if project_key:
      key = ProjectKey(project_key)
      query_params['project_id'] = key.id

    if kwargs.get('scenario_key'):
      key = ScenarioKey(kwargs['scenario_key'])
      query_params['scenario_id'] = key.id
    
    return self.__model.index(**query_params)

  def replay(self, request_key: str, kwargs: dict):
    scenario_key = None

    # Scenario key has no meaning if mode is replay
    # Only set scenario key if mode is record
    if kwargs.get('record'):
      scenario_key = kwargs.get('scenario_key')
      if not scenario_key:
        data_rules = self.__data_rules()
        scenario_key = data_rules.scenario_key

    return self.__replay(request_key, {
      'mode': mode.RECORD if kwargs.get('record') else mode.REPLAY,
      'scenario_key': scenario_key 
    })

  def mock(self, request_key: str, kwargs: dict):
    kwargs['mode'] = mode.MOCK
    return self.__replay(request_key, kwargs)

  def test(self, request_key: str, kwargs: dict):
    strategy = kwargs.get('strategy')
    if not strategy:
        data_rule = self.__data_rules()
        strategy = data_rule.test_strategy

    return self.__replay(request_key, {
      'mode': mode.TEST,
      'report_key': kwargs.get('report_key'),
      'test_origin': test_origin.CLI,
      'test_strategy': strategy or test_strategy.DIFF
    })

  def __replay(self, request_key: str, kwargs: dict):
    request = self.show(request_key, {
      'body': True,
      'headers': True,
      'query_params': True,
      'response': True,
    })
    return replay(Request(request), kwargs)

  def __data_rules(self):
    project_key = ProjectKey(self.__settings.proxy.intercept.project_key)
    return self.__settings.proxy.data.data_rules(project_key.id)