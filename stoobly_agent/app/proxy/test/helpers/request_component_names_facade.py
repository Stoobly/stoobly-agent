import pdb
import re
from typing import List

from mitmproxy.coretypes.multidict import MultiDict
from requests import request

from stoobly_agent.app.proxy.replay.rewrite_params_service import build_id_to_alias_map
from stoobly_agent.config.constants import test_filter
from stoobly_agent.lib.api.interfaces.endpoints import Alias, RequestComponentName
from stoobly_agent.lib.orm.trace import Trace
from stoobly_agent.lib.orm.trace_alias import TraceAlias

class RequestComponentNamesFacade():

  def __init__(self, request_component_names_response):
    self.__request_component_names: List[RequestComponentName] = request_component_names_response

    self.__aliased_request_component_names = None
    self.__deterministic_request_component_names = None
    self.__required_request_component_names = None

    self.__filter: test_filter.TestFilter = test_filter.ALL
    self.__trace: Trace = None

    self.__request_component_name_map = {}
    for request_component_name in self.__request_component_names:
      if not request_component_name.get('query'):
        continue

      self.__request_component_name_map[request_component_name['query']] = request_component_name

    self.__id_to_alias_map = {}

    # Cache
    self.__edges_index_cache = None
    self.__query_index_cache = None

  @property
  def query_index(self):
    if self.__query_index_cache:
      return self.__query_index_cache

    _index = MultiDict()

    for request_component_name in self.__request_component_names:
      query = request_component_name.get('query')
      if not query:
        query = request_component_name.get('name')

      _index.add(query, request_component_name)

    self.__query_index_cache = _index

    return _index

  @property
  def edges_index(self):
    if self.__edges_index_cache:
      return self.__edges_index_cache

    _index = {}

    for request_component_name in self.__request_component_names:
      # TODO: make this less hacky, right now only response_param_names and body_param_names have children though
      parent_id = request_component_name.get('response_param_name_id')
      if not parent_id:
        parent_id = request_component_name.get('body_param_name_id')

      if parent_id not in _index:
        _index[parent_id] = []

      _index[parent_id].append(request_component_name)

    self.__edges_index_cache = _index 

    return _index

  @property
  def aliased(self) -> List[RequestComponentName]: 
    if not self.__aliased_request_component_names:
      filter_handler = lambda param_name: param_name.get('alias_id') != None
      self.__aliased_request_component_names = list(filter(filter_handler, self.__request_component_names))

    return self.__aliased_request_component_names

  @property
  def all(self) -> List[RequestComponentName]:
    return self.__request_component_names

  @property
  def deterministic(self) -> List[RequestComponentName]:
    if not self.__deterministic_request_component_names:
      filter_handler = lambda param_name: (not not param_name.get('is_deterministic') )
      self.__deterministic_request_component_names = list(filter(filter_handler, self.__request_component_names))

    return self.__deterministic_request_component_names

  @property
  def required(self) -> List[RequestComponentName]: 
    if not self.__required_request_component_names:
      filter_handler = lambda param_name: (not not param_name.get('is_required'))
      self.__required_request_component_names = list(filter(filter_handler, self.__request_component_names))

    return self.__required_request_component_names

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
    _request_component_name = self.__request_component_name_map.get(query)
    if not _request_component_name:
      return False

    # If aliased, then filter
    return not not _request_component_name.get('alias_id')

  def __select_link(self, query: str):
    if not self.__trace:
      return True

    _request_component_name: RequestComponentName = self.__request_component_name_map.get(query)
    if not _request_component_name:
      return False

    alias_id = _request_component_name.get('alias_id')
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