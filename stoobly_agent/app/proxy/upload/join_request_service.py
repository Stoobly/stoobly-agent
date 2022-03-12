import pdb
from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow

from ..mitmproxy.request_adapter import MitmproxyRequestAdapter
from ..mitmproxy.response_adapter import MitmproxyResponseAdapter
from ..settings import get_service_url

from .joined_request import JoinedRequest
from .proxy_request import ProxyRequest

def join_request(
    adapted_request:  MitmproxyRequestAdapter, adapted_response: MitmproxyResponseAdapter, active_mode_settings
) -> JoinedRequest:
    # Decorate request with service_url
    service_url = get_service_url(adapted_request.request, active_mode_settings)
    proxy_request = ProxyRequest(adapted_request, service_url)

    # Create JoinedRequest
    return JoinedRequest(proxy_request).with_response(adapted_response)

def join_rewritten_request(flow: MitmproxyHTTPFlow, active_mode_settings) -> JoinedRequest:
    # Adapt flow.request
    request = MitmproxyRequestAdapter(flow.request)

    # Adapt flow.response
    response = MitmproxyResponseAdapter(flow.response)

    rewrite_rules: list = active_mode_settings.get('rewrite_rules')
    request.rewrite(rewrite_rules)
    response.filter(rewrite_rules)

    return join_request(request, response, active_mode_settings)

def join_filtered_request(flow: MitmproxyHTTPFlow, active_mode_settings) -> JoinedRequest:
    # Adapt flow.request
    request = MitmproxyRequestAdapter(flow.request)

    # Adapt flow.response
    response = MitmproxyResponseAdapter(flow.response)

    filter_rules: list = active_mode_settings.get('filter_rules')
    request.filter(filter_rules)
    response.filter(filter_rules)

    return join_request(request, response, active_mode_settings)