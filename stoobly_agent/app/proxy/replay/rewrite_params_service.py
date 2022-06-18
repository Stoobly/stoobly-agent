import pdb
import jmespath

from .visitor import TreeInterpreter, Visitor

# Monkey patch jmespath with replacement functionality
jmespath.parser.visitor.Vistor = Visitor
jmespath.parser.visitor.TreeInterpreter = TreeInterpreter

from typing import Callable, Dict, List, Union
from orator.orm.collection import Collection

from stoobly_agent.app.models.schemas.request import Request
from stoobly_agent.lib.api.interfaces.endpoints import Alias, EndpointShowResponse, RequestComponentName
from stoobly_agent.lib.logger import Logger
from stoobly_agent.lib.orm.trace import Trace
from stoobly_agent.lib.orm.trace_alias import TraceAlias

AliasMap = Dict[str, RequestComponentName]

def __handle_after_replace(trace_alias: TraceAlias, value):
  pass

def build_id_to_alias_map(aliases):
    id_to_alias = {}
    for _alias in aliases:
      id_to_alias[_alias['id']] = _alias
    return id_to_alias

def rewrite_params(
  params: Union[list, dict],
  param_names: List[RequestComponentName], 
  id_to_alias: AliasMap, 
  trace: Trace,
  handle_after_replace: Callable = __handle_after_replace 
):
  for param_name in param_names:
    _alias: Alias = id_to_alias.get(param_name['alias_id'])
    if not _alias:
      continue

    current_value = jmespath.search(param_name.get('query') or param_name.get('name'), params)
    trace_aliases = resolve_alias(trace, _alias['name'], current_value)

    if trace_aliases.is_empty():
      continue

    trace_aliases_list = []
    trace_aliases.each(lambda trace_alias: trace_aliases_list.append(trace_alias))
    trace_alias_values = list(map(lambda trace_alias: trace_alias.value, trace_aliases_list))

    # We have may have to first search for all values matching query,
    # If there's more than one, then try to assign different alias values  
    handler = handle_after_replace if handle_after_replace else __handle_after_replace
    jmespath.search(
      param_name['query'], params, { 
        'replacements': trace_alias_values, 
        'handle_after_replace': lambda v, i: handler(trace_aliases_list[i], v)
      }
    )

def resolve_alias(trace: Trace, alias_name: str, value: str) -> Collection:
  '''
  Return TraceAlias collection based on alias_name and value
  '''

  trace_alias_hash = {
    'assigned_to': value,
    'name': alias_name,
    'trace_id': trace.id,
  }

  Logger.instance().debug(f"\tResolving Trace Alias: {trace_alias_hash}")

  trace_aliases = TraceAlias.where(trace_alias_hash).get()

  if trace_aliases.is_empty():
    trace_aliases = TraceAlias.where({
      'name': alias_name,
      'trace_id': trace.id,
    }).where_null('assigned_to').get()

  if not trace_aliases.is_empty():
    trace_aliases.each(lambda trace_alias: Logger.instance().debug(f"\tResolved Trace Alias: {trace_alias.to_dict()}"))

  return trace_aliases