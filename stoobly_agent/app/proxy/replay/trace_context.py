import pdb

from requests import Response
from typing import Callable, Dict, List, Union

from stoobly_agent.app.proxy.replay.alias_resolver import AliasResolver
from stoobly_agent.app.cli.helpers.tabulate_print_service import tabulate_print
from stoobly_agent.app.models.schemas.request import Request
from stoobly_agent.app.proxy.mock.search_endpoint import search_endpoint
from stoobly_agent.app.proxy.replay.body_parser_service import decode_response, is_traversable
from stoobly_agent.app.cli.helpers.context import ReplayContext
from stoobly_agent.app.proxy.replay.rewrite_params_service import build_id_to_alias_map, rewrite_params
from stoobly_agent.config.constants import alias_resolve_strategy, custom_headers
from stoobly_agent.lib.api.endpoints_resource import EndpointsResource
from stoobly_agent.lib.api.interfaces.endpoints import Alias, EndpointShowResponse, RequestComponentName, ResponseParamName
from stoobly_agent.lib.api.keys import ProjectKey
from stoobly_agent.lib.logger import bcolors, Logger
from stoobly_agent.lib.orm.trace import Trace
from stoobly_agent.lib.orm.trace_alias import TraceAlias
from stoobly_agent.lib.orm.trace_request import TraceRequest
from stoobly_agent.lib.utils import jmespath

AliasMap = Dict[str, RequestComponentName]
LOG_ID = 'Trace'

