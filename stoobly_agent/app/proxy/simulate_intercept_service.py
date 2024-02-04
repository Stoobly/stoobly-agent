import pdb
import requests

from io import BytesIO
from mitmproxy.http import Request as MitmproxyRequest
from urllib3 import HTTPResponse
from urllib3.exceptions import InsecureRequestWarning

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

    res = None 

    if not config.get('verify'):
      # Suppress only the single warning from urllib3 needed.
      requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

    try:
      res = session.send(prepared_request, **{'timeout': 300, **config})
    except requests.exceptions.ConnectTimeout:
      res = __response(b'Gateway Timeout', 504)
    except requests.exceptions.SSLError as e:
      res = __response(str(e).encode(), 502)
    except requests.exceptions.ConnectionError:
      res = __response(b'Bad Gateway', 502)
    except Exception:
      res = __response(b'Unknown Error', 0)

    flow.response = res

  handle_response(flow)

  return MitmproxyResponseAdapterFactory(flow.response).python_response()

def __prepare_mitmproxy_request(request: MitmproxyRequest) -> requests.Request:
  _request = MitmproxyRequestAdapterFactory(request).python_request()
  return _request.prepare()

def __response(body: bytes, status: int, headers = {}):
  res = requests.Response()

  res.status_code = status
  res.headers = headers
  res.raw = HTTPResponse(
    body=BytesIO(body),
    decode_content=False,
    headers=headers,
    preload_content=False
  )

  return res