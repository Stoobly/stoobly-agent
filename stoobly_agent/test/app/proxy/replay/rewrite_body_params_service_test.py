import pdb
from typing import List
import pytest

from stoobly_agent.test import test_helper

from stoobly_agent.app.proxy.replay.rewrite_params_service import rewrite_params
from stoobly_agent.lib.orm.trace import Trace
from stoobly_agent.lib.orm.trace_alias import TraceAlias

@pytest.fixture
def trace():
  return Trace.create()

class Test():

  def test_rewrites_dict(self, trace):
    response = {
      'id': 1,
    }

    response_param_names = [
      {
        'alias_id': 1,
        'name': 'id',
        'query': 'id',
      }
    ]

    id_to_alias = {
      1: {
        'name': ':requestId',
      }
    } 

    # Create trace alias
    resolved_alias_values = [1000]
    self.build_trace_aliases(trace, id_to_alias.values(), resolved_alias_values)

    rewrite_params(response, response_param_names, id_to_alias, trace, self.handle_after_replace)

    expected_id = resolved_alias_values[0]
    assert response['id'] == expected_id, test_helper.value_not_match_error(response['id'], expected_id)

  def test_rewrites_list_of_dicts(self, trace):
    response = [{
      'id': 1,
    }]

    response_param_names = [
      {
        'alias_id': 1,
        'name': 'id',
        'query': '[*].id',
      }
    ]

    id_to_alias = {
      1: {
        'name': ':requestId',
      }
    } 

    # Create trace alias
    resolved_alias_values = [1000]
    self.build_trace_aliases(trace, id_to_alias.values(), resolved_alias_values)

    rewrite_params(response, response_param_names, id_to_alias, trace, self.handle_after_replace)

    expected_id = resolved_alias_values[0]
    assert response[0]['id'] == expected_id, test_helper.value_not_match_error(response['id'], expected_id)

  def build_trace_aliases(self, trace: Trace, aliases: List[TraceAlias], values: list):
    for i, _alias in enumerate(aliases):
      TraceAlias.create(name=_alias['name'], trace_id=trace.id, value=values[i])

  def handle_after_replace(self, trace_alias: TraceAlias, value):
    pass
