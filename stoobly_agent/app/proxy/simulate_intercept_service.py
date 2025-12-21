import pdb

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from requests import Request

from io import BytesIO
from typing import TYPE_CHECKING
from urllib3.exceptions import InsecureRequestWarning

if TYPE_CHECKING:
    from mitmproxy.http import Request as MitmproxyRequest

from stoobly_agent.app.proxy.mitmproxy.flow_mock import MitmproxyFlowMock
from stoobly_agent.app.models.adapters.mitmproxy import MitmproxyRequestAdapterFactory, MitmproxyResponseAdapterFactory

from .intercept_handler import request as handle_request, response as handle_response

def simulate_intercept(request: 'Request', **config):
  # Lazy import for runtime usage
  import requests
  
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

def __prepare_mitmproxy_request(request: 'MitmproxyRequest') -> 'Request':
  # Lazy import for runtime usage
  import requests
  _request = MitmproxyRequestAdapterFactory(request).python_request()
  return _request.prepare()

def __response(body: bytes, status: int, headers = {}):
  # Lazy import for runtime usage
  import requests
  res = requests.Response()

  res.status_code = status
  res.headers = headers

  from urllib3 import HTTPResponse
  res.raw = HTTPResponse(
    body=BytesIO(body),
    decode_content=False,
    headers=headers,
    preload_content=False
  )

  return res