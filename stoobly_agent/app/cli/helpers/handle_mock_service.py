import requests

from stoobly_agent.app.models.adapters.python import PythonResponseAdapterFactory
from stoobly_agent.app.proxy.mitmproxy.response_facade import MitmproxyResponseFacade
from stoobly_agent.app.proxy.record.response_string import ResponseString

RAW_FORMAT = 'raw'

def print_raw_response(response: requests.Response):
  mitmproxy_response = PythonResponseAdapterFactory(response).mitmproxy_response()
  facade = MitmproxyResponseFacade(mitmproxy_response)
  response_string = ResponseString(facade, None)

  print(response_string.get().decode(), end="")