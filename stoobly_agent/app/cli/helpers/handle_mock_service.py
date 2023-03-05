import requests

from stoobly_agent.app.models.adapters.python import PythonResponseAdapterFactory
from stoobly_agent.app.models.adapters.raw_http_response_adapter import DEFAULT_HTTP_VERSION
from stoobly_agent.app.proxy.mitmproxy.response_facade import MitmproxyResponseFacade
from stoobly_agent.app.proxy.upload.response_string import ResponseString

RAW_FORMAT = 'raw'

def print_raw_response(response: requests.Response):
  http_version = DEFAULT_HTTP_VERSION
  if hasattr(response, 'raw'): 
    http_version = f"HTTP/{response.raw.version / 10.0}"

  mitmproxy_response = PythonResponseAdapterFactory(response).mitmproxy_response(http_version)
  facade = MitmproxyResponseFacade(mitmproxy_response)
  response_string = ResponseString(facade, None)

  print(response_string.get().decode())