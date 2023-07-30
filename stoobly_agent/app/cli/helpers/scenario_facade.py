import pdb

from stoobly_agent.app.cli.helpers.iterate_group_by import iterate_group_by
from stoobly_agent.app.cli.helpers.replay_facade import ReplayCliOptions, ReplayFacade, TestCliOptions
from stoobly_agent.app.models.scenario_model import ScenarioModel
from stoobly_agent.app.proxy.replay.replay_scenario_service import inject_replay
from stoobly_agent.app.proxy.replay.trace_context import TraceContext
from stoobly_agent.app.settings import Settings
from stoobly_agent.config.constants import mode
from stoobly_agent.lib.api.keys import ProjectKey, ScenarioKey

class ScenarioFacade(ReplayFacade):

  def __init__(self, settings: Settings):
    super().__init__(settings)
    self.__model = ScenarioModel(settings)

  def create(self, project_key: str, name: str, description: str = ''):
    key = ProjectKey(project_key)
    return self.__model.create(**{
      'project_id': key.id, 
      'description': description,
      'name': name,
    })

  def index(self, project_key, cli_options: dict):
    key = ProjectKey(project_key)
    return self.__model.index(**{ 'project_id': key.id, **cli_options})

  def show(self, scenario_key: str):
    key = ScenarioKey(scenario_key)
    return self.__model.show(key.id)

  def replay(self, source_key: str, cli_options: ReplayCliOptions):
    return self.__replay(source_key, {
      'mode': mode.RECORD if cli_options.get('record') else mode.REPLAY,
      **self.common_replay_cli_options(cli_options),
      **self.__common_replay_options(source_key),
    })

  def snapshot(self, scenario_key: str, cli_options: dict):
    key = ScenarioKey(scenario_key)

    return self.__model.snapshot(key.id, **cli_options)

  def test(self, scenario_key: str, cli_options: TestCliOptions):
    return self.__replay(scenario_key, {
      'mode': mode.TEST,
      'report_key': cli_options.get('report_key'),
      'scenario_key': scenario_key, # Mock the request from the specified scenario instead of active scenario
      **self.common_test_cli_options(cli_options),
      **self.__common_replay_options(scenario_key),
    })

  def delete(self, scenario_key: str):
    key = ScenarioKey(scenario_key)

    return self.__model.destroy(key.id)

  def __common_replay_options(self, scenario_key: str):
    return {
      'project_key': ProjectKey.encode(ScenarioKey(scenario_key).project_id),
    }

  def __replay(self, scenario_key: str, replay_options: ReplayCliOptions):
    trace_context = replay_options['trace_context']
    group_by = replay_options['group_by']

    if not group_by or not trace_context:
      replay = inject_replay()
      return replay(scenario_key, replay_options)
    else:
      return iterate_group_by(
        group_by, 
        trace_context,
        lambda trace_context: self.__replay_with_trace_context(trace_context, scenario_key, replay_options)
      )

  def __replay_with_trace_context(self, trace_context: TraceContext, scenario_key: str, replay_options: ReplayCliOptions):
    _replay_options = replay_options.copy()
    _replay_options['trace_context'] = trace_context
    replay = inject_replay()
    return replay(scenario_key, _replay_options)
