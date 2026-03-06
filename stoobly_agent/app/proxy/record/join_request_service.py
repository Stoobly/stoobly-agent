import pdb

from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow, Request as MitmproxyRequest, Response as MitmproxyResponse

from stoobly_agent.app.proxy.intercept_settings import InterceptSettings

from ..mitmproxy.request_facade import MitmproxyRequestFacade
from ..mitmproxy.response_facade import MitmproxyResponseFacade
from .joined_request import JoinedRequest
from .proxy_request import ProxyRequest

class JoinRequestOptions(TypedDict):
    id: str
    intercept_settings: InterceptSettings

def join_request(
    adapted_request: MitmproxyRequestFacade, adapted_response: MitmproxyResponseFacade, **options: JoinRequestOptions
) -> JoinedRequest:
    intercept_settings: InterceptSettings = options.get('intercept_settings')

    # Decorate request with service_url
    upstream_url = intercept_settings.upstream_url if intercept_settings else None
    proxy_request = ProxyRequest(adapted_request, upstream_url)

    if options.get('id'):
        proxy_request.id = options['id']

    # Create JoinedRequest
    return JoinedRequest(proxy_request).with_response(adapted_response)

def join_request_from_flow(
    flow: 'MitmproxyHTTPFlow', **options: JoinRequestOptions
) -> JoinedRequest:
    return join_request_from_request_response(flow.request, flow.response, **options)

def join_request_from_request_response(
    request: 'MitmproxyRequest', response: 'MitmproxyResponse', **options: JoinRequestOptions
):
    request = MitmproxyRequestFacade(request)
    response = MitmproxyResponseFacade(response)

    return join_request(request, response, **options)