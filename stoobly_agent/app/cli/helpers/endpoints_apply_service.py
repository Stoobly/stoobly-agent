import pdb
from typing import Callable, TypedDict

from stoobly_agent.app.models.adapters.orm.request.mitmproxy_adapter import MitmproxyRequestAdapter
from stoobly_agent.app.proxy.mitmproxy.request_facade import MitmproxyRequestFacade
from stoobly_agent.app.proxy.mock.hashed_request_decorator import HashedRequestDecorator
from stoobly_agent.app.settings import Settings
from stoobly_agent.lib.api.endpoints_resource import EndpointsResource
from stoobly_agent.lib.api.interfaces.endpoints import EndpointShowResponse
from stoobly_agent.lib.orm.request import Request

class Handlers(TypedDict):
  endpoint_handler: Callable[[EndpointShowResponse], None]
  request_handler: Callable[[Request], None]

def apply_endpoints(project_id: int, **handlers: Handlers):
  settings = Settings.instance()

  resource = EndpointsResource(settings.remote.api_url, settings.remote.api_key)
  res = resource.index(project_id=project_id, ignored_components=1)
  res.raise_for_status()  
  
  endpoints = res.json()
  endpoint_handler = handlers.get('endpoint_handler')
  for endpoint in endpoints:
    if endpoint_handler:
      endpoint_handler(endpoint)

    apply_endpoint(endpoint, handlers.get('request_handler'))

def apply_endpoint(endpoint: EndpointShowResponse, request_handler = None):
  ignored_components = endpoint['ignored_components']
  requests = Request.where('path', 'like', endpoint['match_pattern']).get()

  for request in requests:
    if request_handler:
      request_handler(request)

    hash_request(request, ignored_components)

def hash_request(request: Request, ignored_components = []):
  mitmproxy_request = MitmproxyRequestAdapter(request).adapt()
  request_facade = MitmproxyRequestFacade(mitmproxy_request)
  hashed_request = HashedRequestDecorator(request_facade)

  hashed_request.with_ignored_components(ignored_components) 

  request.headers_hash = hashed_request.headers_hash()
  request.query_params_hash = hashed_request.query_params_hash()
  request.body_params_hash = hashed_request.body_params_hash()
  request.body_text_hash = hashed_request.body_text_hash()

  request.save()