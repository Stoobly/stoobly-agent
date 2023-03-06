import pdb
import requests

from mitmproxy.http import Request as MitmproxyRequest

from stoobly_agent.app.proxy.mitmproxy.flow_mock import MitmproxyFlowMock
from stoobly_agent.app.models.adapters.mitmproxy import MitmproxyRequestAdapterFactory, MitmproxyResponseAdapterFactory

from .intercept_handler import request as handle_request, response as handle_response

def simulate_intercept(request: requests.Request, **config):
  flow = MitmproxyFlowMock()

  flow.request = request

  handle_request(flow)

  if not flow.response:
    session = requests.Session()
    prepared_request = __prepare_mitmproxy_request(flow.request)
    res = session.send(prepared_request, **config)
    flow.response = res

  handle_response(flow)

  return MitmproxyResponseAdapterFactory(flow.response).python_response()

def __prepare_mitmproxy_request(request: MitmproxyRequest) -> requests.Request:
  _request = MitmproxyRequestAdapterFactory(request).python_request()
  return _request.prepare()