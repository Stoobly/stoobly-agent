import pdb
import pytest

from stoobly_agent.app.cli.helpers.iterate_group_by import iterate_group_by
from stoobly_agent.app.cli.helpers.trace_context_facade import TraceContextFacade
from stoobly_agent.test.test_helper import reset

def iterate(settings, assign, group_by):
  trace_context = TraceContextFacade(settings).with_aliases(assign).trace_context

  iterations = []
  def handler(context):
    iterations.append({
      'trace_id': context.trace.id,
      'aliases': [(a.name, a.value, a.assigned_to) for a in context.trace.trace_aliases],
    })

  iterate_group_by(group_by, trace_context, handler)

  return trace_context, iterations

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
      _, iterations = iterate(settings, [':id=1', ':id=2'], ':id')

      for iteration in iterations:
        for _, _, assigned_to in iteration['aliases']:
          assert assigned_to is None
