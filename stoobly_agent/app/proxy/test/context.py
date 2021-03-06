import pdb

from mitmproxy.http import Request
from typing import Union
from stoobly_agent.app.cli.helpers.context import ReplayContext

from stoobly_agent.app.proxy.mock.context import MockContext
from stoobly_agent.app.proxy.replay.alias_resolver import AliasResolver
from stoobly_agent.app.proxy.replay.body_parser_service import encode_response, is_traversable
from stoobly_agent.app.proxy.replay.rewrite_params_service import build_id_to_alias_map, rewrite_params
from stoobly_agent.app.proxy.test.mitmproxy_response_adapter import MitmproxyResponseAdapter
from stoobly_agent.app.proxy.test.requests_response_adapter import RequestsResponseAdapter
from stoobly_agent.app.proxy.test.response_param_names_facade import ResponseParamNamesFacade

from stoobly_agent.config.constants import custom_headers
from stoobly_agent.lib.api.endpoints_resource import EndpointsResource
from stoobly_agent.lib.api.interfaces.endpoints import EndpointShowResponse
from stoobly_agent.lib.orm.trace import Trace

from .context_response import TestContextResponse

class TestContext():
  def __init__(self, replay_context: ReplayContext, mock_context: MockContext):
    self.__flow = mock_context.flow
    self.__intercept_settings = mock_context.intercept_settings
    self.__mock_context = mock_context

    mock_response = self.__mock_context.response
    self.__expected_response = RequestsResponseAdapter(mock_response).adapt()

    upstream_response = self.__flow.response
    self.__response = MitmproxyResponseAdapter(upstream_response).adapt()

    self.__endpoint_show_response = None
    self.__log = ''
    self.__passed = None
    self.__response_param_names = None
    self.__skipped = False

    self.__cached_rewritten_expected_response_content = None

  def with_response_param_names(self, resource: EndpointsResource):
    endpoint_id = self.mock_request_endpoint_id

    if not resource or not endpoint_id:
      return 

    try:
      res = resource.show(endpoint_id, aliases=True, response_param_names=True)
    except Exception as e:
      return 

    if not res.ok:
      return 

    self.__endpoint_show_response: EndpointShowResponse = res.json()
    aliases = self.__endpoint_show_response['aliases']
    response_param_names = self.__endpoint_show_response['response_param_names']

    self.__response_param_names = ResponseParamNamesFacade(
      response_param_names      
    ).with_aliases(aliases).with_filter(self.filter).with_trace(self.trace)

  @property
  def cached_expected_response_content(self) -> Union[bytes, None, str]:
    if not self.__cached_rewritten_expected_response_content:
      return None

    return encode_response(self.__cached_rewritten_expected_response_content, self.__expected_response.content_type) 

  @property
  def lifecycle_hooks(self):
    return self.__intercept_settings.lifecycle_hooks

  @property
  def lifecycle_hooks_script_path(self):
    return self.__intercept_settings.lifecycle_hooks_script_path

  @property
  def end_time(self):
    return self.__flow.response.timestamp_end

  @property
  def expected_response(self) -> TestContextResponse:
    return self.__expected_response

  @property
  def decoded_expected_response_content(self):
    return self.__expected_response.decode_content()

  @property
  def filter(self):
    return self.intercept_settings.test_filter

  @property
  def flow(self):
    return self.__flow

  @property
  def intercept_settings(self):
    return self.__intercept_settings

  @property
  def log(self):
    return self.__log

  @log.setter
  def log(self, v: str):
    self.__log = v

  @property
  def mock_request_id(self) -> Union[str, None]:
    return self.expected_response.headers.get(custom_headers.MOCK_REQUEST_ID)

  @property
  def mock_request_endpoint_id(self) -> Union[str, None]:
    return self.expected_response.headers.get(custom_headers.MOCK_REQUEST_ENDPOINT_ID)

  @property
  def passed(self):
    return self.__passed

  @passed.setter
  def passed(self, v):
    self.__passed = v

  @property
  def request(self) -> Request:
    return self.__flow.request

  @property
  def response(self) -> TestContextResponse:
    return self.__response

  @property
  def response_param_names(self) -> ResponseParamNamesFacade:
    return self.__response_param_names

  @property
  def rewritten_expected_response_content(self):
    _decoded_expected_response_content = self.decoded_expected_response_content
    
    trace = self.trace
    if not trace:
      return _decoded_expected_response_content

    if not is_traversable(_decoded_expected_response_content):
      return _decoded_expected_response_content

    if not self.response_param_names:
      return _decoded_expected_response_content

    aliased_response_param_names = self.response_param_names.aliased
    aliases = self.__endpoint_show_response.get('aliases') or []

    if len(aliased_response_param_names) == 0 or len(aliases) == 0:
      return _decoded_expected_response_content

    id_to_alias_map = build_id_to_alias_map(aliases)
    alias_resolver = AliasResolver(trace, self.intercept_settings.alias_resolve_strategy)
    rewrite_params(_decoded_expected_response_content, aliased_response_param_names, id_to_alias_map, alias_resolver)

    self.__cached_rewritten_expected_response_content = _decoded_expected_response_content

    return _decoded_expected_response_content

  @property
  def skipped(self):
    return self.__skipped

  @skipped.setter
  def skipped(self, v: bool):
    self.skipped = v

  @property
  def start_time(self):
    return self.request.timestamp_start

  @property
  def strategy(self):
    return self.intercept_settings.test_strategy

  @property
  def trace(self) -> Union[Trace, None]:
    headers = self.request.headers
    trace_id = headers.get(custom_headers.TRACE_ID)

    if not trace_id:
      return

    return Trace.find(trace_id)