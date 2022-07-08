import pdb
from typing import List

from stoobly_agent.app.proxy.replay.rewrite_params_service import build_id_to_alias_map
from stoobly_agent.config.constants import test_filter
from stoobly_agent.lib.api.interfaces.endpoints import Alias, ResponseParamName
from stoobly_agent.lib.orm.trace import Trace
from stoobly_agent.lib.orm.trace_alias import TraceAlias

class ResponseParamNamesFacade():

  def __init__(self, response_param_names_response):
    self.__response_param_names = response_param_names_response

    self.__aliased_response_param_names = None
    self.__deterministic_response_param_names = None
    self.__required_response_param_names = None

    self.__filter: test_filter.TestFilter = test_filter.ALL
    self.__trace: Trace = None

    self.__response_param_name_map = {}
    for response_param_name in self.__response_param_names:
      if not response_param_name.get('query'):
        continue

      self.__response_param_name_map[response_param_name['query']] = response_param_name

    self.__id_to_alias_map = {}

  @property
  def aliased(self) -> List[ResponseParamName]: 
    if not self.__aliased_response_param_names:
      filter_handler = lambda param_name: param_name.get('alias_id') != None
      self.__aliased_response_param_names = list(filter(filter_handler, self.__response_param_names))

    return self.__aliased_response_param_names

  @property
  def all(self) -> List[ResponseParamName]:
    return self.__response_param_names

  @property
  def deterministic(self) -> List[ResponseParamName]:
    if not self.__deterministic_response_param_names:
      filter_handler = lambda param_name: (not not param_name.get('is_deterministic') )
      self.__deterministic_response_param_names = list(filter(filter_handler, self.__response_param_names))

    return self.__deterministic_response_param_names

  @property
  def required(self) -> List[ResponseParamName]: 
    if not self.__required_response_param_names:
      filter_handler = lambda param_name: (not not param_name.get('is_required'))
      self.__required_response_param_names = list(filter(filter_handler, self.__response_param_names))

    return self.__required_response_param_names

  def is_selected(self, query: str) -> bool:
    if self.__filter == test_filter.ALL:
      return True
    elif self.__filter == test_filter.ALIAS:
      return self.__select_alias(query)
    elif self.__filter == test_filter.LINK:
      return self.__select_link(query)
    else:
      return False

  def with_aliases(self, aliases: List[Alias]):
    self.__id_to_alias_map = build_id_to_alias_map(aliases)
    return self

  def with_filter(self, filter: test_filter.TestFilter):
    self.__filter = filter
    return self

  def with_trace(self, trace: Trace):
    self.__trace = trace
    return self
    
  def __select_alias(self, query: str):
    _response_param_name = self.__response_param_name_map.get(query)
    if not _response_param_name:
      return False

    # If aliased, then filter
    return not not _response_param_name.get('alias_id')

  def __select_link(self, query: str):
    if not self.__trace:
      return True

    _response_param_name: ResponseParamName = self.__response_param_name_map.get(query)
    if not _response_param_name:
      return False

    alias_id = _response_param_name.get('alias_id')
    if not alias_id:
      return False

    _alias: Alias = self.__id_to_alias_map.get(alias_id)
    
    if not _alias:
      return False

    alias_name = _alias['name']
    trace_aliases = TraceAlias.where({
      'name': alias_name,
      'trace_id': self.__trace.id,
    })

    return trace_aliases.count() > 0