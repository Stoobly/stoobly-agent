import pdb
from typing import Collection

from stoobly_agent.config.constants import alias_resolve_strategy
from stoobly_agent.lib.logger import Logger, bcolors
from stoobly_agent.lib.orm.trace import Trace
from stoobly_agent.lib.orm.trace_alias import TraceAlias

LOG_ID = 'Alias'

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

  def assign_alias(self, trace_alias: TraceAlias, value):
    if not trace_alias:
      return
      
    if trace_alias.assigned_to == None:
      trace_alias.assigned_to = value
      trace_alias.save()

      Logger.instance(LOG_ID).info(f"{bcolors.OKBLUE}Assigned{bcolors.ENDC} {trace_alias.name}: {value} -> {trace_alias.value}")

  def resolve_alias(self, alias_name: str, value: str):
    trace_alias = self.__resolve_alias(alias_name, value)
    return trace_alias

  def create_alias(self, alias_name, value, trace_request = None):
    columns = {
      'name': alias_name,
      'value': self.__serialize(value),
      'trace_id': self.__trace.id,
    }

    trace_alias = TraceAlias.find_by(**columns)
    if trace_alias:
      return trace_alias

    trace_alias = TraceAlias.create(**{
      **columns,
      'trace_request_id': trace_request.id if trace_request else None
    })

    if trace_alias:
      Logger.instance(LOG_ID).info(f"{bcolors.OKGREEN}Created{bcolors.ENDC} alias {trace_alias.name}: {value}")

    return trace_alias

  def __resolve_alias(self, alias_name: str, value: str):
    strategy = self.__strategy

    if strategy == alias_resolve_strategy.NONE:
      return

    trace_aliases = self.__resolve_aliases(alias_name, value)
    if trace_aliases.is_empty():
      return
      
    if strategy == alias_resolve_strategy.LIFO:
      return trace_aliases.pop()
    elif strategy == alias_resolve_strategy.FIFO:
      return trace_aliases.shift()

  def __resolve_aliases(self, alias_name: str, value: str) -> Collection:
    '''
    Return TraceAlias collection based on alias_name and value
    '''
    trace_aliases = self.__assigned_aliases(alias_name, value)

    if trace_aliases.is_empty():
      trace_aliases = self.__available_aliases(alias_name)

    return trace_aliases

  def __assigned_aliases(self, alias_name: str, value: str) -> Collection:
    trace = self.__trace

    trace_alias_hash = {
      'assigned_to': self.__serialize(value),
      'name': alias_name,
      'trace_id': trace.id,
    }

    trace_aliases = TraceAlias.where(trace_alias_hash).get()

    if not trace_aliases.is_empty():
      self.__log_resolved_aliases(trace_aliases)

    return trace_aliases

  def __available_aliases(self, alias_name: str) -> Collection:
    trace = self.__trace

    trace_aliases = TraceAlias.where({
      'name': alias_name,
      'trace_id': trace.id,
    }).where_null('assigned_to').get()

    if not trace_aliases.is_empty():
      self.__log_resolved_aliases(trace_aliases)

    return trace_aliases

  def __serialize(self, value):
    return str(value) if isinstance(value, list) or isinstance(value, dict) else value

  def __log_resolved_aliases(self, trace_aliases):
    trace_aliases.each(lambda trace_alias: Logger.instance(LOG_ID).debug(f"\tResolved Trace Alias: {trace_alias.to_dict()}"))