import pdb

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
  request_groups_with_alias_name = __group_by_alias_name(request_groups, alias_name) 

  for _trace_aliases in request_groups_with_alias_name:
    trace = Trace.create()
    trace_request = TraceRequest.create(trace_id=trace.id)

    for trace_alias in _trace_aliases:
      _trace_alias = trace_alias.replicate()
      _trace_alias.assigned_to = None
      _trace_alias.trace_id = trace.id
      _trace_alias.trace_request_id = trace_request.id
      _trace_alias.save()

    trace_context = TraceContext(trace_context.endpoints_resource, trace)

    handler(trace_context)

def __build_request_groups(trace_aliases: List[TraceAlias]):
  '''
  Returns { :traceRequestId => { :aliasName => [] } }
  '''
  request_groups = {}

  for trace_alias in trace_aliases:
    trace_request_id = trace_alias.trace_request_id
    if trace_request_id not in request_groups:
      request_groups[trace_request_id] = {}

    trace_alias_name = trace_alias.name
    request_group = request_groups[trace_request_id]
    if trace_alias_name not in request_group:
      request_group[trace_alias_name] = []
    
    request_group[trace_alias_name].append(trace_alias)

  return request_groups

def __group_by_alias_name(request_groups: dict, alias_name: str):
  '''
  Returns list of lists where each have at most one trace_alias with name == alias_name 
  '''
  request_groups_with_alias_name = []

  # request_groups e.g. 
  # {None: {':endpointId': [<stoobly_agent.lib.orm.trace_alias.TraceAlias object at 0x7f88eedeca90>, <stoobly_agent.lib.orm.trace_alias.TraceAlias object at 0x7f88eedec0a0>]}}
  for trace_request_id, request_group in request_groups.items():
    if alias_name not in request_group:
      continue
    
    # request_group[alias_name] e.g. 
    # [<stoobly_agent.lib.orm.trace_alias.TraceAlias object at 0x7f88eedeca90>, <stoobly_agent.lib.orm.trace_alias.TraceAlias object at 0x7f88eedec0a0>]
    for i, trace_alias in enumerate(request_group[alias_name]):
      group = [trace_alias]

      for _alias_name, trace_aliases in request_group.items():
        if len(trace_aliases) == 0:
          continue

        # We have already added a trace_alias.name == alias_name, skip it
        if _alias_name == alias_name:
          continue
        
        trace_alias = trace_aliases[i % len(trace_aliases)]

        group.append(trace_alias)
    
      request_groups_with_alias_name.append(group)

  return request_groups_with_alias_name