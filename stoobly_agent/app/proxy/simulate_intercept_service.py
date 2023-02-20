import pdb
import requests

from stoobly_agent.app.proxy.mitmproxy.flow_mock import MitmproxyFlowMock

from .intercept_handler import request as handle_request

def simulate_intercept(request: requests.Request, **config):
  flow = MitmproxyFlowMock()
  flow.request = request

  handle_request(flow)

  if flow.response:
    return flow.response

  session = requests.Session()
  res = session.send(request.prepare(), **config)
  flow.response = res

  return res