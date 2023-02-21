import pdb
import requests

from stoobly_agent.app.proxy.mitmproxy.flow_mock import MitmproxyFlowMock

from .intercept_handler import request as handle_request, response as handle_response

def simulate_intercept(request: requests.Request, **config):
  flow = MitmproxyFlowMock()
  flow.request = request

  handle_request(flow)

  res = None
  if not flow.response:
    session = requests.Session()
    res = session.send(request.prepare(), **config)
    flow.response = res

  handle_response(flow)

  return flow.response