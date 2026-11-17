import pdb
import pytest

from stoobly_agent.app.cli.helpers.iterate_group_by import iterate_group_by
from stoobly_agent.app.cli.helpers.replay_facade import ReplayFacade
from stoobly_agent.app.cli.helpers.trace_context_facade import TraceContextFacade
from stoobly_agent.lib.orm.trace import Trace
from stoobly_agent.lib.orm.trace_alias import TraceAlias
from stoobly_agent.lib.orm.trace_request import TraceRequest
from stoobly_agent.test.test_helper import reset

def iterate(settings, assign, group_by, trace=None, assigned_to=None):
  trace_context = TraceContextFacade(settings, trace).with_aliases(assign).trace_context

  if assigned_to is not None:
    for trace_alias in trace_context.trace.trace_aliases:
      trace_alias.assigned_to = assigned_to
      trace_alias.save()

  iterations = []
  def handler(context):
    iterations.append({
      'trace_id': context.trace.id,
      'aliases': [(a.name, a.value, a.assigned_to) for a in context.trace.trace_aliases],
    })

  iterate_group_by(group_by, trace_context, handler)

  return trace_context, iterations

def values_of(iteration, name):
  return [value for _name, value, _ in iteration['aliases'] if _name == name]

def pairs_of(iterations, name, other_name):
  return [(values_of(i, name)[0], values_of(i, other_name)[0]) for i in iterations]

class TestIterateGroupBy():

  @pytest.fixture(scope='class', autouse=True)
  @classmethod
  def settings(cls):
    return reset()

  class TestWhenSameAliasAssignedAndGroupedBy():

    def test_it_iterates_once_per_assigned_value(self, settings):
      _, iterations = iterate(settings, [':id=1', ':id=2'], ':id')

      assert len(iterations) == 2

    def test_it_has_one_value_for_alias_per_iteration(self, settings):
      _, iterations = iterate(settings, [':id=1', ':id=2'], ':id')

      for iteration in iterations:
        ids = [value for name, value, _ in iteration['aliases'] if name == ':id']
        assert len(ids) == 1

      values = {value for iteration in iterations for name, value, _ in iteration['aliases'] if name == ':id'}
      assert values == {1, 2}

  class TestWhenOtherAliasAssigned():

    def test_it_carries_other_alias_into_each_iteration(self, settings):
      _, iterations = iterate(settings, [':id=1', ':id=2', ":name='a'"], ':id')

      assert len(iterations) == 2
      for iteration in iterations:
        names = [value for name, value, _ in iteration['aliases'] if name == ':name']
        assert names == ['a']

  class TestWhenGroupByAliasNotAssigned():

    def test_it_does_not_iterate(self, settings):
      _, iterations = iterate(settings, [":name='a'"], ':id')

      assert len(iterations) == 0

  class TestIterationTrace():

    def test_it_uses_a_new_trace(self, settings):
      trace_context, iterations = iterate(settings, [':id=1', ':id=2'], ':id')

      trace_ids = {iteration['trace_id'] for iteration in iterations}
      assert len(trace_ids) == 2
      assert trace_context.trace.id not in trace_ids

    def test_it_clears_assigned_to(self, settings):
      _, iterations = iterate(settings, [':id=1', ':id=2'], ':id', assigned_to='previous')

      assert len(iterations) == 2
      for iteration in iterations:
        for _, _, assigned_to in iteration['aliases']:
          assert assigned_to is None

  class TestWhenOtherAliasHasFewerValues():

    def test_it_pairs_values_round_robin(self, settings):
      _, iterations = iterate(settings, [':id=1', ':id=2', ':id=3', ":name='a'", ":name='b'"], ':id')

      assert pairs_of(iterations, ':id', ':name') == [(1, 'a'), (2, 'b'), (3, 'a')]

    def test_it_pairs_values_when_other_alias_has_more_values(self, settings):
      _, iterations = iterate(settings, [':id=1', ':id=2', ":name='a'", ":name='b'", ":name='c'"], ':id')

      assert pairs_of(iterations, ':id', ':name') == [(1, 'a'), (2, 'b')]

  class TestWhenSameAliasAssignedTwice():

    def test_it_iterates_once(self, settings):
      _, iterations = iterate(settings, [':id=1', ':id=1'], ':id')

      assert len(iterations) == 1

  class TestWhenTraceHasRecordedRequestAliases():

    @pytest.fixture()
    def trace(self):
      trace = Trace.create()

      for value in [10, 20]:
        trace_request = TraceRequest.create(trace_id=trace.id)
        TraceAlias.create(name=':id', value=value, trace_id=trace.id, trace_request_id=trace_request.id)

      return trace

    def test_it_iterates_assigned_value_in_addition_to_recorded_values(self, settings, trace):
      _, iterations = iterate(settings, [':id=1'], ':id', trace=trace)

      assert sorted(values_of(i, ':id')[0] for i in iterations) == [1, 10, 20]

  class TestReplayFacade():

    def test_it_passes_assign_and_group_by_to_iterate_group_by(self, settings):
      options = ReplayFacade(settings).common_cli_options({
        'assign': [':id=1', ':id=2'],
        'group_by': ':id',
      })

      assert options['group_by'] == ':id'

      iterations = []
      iterate_group_by(options['group_by'], options['trace_context'], lambda context: iterations.append(context))

      assert len(iterations) == 2
