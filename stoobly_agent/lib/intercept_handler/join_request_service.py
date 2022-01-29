from ..joined_request import JoinedRequest
from ..mitmproxy_request_adapter import MitmproxyRequestAdapter
from ..mitmproxy_response_adapter import MitmproxyResponseAdapter
from ..proxy_request import ProxyRequest
from .settings import get_service_url

def join_request(flow, active_mode_settings):
    param_filters = active_mode_settings.get('filter_patterns')

    # Adapt flow.request
    request = MitmproxyRequestAdapter(flow.request)
    request.with_param_filters(param_filters)

    # Decorate request with service_url
    service_url = get_service_url(flow.request, active_mode_settings)
    proxy_request = ProxyRequest(request, service_url)

    # Adapt flow.response
    response = MitmproxyResponseAdapter(flow.response)
    response.with_param_filters(param_filters)

    # Create JoinedRequest
    return JoinedRequest(proxy_request).with_response(response)
