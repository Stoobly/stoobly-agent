import pdb

from stoobly_agent.app.cli.helpers.replay_facade import ReplayCliOptions, ReplayFacade, TestCliOptions
from stoobly_agent.app.cli.helpers.iterate_group_by import iterate_group_by
from stoobly_agent.app.models.request_model import RequestModel
from stoobly_agent.app.models.schemas.request import Request
from stoobly_agent.app.cli.helpers.context import ReplayContext
from stoobly_agent.app.proxy.replay.replay_request_service import ReplayRequestOptions, replay, replay_with_trace
from stoobly_agent.app.proxy.replay.trace_context import TraceContext
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
    replay_context = self.__build_replay_context(request_key)
    replay_options = {
      'mode': mode.RECORD if cli_options.get('record') else mode.REPLAY,
      'scenario_key': '',
      **self.common_replay_cli_options(cli_options)
    }
    trace_context = replay_options.get('trace_context')

    return self.__replay(replay_context, trace_context, replay_options)

  def mock(self, request_key: str, cli_options: ReplayCliOptions):
    replay_context = self.__build_replay_context(request_key)
    cli_options['mode'] = mode.MOCK
    return self.__replay(replay_context, None, cli_options)

  def test(self, request_key: str, cli_options: TestCliOptions):
    replay_context = self.__build_replay_context(request_key)
    replay_options = {
      'mode': mode.TEST,
      'report_key': cli_options.get('report_key'),
      'scenario_key': '', # When replaying a specific request, we don't want active scenario to be used
      **self.common_test_cli_options(cli_options)
    }
    trace_context = replay_options.get('trace_context')

    return self.__replay(replay_context, trace_context, replay_options)

  def __build_replay_context(self, request_key: str):
    request_response = self.show(request_key, {
      'body': True,
      'headers': True,
      'query_params': True,
      'response': True,
    })
    return ReplayContext(Request(request_response))

  def __replay(self, replay_context: ReplayContext, trace_context: TraceContext, replay_options: ReplayRequestOptions):
    if not trace_context:
      return replay(replay_context, replay_options)

    group_by = replay_options.get('group_by')
    if not group_by:
      trace_context = replay_options['trace_context']
      return replay_with_trace(replay_context, trace_context, replay_options)
    else:
      return iterate_group_by(
        group_by, 
        trace_context,
        lambda trace_context: replay_with_trace(replay_context.clone(), trace_context, replay_options)
      )