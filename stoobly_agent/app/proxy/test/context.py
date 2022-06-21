import pdb

from mitmproxy.http import HTTPFlow, Request
from typing import Union

from stoobly_agent.app.proxy.mock.context import MockContext
from stoobly_agent.app.proxy.replay.rewrite_params_service import build_id_to_alias_map, rewrite_params
from stoobly_agent.app.proxy.test.mitmproxy_response_adapter import MitmproxyResponseAdapter
from stoobly_agent.app.proxy.test.requests_response_adapter import RequestsResponseAdapter
from stoobly_agent.app.proxy.test.response_param_names_facade import ResponseParamNamesFacade

from stoobly_agent.config.constants import custom_headers, test_strategy
from stoobly_agent.lib.api.endpoints_resource import EndpointsResource
from stoobly_agent.lib.api.interfaces.endpoints import EndpointShowResponse
from stoobly_agent.lib.orm.trace import Trace

from .context_response import TestContextResponse

class TestContext():
  def __init__(self, mock_context: MockContext):
    self.__flow = mock_context.flow
    self.__mock_context = mock_context
    self.__strategy = test_strategy.DIFF

    mock_response = self.__mock_context.response
    self.__expected_response = RequestsResponseAdapter(mock_response).adapt()

    upstream_response = self.__flow.response
    self.__response = MitmproxyResponseAdapter(upstream_response).adapt()

    self.__endpoint_show_response = None
    self.__response_param_names = None

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
    self.__response_param_names = ResponseParamNamesFacade(self.__endpoint_show_response['response_param_names'])

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
  def mock_request_id(self) -> Union[str, None]:
    return self.expected_response.headers.get(custom_headers.MOCK_REQUEST_ID)

  @property
  def mock_request_endpoint_id(self) -> Union[str, None]:
    return self.expected_response.headers.get(custom_headers.MOCK_REQUEST_ENDPOINT_ID)

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

    if not isinstance(_decoded_expected_response_content, list) or not isinstance(_decoded_expected_response_content, dict):
      return _decoded_expected_response_content

    if not self.response_param_names:
      return _decoded_expected_response_content

    aliased_response_param_names = self.response_param_names.aliased
    aliases = self.__endpoint_show_response.get('aliases') or []
    if len(aliased_response_param_names) == 0 or len(aliases) == 0:
      return _decoded_expected_response_content

    id_to_alias_map = build_id_to_alias_map(aliases)
    rewrite_params(_decoded_expected_response_content, aliased_response_param_names, id_to_alias_map, trace)

    return _decoded_expected_response_content

  @property
  def start_time(self):
    return self.request.timestamp_start

  @property
  def strategy(self):
    return self.__strategy

  @strategy.setter
  def strategy(self, v: Union[test_strategy.CUSTOM, test_strategy.DIFF, test_strategy.FUZZY]):
    self.__strategy = v

  @property
  def trace(self) -> Union[Trace, None]:
    headers = self.request.headers
    trace_id = headers.get(custom_headers.TRACE_ID)

    if not trace_id:
      return

    return Trace.find(trace_id)