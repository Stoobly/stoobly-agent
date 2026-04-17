from typing import List

from stoobly_agent.app.models.adapters.python import PythonRequestAdapterFactory
from stoobly_agent.app.models.adapters.raw_http_request_adapter import RawHttpRequestAdapter
from stoobly_agent.app.proxy.mitmproxy.request_facade import MitmproxyRequestFacade
from stoobly_agent.app.proxy.mock.hashed_request_decorator import HashedRequestDecorator
from stoobly_agent.lib.orm.request import Request

COMPONENT_HASH_KEYS = ['headers_hash', 'query_params_hash', 'body_params_hash', 'body_text_hash']

def component_hashes(query_params: dict):
  return {
    key: query_params[key]
    for key in COMPONENT_HASH_KEYS
    if query_params.get(key) is not None
  }

def filter_requests_by_hashes(requests: List[Request], component_hashes: dict, ignored_components: list):
  matched_requests = []

  for request in requests:
    request_hashes = __request_hashes(request, ignored_components)
    matches = True

    for key, value in component_hashes.items():
      if request_hashes.get(key) != value:
        matches = False
        break

    if matches:
      matched_requests.append(request)

  return matched_requests

def __request_hashes(request: Request, ignored_components: list):
  python_request = RawHttpRequestAdapter(request.raw).to_request()
  http_version = request.http_version
  if isinstance(http_version, float):
    http_version = f"HTTP/{http_version}"
  if not http_version:
    http_version = 'HTTP/1.1'

  mitmproxy_request = PythonRequestAdapterFactory(python_request).mitmproxy_request(http_version)
  request_facade = MitmproxyRequestFacade(mitmproxy_request)
  hashed_request = HashedRequestDecorator(request_facade).with_ignored_components(ignored_components or [])

  return {
    'headers_hash': hashed_request.headers_hash(),
    'query_params_hash': hashed_request.query_params_hash(),
    'body_params_hash': hashed_request.body_params_hash(),
    'body_text_hash': hashed_request.body_text_hash(),
  }
