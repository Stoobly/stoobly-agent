import pdb

from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow
from typing import List

from stoobly_agent.app.proxy.intercept_settings import InterceptSettings
from stoobly_agent.app.settings.rewrite_rule import RewriteRule

from ..mitmproxy.request_facade import MitmproxyRequestFacade
from ..mitmproxy.response_facade import MitmproxyResponseFacade
from ..utils.rewrite import rewrite_request_response
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

def join_request_from_flow(
    flow: MitmproxyHTTPFlow, intercept_settings: InterceptSettings
) -> JoinedRequest:
    request = MitmproxyRequestFacade(flow.request)
    response = MitmproxyResponseFacade(flow.response)

    return join_request(request, response, intercept_settings)