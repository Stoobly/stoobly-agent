import pdb

from stoobly_agent.app.cli.helpers.replay_facade import ReplayCliOptions, ReplayFacade, TestCliOptions
from stoobly_agent.app.models.request_model import RequestModel
from stoobly_agent.app.models.schemas.request import Request
from stoobly_agent.app.proxy.replay.context import ReplayContext
from stoobly_agent.app.proxy.replay.replay_request_service import ReplayRequestOptions, replay, replay_with_trace
from stoobly_agent.app.settings import Settings
from stoobly_agent.config.constants import mode
from stoobly_agent.lib.api.keys import ProjectKey, RequestKey
from stoobly_agent.lib.api.keys.scenario_key import ScenarioKey

class RequestFacade(ReplayFacade):

  def __init__(self, settings: Settings):
    self.__model = RequestModel(settings)

    super().__init__(settings)

  def show(self, request_key: str, cli_options: dict):
    key = RequestKey(request_key)

    return self.__model.show(key.id, **{ 
      'project_id': key.project_id, 
      **cli_options 
    })

  def index(self, project_key, cli_options: dict):
    query_params = { **cli_options }

    if project_key:
      key = ProjectKey(project_key)
      query_params['project_id'] = key.id

    if cli_options.get('scenario_key'):
      key = ScenarioKey(cli_options['scenario_key'])
      query_params['scenario_id'] = key.id
    
    return self.__model.index(**query_params)

  def replay(self, request_key: str, cli_options: ReplayCliOptions):
    scenario_key = None

    return self.__replay(request_key, {
      'mode': mode.RECORD if cli_options.get('record') else mode.REPLAY,
      'scenario_key': scenario_key,
      **self.common_replay_cli_options(cli_options)
    })

  def mock(self, request_key: str, cli_options: ReplayCliOptions):
    cli_options['mode'] = mode.MOCK
    return self.__replay(request_key, cli_options)

  def test(self, request_key: str, cli_options: TestCliOptions):
    return self.__replay(request_key, {
      'mode': mode.TEST,
      'report_key': cli_options.get('report_key'),
      'scenario_key': '', # When replaying a specific request, we don't want active scenario to be used
      **self.common_test_cli_options(cli_options)
    })

  def __replay(self, request_key: str, replay_options: ReplayRequestOptions):
    request_response = self.show(request_key, {
      'body': True,
      'headers': True,
      'query_params': True,
      'response': True,
    })
    context = ReplayContext(Request(request_response))

    if not replay_options.get('trace_context'):
      return replay(context, replay_options)
    else:
      return replay_with_trace(context, replay_options['trace_context'], replay_options)