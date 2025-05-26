import requests

from stoobly_agent.app.models.adapters.python import PythonResponseAdapterFactory
from stoobly_agent.app.proxy.mitmproxy.response_facade import MitmproxyResponseFacade
from stoobly_agent.app.proxy.record.response_string import ResponseString

RAW_FORMAT = 'raw'

def print_raw_response(response: requests.Response, file_path = None):
  mitmproxy_response = PythonResponseAdapterFactory(response).mitmproxy_response()
  facade = MitmproxyResponseFacade(mitmproxy_response)
  response_string = ResponseString(facade, None)

  if not file_path:
    print(response_string.get().decode(), end="")
  else:
    with open(file_path, 'w') as fp:
      fp.write(response_string.get().decode()) 