from typing import Callable, List

from stoobly_agent.app.proxy.replay.trace_context import TraceContext
from stoobly_agent.lib.orm.trace import Trace
from stoobly_agent.lib.orm.trace_alias import TraceAlias
from stoobly_agent.lib.orm.trace_request import TraceRequest

def iterate_group_by(alias_name: str, trace_context: TraceContext, handler: Callable[[TraceContext], None]):
  trace = trace_context.trace
  trace_aliases = trace.trace_aliases

  # Build map trace_request_id => trace_aliase with trace_request_id
  request_groups = __build_request_groups(trace_aliases)

  # Find all request groups that have alias name as one of the aliases
  request_groups_with_alias_name = __filter_by_alias_name(request_groups, alias_name) 

  for _trace_aliases in request_groups_with_alias_name:
    trace = Trace.create()
    trace_request = TraceRequest.create(trace_id=trace.id)

    for trace_alias in _trace_aliases:
      _trace_alias = trace_alias.replicate()
      _trace_alias.trace_id = trace.id
      _trace_alias.trace_request_id = trace_request.id
      _trace_alias.save()

    trace_context = TraceContext(trace_context.endpoints_resource, trace)
    handler(trace_context)

def __build_request_groups(trace_aliases: List[TraceAlias]):
  request_groups = {}

  for trace_alias in trace_aliases:
    trace_request_id = trace_alias.trace_request_id
    if trace_request_id not in request_groups:
      request_groups[trace_request_id] = []
    
    request_groups[trace_request_id].append(trace_alias)

    return request_groups

def __filter_by_alias_name(request_groups: dict, alias_name: str):
  request_groups_with_alias_name = []

  for trace_request_id, _trace_aliases in request_groups.items():
    for trace_alias in _trace_aliases:
      if trace_alias.name == alias_name: 
        request_groups_with_alias_name.append(_trace_aliases)

  return request_groups_with_alias_name