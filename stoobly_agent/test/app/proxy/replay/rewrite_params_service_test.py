import pdb
import pytest

from typing import List

from stoobly_agent.app.proxy.replay.alias_resolver import AliasResolver
from stoobly_agent.app.proxy.replay.rewrite_params_service import rewrite_params
from stoobly_agent.config.constants import alias_resolve_strategy
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

    alias_resolver = AliasResolver(trace, alias_resolve_strategy.LIFO)
    rewrite_params(response, response_param_names, id_to_alias, alias_resolver)

    expected_id = resolved_alias_values[0]
    assert response['id'] == expected_id, self.value_not_match_error(response['id'], expected_id)

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

    alias_resolver = AliasResolver(trace, alias_resolve_strategy.LIFO)
    rewrite_params(response, response_param_names, id_to_alias, alias_resolver)

    expected_id = resolved_alias_values[0]
    assert response[0]['id'] == expected_id, self.value_not_match_error(response['id'], expected_id)

  def test_rewrites_dict_of_list_of_dicts_of_dicts(self, trace):
    response = {'list': [{'id': 910, 'service_id': 26, 'name': 'users', 'position': 0, 'created_at': '2022-10-03T00:59:15.172Z', 'updated_at': '2022-10-03T00:59:15.172Z'}, {'id': 911, 'service_id': 26, 'name': ':userId2', 'position': 1, 'created_at': '2022-10-03T00:59:15.404Z', 'updated_at': '2022-10-03T00:59:20.238Z', 'alias_name': ':userId2', 'alias': {'id': 144, 'name': ':userId2', 'created_at': '2022-07-28T08:16:59.599Z', 'updated_at': '2022-08-22T08:47:54.567Z', 'project_id': 38, 'path_segment_names_count': -1, 'header_names_count': 0, 'query_param_names_count': 0, 'body_param_names_count': 0, 'response_param_names_count': 0, 'service_id': 26}}], 'total': 2}
    response_param_names = [{'id': 23993, 'alias_id': 152, 'endpoint_id': 1477, 'response_param_name_id': 23991, 'name': 'id', 'query': 'list[*].alias.id', 'inferred_type': 'Integer', 'response_param_names_count': 0, 'is_required': True, 'created_at': '2022-08-25T06:53:31.663Z', 'updated_at': '2022-08-25T06:54:51.936Z', 'requests_count': 4, 'is_deterministic': False}]
    id_to_alias = {152: {'id': 152, 'name': ':aliasId'}}

    resolved_alias_values = [144]
    self.build_trace_aliases(trace, id_to_alias.values(), resolved_alias_values)

    alias_resolver = AliasResolver(trace, alias_resolve_strategy.LIFO)
    rewrite_params(response, response_param_names, id_to_alias, alias_resolver)

    expected_id = resolved_alias_values[0]
    assert response['list'][1]['alias']['id'] == expected_id, self.value_not_match_error(response['id'], expected_id)

  def build_trace_aliases(self, trace: Trace, aliases: List[TraceAlias], values: list):
    for i, _alias in enumerate(aliases):
      TraceAlias.create(name=_alias['name'], trace_id=trace.id, value=values[i])

  def value_not_match_error(self, v1, v2):
    return f"Got {v1}, expected {v2}"