class TraceContext:

  def __init__(self, endpoints_resource: EndpointsResource, trace = None):
    self.__endpoints_resource = endpoints_resource
    self.__trace = trace or Trace.create()

    self.__alias_resolver = AliasResolver(self.__trace, alias_resolve_strategy.NONE)
    self.__requests: List[Request] = []
    self.__remote_project_key: ProjectKey = None

    Logger.instance(LOG_ID).debug(f"Using trace {self.__trace.id}")

  @property
  def alias_resolve_strategy(self):
    return self.__alias_resolver.strategy

  @alias_resolve_strategy.setter
  def alias_resolve_strategy(self, v):
    if v:
      self.__alias_resolver.strategy = v

  @property
  def trace(self):
    return self.__trace

  @property
  def endpoints_resource(self):
    return self.__endpoints_resource

  def with_remote_project(self, key: str):
    if key:
      self.__remote_project_key = ProjectKey(key)

  def with_replay_context(self, context: ReplayContext, replay: Callable[[], Response]): 
    request = context.request
    endpoint = None

    if request.endpoint_id:
      endpoint = self.__get_endpoint(request.endpoint_id)
    elif self.__remote_project_key:
      endpoint = search_endpoint(
        self.endpoints_resource, 
        self.__remote_project_key.id,
        request.method,
        request.url,
        **self.__endpoint_query_params(),
      )

    if endpoint:
      Logger.instance(LOG_ID).debug(f"\tMatched Endpoint: {endpoint}")

      if self.alias_resolve_strategy != alias_resolve_strategy.NONE:
        self.rewrite_request(request, endpoint)

    trace_request = TraceRequest.create(trace_id=self.__trace.id)

    # Set trace id for request
    headers = request.headers
    headers[custom_headers.TRACE_ID] = str(self.trace.id)
    headers[custom_headers.TRACE_REQUEST_ID] = str(trace_request.id)
    request.headers = headers

    # Replay request
    response = replay(context)

    if endpoint:
      self.__create_trace_aliases(trace_request, response, endpoint)

    self.__requests.append((request, response))

  def create_trace_alias(self, alias_name, value, trace_request = None):
    return self.__alias_resolver.create_alias(alias_name, value, trace_request)

  def rewrite_request(self, request: Request, endpoint: EndpointShowResponse):
    if not endpoint:
      return

    id_to_alias = build_id_to_alias_map(endpoint['aliases'])

    self.__rewrite_path(request, endpoint['path_segment_names'], id_to_alias) 
    self.__rewrite_headers(request, endpoint['header_names'], id_to_alias)
    self.__rewrite_query_params(request, endpoint['query_param_names'], id_to_alias)
    self.__rewrite_body_params(request, endpoint['body_param_names'], id_to_alias)

  def __rewrite_path(
    self, request: Request, path_segment_names: List[RequestComponentName], id_to_alias: AliasMap
  ):
    path_segment_strings = request.path_segment_strings
    for path_segment_name in path_segment_names:
      position = path_segment_name.get('position') 

      if position == None:
        continue

      if position > len(path_segment_strings):
        continue

      _alias: Alias = id_to_alias.get(path_segment_name['alias_id'])
      if not _alias:
        continue

      current_value = path_segment_strings[position]
      trace_alias = self.__resolve_and_assign_alias(_alias['name'], current_value)
      if not trace_alias:
        continue

      path_segment_strings[position] = str(trace_alias.value)

    request.path = '/' + '/'.join(path_segment_strings)

  def __rewrite_handler(self, component_type: str, alias_name: str, name: str, value):
    Logger.instance(LOG_ID).info(f"{bcolors.OKCYAN}Rewriting{bcolors.ENDC} {component_type} alias {alias_name} {name} => {value}")

  def __rewrite_headers(
    self, request: Request, header_names: List[RequestComponentName], id_to_alias: AliasMap
  ):
    headers = request.headers
    rewrite_handler = lambda alias_name, name, value: self.__rewrite_handler('header', alias_name, name, value)
    self.__rewrite_components(headers, header_names, id_to_alias, rewrite_handler)
    request.headers = headers

  def __rewrite_query_params(
    self, request: Request, query_param_names: List[RequestComponentName], id_to_alias: AliasMap
  ):
    query_params = request.query_params
    rewrite_handler = lambda alias_name, name, value: self.__rewrite_handler('query param', alias_name, name, value)
    self.__rewrite_components(query_params, query_param_names, id_to_alias, rewrite_handler)
    request.query_params = query_params

  def __rewrite_body_params(
    self, request: Request, body_param_names: List[RequestComponentName], id_to_alias: AliasMap
  ):
    body_params = request.body_params

    if is_traversable(body_params):
      rewrite_params(
        body_params, 
        body_param_names, 
        id_to_alias, 
        self.__alias_resolver,
        handle_after_replace=self.__rewrite_body_params_handler
      )

      request.body_params = body_params

  def __rewrite_body_params_handler(self, name, value, trace_alias: TraceAlias):
    self.__rewrite_handler('body param', trace_alias.name, name, value)
    return self.__alias_resolver.assign_alias(trace_alias, value)

  # Query params and headers
  def __rewrite_components(self, components, component_names, id_to_alias: AliasMap, rewrite_handler):
    delimitter = ',' # Comma is reserved for both query params and headers

    visited = {}
    for component_name in component_names:
      _alias: Alias = id_to_alias.get(component_name['alias_id'])
      if not _alias:
        continue
      
      # Query params and headers can have multiple values, process just once
      name = component_name['name']
      if name in visited:
        continue
      else:
        visited[name] = True

      if name not in components:
        continue

      current_values = components.get_all(name)
      joined_value = delimitter.join(current_values)
      trace_alias = self.__resolve_and_assign_alias(_alias['name'], joined_value)

      if not trace_alias:
        continue

      # Remove all values for the key, name
      components.pop(name)

      # Update with new values
      alias_value = str(trace_alias.value)
      new_values = alias_value.split(delimitter)
      for new_value in new_values:
        components.add(name, new_value)

        if rewrite_handler:
          rewrite_handler(_alias['name'], name, new_value)

  def __create_trace_aliases(self, trace_request: TraceRequest, response: Response, endpoint: EndpointShowResponse):
    '''
    1. Parse all aliased properties from response
    2. Create TraceAlias records for each parsed aliased propert
    '''
    content = decode_response(response.content, response.headers.get('content-type'))
    if not is_traversable(content):
        return Logger.instance(LOG_ID).debug('Skipping creating aliases, content is not traversable')

    id_to_alias = {}
    aliases = endpoint['aliases']
    for _alias in aliases:
      id_to_alias[_alias['id']] = _alias

    response_param_names = endpoint['response_param_names']
    Logger.instance(LOG_ID).debug(f"\tBuilding Trace Aliases from: {response_param_names}")

    for response_param_name in response_param_names:
      try:
        values = self.__query_resolves_response(response_param_name, content)
        Logger.instance(LOG_ID).debug(f"\tValues: {values}")
      except Exception as e:
        Logger.instance(LOG_ID).error(e)
        continue

      _alias: Alias = id_to_alias[response_param_name['alias_id']]
      Logger.instance(LOG_ID).debug(f"\tAlias: {_alias}")

      for value in values:  
        if _alias and value:
          self.__alias_resolver.create_alias(_alias['name'], value, trace_request) 

  def __resolve_and_assign_alias(self, alias_name: str, value) -> Union[TraceAlias, None]:
    trace_alias = self.__alias_resolver.resolve_alias(alias_name, value)

    if trace_alias:
      self.__alias_resolver.assign_alias(trace_alias, value)

      return trace_alias

  def __query_resolves_response(self, response_param_name: ResponseParamName, response: Union[list, dict]) -> list:
    '''
    Return value in response specified by query
    '''

    query = response_param_name['query']
    expression = jmespath.compile(query)
    value = expression.search(response)

    return jmespath.flatten(value, query)

  def __get_endpoint(self, endpoint_id: int) -> Union[EndpointShowResponse, None]:
    res = self.__endpoints_resource.show(
      endpoint_id,
      **self.__endpoint_query_params()
    )

    if res.ok:
      return res.json()

  def __endpoint_query_params(self):
    return {
      'aliases': True,
      'filter': 'alias_id',
      'path_segment_names': True,
      'query_param_names': True,
      'header_names': True,
      'body_param_names': True,
      'response_param_names': True
    }

  def __dump_trace_aliases(self):
    aliases = self.__trace.trace_aliases()

    data = []
    for _alias in aliases:
      data.append({
        'assigned_to': _alias.assigned_to,
        'name': _alias.name,
        'value': _alias.value,
      })

    tabulate_print(data, print_handler=Logger.instance(LOG_ID).debug)
