import pdb

from stoobly_agent.app.models.adapters.orm.request.mitmproxy_adapter import MitmproxyRequestAdapter
from stoobly_agent.app.models.types.request import RequestIndexSimilarParams
from stoobly_agent.app.proxy.mitmproxy.request_facade import MitmproxyRequestFacade
from stoobly_agent.app.proxy.mock.hashed_request_decorator import HashedRequestDecorator
from stoobly_agent.lib.api.interfaces.endpoints import EndpointShowResponse
from stoobly_agent.lib.orm.request import Request

from .endpoints_apply_context import EndpointsApplyContext

def apply_endpoints(context: EndpointsApplyContext):
  for endpoint in context.endpoints:
    for endpoint_handler in context.endpoint_handlers:
      endpoint_handler(endpoint)

    apply_endpoint(context, endpoint)

def apply_endpoint(context: EndpointsApplyContext, endpoint: EndpointShowResponse):
  ignored_components = endpoint['ignored_components'] if 'ignored_components' in endpoint else []
  requests = endpoint_requests(context, endpoint)

  for request in requests:
    for request_handler in context.request_handlers:
      request_handler(request, endpoint)

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

def endpoint_requests(context: EndpointsApplyContext, endpoint: EndpointShowResponse):
  local_db_request_adapter = context.request_model
  if not local_db_request_adapter:
    return []

  host = endpoint['host']
  if not host:
    host = '%'

  port = endpoint['port']
  if not port:
    port = '%'

  method = endpoint['method']
  pattern = endpoint['match_pattern']

  scenario_id = context.scenario_id
  params = RequestIndexSimilarParams(host=host, port=port, method=method, pattern=pattern, scenario_id=scenario_id)
  return local_db_request_adapter.index_similar(params)