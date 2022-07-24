import pdb

from typing import Callable, Dict, List, TypedDict, Union

from stoobly_agent.app.proxy.replay.alias_resolver import AliasResolver
from stoobly_agent.config.constants import alias_resolve_strategy
from stoobly_agent.lib.api.interfaces.endpoints import Alias, RequestComponentName
from stoobly_agent.lib.orm.trace_alias import TraceAlias
from stoobly_agent.lib.utils import jmespath

AliasMap = Dict[str, RequestComponentName]

class Options(TypedDict):
  handle_after_replace: Callable
  handle_replace: Callable

def __handle_after_replace(trace: TraceAlias, value):
  pass

def __handle_replace(replacement_options: list, number_of_replacements: int, strategy: alias_resolve_strategy.AliasResolveStrategy):
  if strategy == alias_resolve_strategy.NONE:
    return

  if strategy == alias_resolve_strategy.FIFO:
    index = number_of_replacements
    return -1 if index >= len(replacement_options) else index
  elif strategy == alias_resolve_strategy.LIFO:
    index = len(replacement_options) - number_of_replacements - 1
    return -1 if index < 0 else index

def build_id_to_alias_map(aliases: List[Alias]):
    id_to_alias = {}
    for _alias in aliases:
      id_to_alias[_alias['id']] = _alias
    return id_to_alias

def rewrite_params(
  params: Union[list, dict],
  param_names: List[RequestComponentName], 
  id_to_alias: AliasMap, 
  alias_resolver: AliasResolver,
  **options: Options
):
  for param_name in param_names:
    _alias: Alias = id_to_alias.get(param_name['alias_id'])
    if not _alias:
      continue

    current_value = jmespath.search(param_name.get('query') or param_name.get('name'), params)
    trace_aliases = alias_resolver.resolve_aliases(_alias['name'], current_value)

    if trace_aliases.is_empty():
      continue

    trace_aliases_list = []
    trace_aliases.each(lambda trace_alias: trace_aliases_list.append(trace_alias))
    trace_alias_values = list(map(lambda trace_alias: trace_alias.value, trace_aliases_list))
 
    handle_after_replace = options.get('handle_after_replace')
    handle_after_replace = handle_after_replace if handle_after_replace else __handle_after_replace

    # We have may have to first search for all values matching query,
    # If there's more than one, then try to assign different alias values 
    handle_replace = options.get('handle_replace')
    handle_replace = handle_replace if handle_replace else __handle_replace
    
    jmespath.search(
      param_name['query'], params, { 
        'replacements': trace_alias_values, 
        'handle_replace': lambda options, count: __handle_replace(options, count, alias_resolver.strategy),
        'handle_after_replace': lambda v, i: __handle_after_replace(trace_aliases_list[i], v)
      }
    )