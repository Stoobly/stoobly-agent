import jmespath
import pdb

from requests import Response
from typing import Callable, List, Union

from stoobly_agent.app.models.schemas.request import Request
from stoobly_agent.app.proxy.replay.context import ReplayContext
from stoobly_agent.app.proxy.test.decode_response_service import decode_response
from stoobly_agent.lib.api.endpoints_resource import EndpointsResource
from stoobly_agent.lib.api.interfaces.endpoints import Alias, EndpointShowResponse, RequestComponentName, ResponseParamName
from stoobly_agent.lib.logger import Logger
from stoobly_agent.lib.orm.trace import Trace
from stoobly_agent.lib.orm.trace_alias import TraceAlias

class TraceContext:

  def __init__(self, endpoints_resource: EndpointsResource):
    self.__endpoints_resource = endpoints_resource

    self.__trace = Trace.create()
    Logger.instance().debug(f"Created Trace {self.__trace.id}")
    self.__requests: List[Request] = []

  def with_replay_context(self, context: ReplayContext, replay: Callable[[], Response]): 
    request = context.request
    endpoint = None

    if request.endpoint_id:
      endpoint = self.__get_endpoint(request.endpoint_id)
      Logger.instance().debug(f"\tMatched Endpoint: {endpoint}")

      self.__rewrite_request(request, endpoint)

    response = replay()

    if endpoint:
      self.__create_trace_aliases(response, endpoint)

    self.__requests.append((request, response))

  def __rewrite_request(self, request: Request, endpoint: EndpointShowResponse):
    if not endpoint:
      return

    id_to_alias = {}
    aliases = endpoint['aliases']
    for _alias in aliases:
      id_to_alias[_alias['id']] = _alias

    self.__rewrite_path(request, endpoint['path_segment_names'], id_to_alias) 
    self.__rewrite_query_params(request, endpoint['query_param_names'], id_to_alias)
    # TODO: rewrite body_params and headers

  def __rewrite_path(self, request: Request, path_segment_names: List[RequestComponentName], id_to_alias):
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
      trace_alias = self.__resolve_alias(_alias['name'], current_value)

      if not trace_alias:
        continue

      # Set path with alias value
      path_segment_strings[position] = trace_alias.value
    request.path = '/' + '/'.join(path_segment_strings)

  def __rewrite_query_params(self, request: Request, query_param_names: List[RequestComponentName], id_to_alias):
    query_params = request.query_params
    for query_param_name in query_param_names:
      _alias: Alias = id_to_alias.get(query_param_name['alias_id'])
      if not _alias:
        continue

      name = query_param_name['name']
      current_value = query_params.get(name)
      trace_alias = self.__resolve_alias(_alias['name'], current_value)

      if not trace_alias:
        continue
      
      query_params[name] = trace_alias.value
    request.query_params = query_params

  def __create_trace_aliases(self, response: Response, endpoint: EndpointShowResponse):
    content = decode_response(response.content, response.headers.get('content-type'))

    id_to_alias = {}
    aliases = endpoint['aliases']
    for _alias in aliases:
      id_to_alias[_alias['id']] = _alias

    response_param_names = endpoint['response_param_names']
    Logger.instance().debug(f"\tBuilding Trace Aliases from: {response_param_names}")

    for response_param_name in response_param_names:
      try:
        value = self.__query_resolves_response(response_param_name['query'], content)
        Logger.instance().debug(f"\tValue: {value}")
      except Exception as e:
        continue
        
      _alias: Alias = id_to_alias[response_param_name['alias_id']]
      Logger.instance().debug(f"\tAlias: {_alias}")

      if _alias and value:
        TraceAlias.create(
          name=_alias['name'],
          value=value,
          trace_id=self.__trace.id
        )

  def __resolve_alias(self, alias_name: str, value):
    trace_alias_hash = {
      'name': alias_name,
      'trace_id': self.__trace.id,
      'assigned_to': value
    }

    Logger.instance().debug(f"\tResolving Trace Alias: {trace_alias_hash}")

    trace_alias = TraceAlias.where(trace_alias_hash).get().first()

    if not trace_alias:
      trace_alias = TraceAlias.where({
        'name': alias_name,
        'trace_id': self.__trace.id,
      }).get().first()

      if not trace_alias:
        return

      trace_alias.assigned_to = value
      trace_alias.save()

    if trace_alias:
      Logger.instance().debug(f"\tResolved Trace Alias: {trace_alias.to_dict()}")

    return trace_alias

  def __query_resolves_response(self, query: str, response: Union[list, dict]):
    if not isinstance(response, dict) and not isinstance(response, list):
      raise

    expression = jmespath.compile(query)
    value = expression.search(response)

    if not isinstance(value, list):
      return value
    else:
      if len(value) == 0:
        raise
      
      return value[0]

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