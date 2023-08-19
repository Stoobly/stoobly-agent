import pdb
from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow

from stoobly_agent.app.proxy.intercept_settings import InterceptSettings

from ..mitmproxy.request_facade import MitmproxyRequestFacade
from ..mitmproxy.response_facade import MitmproxyResponseFacade
from .joined_request import JoinedRequest
from .proxy_request import ProxyRequest

def join_request(
    adapted_request: MitmproxyRequestFacade, adapted_response: MitmproxyResponseFacade, intercept_settings: InterceptSettings
) -> JoinedRequest:
    # Decorate request with service_url
    upstream_url = intercept_settings.upstream_url
    proxy_request = ProxyRequest(adapted_request, upstream_url)

    # Create JoinedRequest
    return JoinedRequest(proxy_request).with_response(adapted_response)

def join_rewritten_request(flow: MitmproxyHTTPFlow, intercept_settings: InterceptSettings) -> JoinedRequest:
    # Adapt flow.request
    request = MitmproxyRequestFacade(flow.request)

    # Adapt flow.response
    response = MitmproxyResponseFacade(flow.response)
    rewrite_rules = intercept_settings.record_rewrite_rules

    request.with_parameter_rules(rewrite_rules).with_url_rules(rewrite_rules).rewrite()
    response.with_rewrite_rules(rewrite_rules).rewrite()

    return join_request(request, response, intercept_settings)