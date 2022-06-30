from typing import Callable, List, TypedDict

from stoobly_agent.app.cli.helpers.trace_context_facade import TraceContextFacade
from stoobly_agent.app.proxy.replay.trace_context import TraceContext
from stoobly_agent.app.settings import Settings
from stoobly_agent.config.constants import request_origin, test_strategy
from stoobly_agent.lib.api.keys.project_key import ProjectKey
from stoobly_agent.lib.orm.trace import Trace

class ReplayCliOptions(TypedDict):
  assign: List[str]
  group_by: str
  on_response: Callable
  record: bool
  scenario_key: str
  trace: Trace

class TestCliOptions(ReplayCliOptions):
  report_key: str
  strategy: str

class ReplayFacade():

  def __init__(self, settings: Settings):
    self.__settings = settings

  def common_cli_options(self, cli_options: ReplayCliOptions) -> ReplayCliOptions:
    assign = cli_options.get('assign')
    trace_context = None
    trace_id = cli_options.get('trace_id')

    # If a trace_id is given, use it to find a trace
    trace = Trace.find_by(id=trace_id) if trace_id else None 
    if trace or assign:
      facade = TraceContextFacade(self.__settings, trace)

      # If assign is given, create default TraceAliases for the trace 
      if assign:
        facade.with_aliases(assign)

      trace_context = facade.trace_context

    return {
      'group_by': cli_options.get('group_by'),
      'on_response': cli_options.get('on_response'),
      'request_origin': request_origin.CLI,
      'trace_context': trace_context,
    }

  def common_replay_cli_options(self, cli_options: ReplayCliOptions) -> ReplayCliOptions:
    common_cli_options = self.common_cli_options(cli_options)

    # Scenario key has no meaning if mode is replay
    # Only set scenario key if mode is record
    if cli_options.get('record'):
      scenario_key = cli_options.get('scenario_key')
      if not scenario_key:
        data_rules = self.data_rules()
        common_cli_options['scenario_key'] = data_rules.scenario_key
      else:
        common_cli_options['scenario_key'] = scenario_key
    
    return common_cli_options

  def common_test_cli_options(self, cli_options: TestCliOptions) -> TestCliOptions:
    strategy = cli_options.get('strategy')
    if not strategy:
        data_rule = self.data_rules()
        strategy = data_rule.test_strategy

    return {
      'test_strategy': strategy or test_strategy.DIFF,
      **self.common_cli_options(cli_options)
    }

  def data_rules(self):
    project_key = ProjectKey(self.__settings.proxy.intercept.project_key)
    return self.__settings.proxy.data.data_rules(project_key.id)