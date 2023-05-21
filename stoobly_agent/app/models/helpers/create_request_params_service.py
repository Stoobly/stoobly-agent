import pdb

from stoobly_agent.app.models.adapters import JoinedRequestAdapter, RawHttpRequestAdapter, RawHttpResponseAdapter
from stoobly_agent.app.models.adapters.python import PythonRequestAdapterFactory, PythonResponseAdapterFactory

def build_params(raw_requests: str, payloads_delimitter = None):
  try:
    joined_request = JoinedRequestAdapter(raw_requests, payloads_delimitter).adapt()
  except Exception as e:
    return

  request_adapter = RawHttpRequestAdapter(joined_request.request_string.get())
  response_adapter = RawHttpResponseAdapter(joined_request.response_string.get())

  mitmproxy_request = PythonRequestAdapterFactory(request_adapter.to_request()).mitmproxy_request(request_adapter.protocol)
  mitmproxy_response = PythonResponseAdapterFactory(response_adapter.to_response()).mitmproxy_response()

  class MitmproxyFlowMock():
      def __init__(self, request, response):
          self.request = request
          self.response = response

  mitmproxy_flow_mock = MitmproxyFlowMock(mitmproxy_request, mitmproxy_response)

  return {
    'flow': mitmproxy_flow_mock,
    'joined_request': joined_request,
  }