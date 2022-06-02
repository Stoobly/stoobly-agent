import jmespath

from .visitor import TreeInterpreter, Visitor

# Monkey patch jmespath with replacement functionality
jmespath.parser.visitor.Vistor = Visitor
jmespath.parser.visitor.TreeInterpreter = TreeInterpreter

import pdb

from requests import Response
from typing import Callable, Dict, List, Union
from orator.orm.collection import Collection

from stoobly_agent.app.cli.helpers.tabulate_print_service import tabulate_print
from stoobly_agent.app.models.schemas.request import Request
from stoobly_agent.app.proxy.replay.context import ReplayContext
from stoobly_agent.app.proxy.replay.body_parser_service import decode_response
from stoobly_agent.lib.api.endpoints_resource import EndpointsResource
from stoobly_agent.lib.api.interfaces.endpoints import Alias, EndpointShowResponse, RequestComponentName, ResponseParamName
from stoobly_agent.lib.logger import Logger, bcolors
from stoobly_agent.lib.orm.trace import Trace
from stoobly_agent.lib.orm.trace_alias import TraceAlias

AliasMap = Dict[str, RequestComponentName]

class TraceContext:

  def __init__(self, endpoints_resource: EndpointsResource, trace = Trace.create()):
    self.__endpoints_resource = endpoints_resource

    self.__trace = trace
    Logger.instance().debug(f"Using trace {self.__trace.id}")

    self.__requests: List[Request] = []

  @property
  def trace(self):
    return self.__trace

  def with_replay_context(self, context: ReplayContext, replay: Callable[[], Response]): 
    request = context.request
    endpoint = None

    if request.endpoint_id:
      endpoint = self.__get_endpoint(request.endpoint_id)

      if endpoint:
        Logger.instance().debug(f"\tMatched Endpoint: {endpoint}")

        self.__rewrite_request(request, endpoint)

    response = replay(context)

    if endpoint:
      self.__create_trace_aliases(response, endpoint)

    self.__requests.append((request, response))

  def create_trace_alias(self, alias_name, value):
    trace_alias = TraceAlias.create(
      name=alias_name,
      value=value,
      trace_id=self.__trace.id
    )
    Logger.instance().info(f"{bcolors.OKGREEN}Resolved {trace_alias.name}: {value}{bcolors.ENDC}")
    return trace_alias

  def __rewrite_request(self, request: Request, endpoint: EndpointShowResponse):
    if not endpoint:
      return

    id_to_alias = {}
    aliases = endpoint['aliases']
    for _alias in aliases:
      id_to_alias[_alias['id']] = _alias

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

      path_segment_strings[position] = trace_alias.value

    request.path = '/' + '/'.join(path_segment_strings)

  def __rewrite_headers(
    self, request: Request, header_names: List[RequestComponentName], id_to_alias: AliasMap
  ):
    headers = request.headers
    self.__rewrite_components(headers, header_names, id_to_alias)
    request.headers = headers

  def __rewrite_query_params(
    self, request: Request, query_param_names: List[RequestComponentName], id_to_alias: AliasMap
  ):
    query_params = request.query_params
    self.__rewrite_components(query_params, query_param_names, id_to_alias)
    request.query_params = query_params

  def __rewrite_body_params(
    self, request: Request, body_param_names: List[RequestComponentName], id_to_alias: AliasMap
  ):
    body_params = request.body_params
    for body_param_name in body_param_names:
      _alias: Alias = id_to_alias.get(body_param_name['alias_id'])
      if not _alias:
        continue

      name = body_param_name['name']
      current_value = body_params.get(name) 
      trace_aliases = self.__resolve_alias(_alias['name'], current_value)

      if trace_aliases.is_empty():
        continue

      trace_aliases_list = []
      trace_aliases.each(lambda trace_alias: trace_aliases_list.append(trace_alias))
      trace_alias_values = list(map(lambda trace_alias: trace_alias.value, trace_aliases_list))

      # We have may have to first search for all values matching query,
      # If there's more than one, then try to assign different alias values  
      jmespath.search(
        body_param_name['query'], body_params, { 
          'replacements': trace_alias_values, 
          'handle_after_replace': lambda v, i: self.__assign_trace_alias(trace_aliases_list[i], v)
        }
      )

    request.body_params = body_params

  def __rewrite_components(self, components, component_names, id_to_alias: AliasMap):
    visited = {}
    for component_name in component_names:
      _alias: Alias = id_to_alias.get(component_name['alias_id'])
      if not _alias:
        continue

      name = component_name['name']
      if name in visited:
        continue
      else:
        visited[name] = True

      new_values = []
      current_values = components.get_all(name)
      if len(current_values) == 0:
        trace_aliases = self.__resolve_alias(_alias['name'], None)
        if trace_aliases.is_empty():
          continue

        trace_alias = trace_aliases.pop()
        new_values.append(trace_alias.value)
      else:
        # Remove all values for the key, name
        components.pop(name)

        for current_value in current_values:
          new_values.append(current_value)
          trace_alias = self.__resolve_and_assign_alias(_alias['name'], current_value)

          if not trace_alias:
            continue
          
          # An alias is found, use alias value instead of current_value
          new_values.pop()
          new_values.append(trace_alias.value)

      for new_value in new_values:
        components.add(name, new_value)

  def __create_trace_aliases(self, response: Response, endpoint: EndpointShowResponse):
    '''
    1. Parse all aliased properties from response
    2. Create TraceAlias records for each parsed aliased propert
    '''
    content = decode_response(response.content, response.headers.get('content-type'))

    id_to_alias = {}
    aliases = endpoint['aliases']
    for _alias in aliases:
      id_to_alias[_alias['id']] = _alias

    response_param_names = endpoint['response_param_names']
    Logger.instance().debug(f"\tBuilding Trace Aliases from: {response_param_names}")

    for response_param_name in response_param_names:
      try:
        values = self.__query_resolves_response(response_param_name['query'], content)
        Logger.instance().debug(f"\tValues: {values}")
      except Exception as e:
        Logger.instance().error(e)
        continue

      _alias: Alias = id_to_alias[response_param_name['alias_id']]
      Logger.instance().debug(f"\tAlias: {_alias}")

      for value in values:  
        if _alias and value:
          self.create_trace_alias(_alias['name'], value) 

  def __resolve_and_assign_alias(self, alias_name: str, value: list) -> Union[TraceAlias, None]:
    trace_aliases = self.__resolve_alias(alias_name, value)
    if trace_aliases.is_empty():
      return
      
    trace_alias = trace_aliases.pop()
    self.__assign_trace_alias(trace_alias, value)

    return trace_alias

  def __assign_trace_alias(self, trace_alias: TraceAlias, value):
    if not trace_alias.assigned_to:
      trace_alias.assigned_to = value
      trace_alias.save()

      Logger.instance().info(f"{bcolors.OKBLUE}Assigned {trace_alias.name}: {value} -> {trace_alias.value}{bcolors.ENDC}")

  def __resolve_alias(self, alias_name: str, value: str) -> Collection:
    '''
    Return TraceAlias collection based on alias_name and value
    '''

    trace_alias_hash = {
      'assigned_to': value,
      'name': alias_name,
      'trace_id': self.__trace.id,
    }

    Logger.instance().debug(f"\tResolving Trace Alias: {trace_alias_hash}")

    trace_aliases = TraceAlias.where(trace_alias_hash).get()

    if trace_aliases.is_empty():
      trace_aliases = TraceAlias.where({
        'name': alias_name,
        'trace_id': self.__trace.id,
      }).where_null('assigned_to').get()

    if not trace_aliases.is_empty():
      trace_aliases.each(lambda trace_alias: Logger.instance().debug(f"\tResolved Trace Alias: {trace_alias.to_dict()}"))

    return trace_aliases

  def __query_resolves_response(self, query: str, response: Union[list, dict]) -> list:
    '''
    Return value in response specified by query
    '''
    if not isinstance(response, dict) and not isinstance(response, list):
      raise

    expression = jmespath.compile(query)
    value = expression.search(response)

    while isinstance(value, list):
      if len(value) == 0:
        raise

      if len(value) == 1:
        value = value[0]

      break

    return value if isinstance(value, list) else [value]

  def __get_endpoint(self, endpoint_id: int) -> Union[EndpointShowResponse, None]:
    res = self.__endpoints_resource.show(endpoint_id,
      aliases=True,
      path_segment_names=True,
      query_param_names=True,
      header_names=True,
      body_param_names=True,
      response_param_names=True
    )

    if res.ok:
      return res.json()

  def __dump_trace_aliases(self):
    aliases = self.__trace.trace_aliases()

    data = []
    for _alias in aliases:
      data.append({
        'assigned_to': _alias.assigned_to,
        'name': _alias.name,
        'value': _alias.value,
      })

    tabulate_print(data, print_handler=Logger.instance().debug)