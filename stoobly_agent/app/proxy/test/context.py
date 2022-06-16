import pdb

from mitmproxy.http import HTTPFlow, HTTPRequest
from typing import Union

from stoobly_agent.app.proxy.mock.context import MockContext
from stoobly_agent.app.proxy.test.mitmproxy_response_adapter import MitmproxyResponseAdapter
from stoobly_agent.app.proxy.test.requests_response_adapter import RequestsResponseAdapter

from stoobly_agent.config.constants import custom_headers, test_strategy
from stoobly_agent.lib.orm.trace import Trace

from .context_response import TestContextResponse

class TestContext():
  def __init__(self, flow: HTTPFlow, mock_context: MockContext):
    self.__flow = flow
    self.__mock_context = mock_context
    self.__strategy = test_strategy.DIFF

    mock_response = self.__mock_context.response
    self.__expected_response = RequestsResponseAdapter(mock_response).adapt()

    upstream_response = self.__flow.response
    self.__response = MitmproxyResponseAdapter(upstream_response).adapt()

  @property
  def end_time(self):
    return self.__flow.response.timestamp_end

  @property
  def expected_response(self) -> TestContextResponse:
    return self.__expected_response

  @property
  def mock_request_id(self) -> Union[str, None]:
    return self.expected_response.headers.get(custom_headers.MOCK_REQUEST_ID)

  @property
  def mock_request_endpoint_id(self) -> Union[str, None]:
    return self.expected_response.headers.get(custom_headers.MOCK_REQUEST_ENDPOINT_ID)

  @property
  def request(self) -> HTTPRequest:
    return self.__flow.request

  @property
  def response(self) -> TestContextResponse:
    return self.__response

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