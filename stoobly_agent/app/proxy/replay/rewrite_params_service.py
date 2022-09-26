import pdb

from typing import Callable, Dict, List, TypedDict, Union

from stoobly_agent.app.proxy.replay.alias_context import AliasContext
from stoobly_agent.app.proxy.replay.alias_resolver import AliasResolver
from stoobly_agent.config.constants import alias_resolve_strategy
from stoobly_agent.lib.api.interfaces.endpoints import Alias, RequestComponentName
from stoobly_agent.lib.orm.trace_alias import TraceAlias
from stoobly_agent.lib.utils import jmespath

AliasMap = Dict[str, RequestComponentName]

def __handle_after_replace(name, value, trace_alias: TraceAlias):
  pass

def __handle_replace(name, value, alias_context: AliasContext):
  trace_alias = alias_context.resolve_alias(name, value)

  if not trace_alias:
    raise ValueError('Alias not set')
  else:
    return trace_alias.value

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
  **options: jmespath.Options
) -> None:
  # If no resolve strategy is set, return
  if alias_resolver.strategy == alias_resolve_strategy.NONE:
    return

  for param_name in param_names:
    alias_context = AliasContext(alias_resolver)
    _alias: Alias = id_to_alias.get(param_name['alias_id'])

    if not _alias:
      continue
 
    handle_after_replace = options.get('handle_after_replace')
    handle_after_replace = handle_after_replace if handle_after_replace else __handle_after_replace

    # We have may have to first search for all values matching query,
    # If there's more than one, then try to assign different alias values 
    handle_replace = options.get('handle_replace')
    handle_replace = handle_replace if handle_replace else __handle_replace

    jmespath.search(
      param_name['query'], params, { 
        'handle_replace': lambda name, value, i: handle_replace(_alias['name'], value, alias_context),
        'handle_after_replace': lambda name, value, i: handle_after_replace(name, value, alias_context.resolved_aliases[i])
      }
    )