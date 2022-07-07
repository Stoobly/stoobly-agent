from typing import Collection

from stoobly_agent.config.constants import alias_resolve_strategy
from stoobly_agent.lib.logger import Logger
from stoobly_agent.lib.orm.trace import Trace
from stoobly_agent.lib.orm.trace_alias import TraceAlias

class AliasResolver():

  def __init__(self, trace: Trace, strategy: alias_resolve_strategy.AliasResolveStrategy):
    self.__trace = trace
    self.__strategy  = strategy

  @property
  def strategy(self):
    return self.__strategy

  @strategy.setter
  def strategy(self, v: alias_resolve_strategy.AliasResolveStrategy):
    self.__strategy = v

  def resolve_alias(self, alias_name: str, value: str):
    strategy = self.__strategy

    if strategy == alias_resolve_strategy.NONE:
      return

    trace_aliases = self.resolve_aliases(alias_name, value)
    if trace_aliases.is_empty():
      return
      
    if strategy == alias_resolve_strategy.LIFO:
      return trace_aliases.pop()
    elif strategy == alias_resolve_strategy.FIFO:
      return trace_aliases.shift()

  def resolve_aliases(self, alias_name: str, value: str) -> Collection:
    '''
    Return TraceAlias collection based on alias_name and value
    '''
    trace = self.__trace

    trace_alias_hash = {
      'assigned_to': str(value) if isinstance(value, list) or isinstance(value, dict) else value,
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