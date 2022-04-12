from mitmproxy import http
from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow
from mitmproxy.net.http.request import Request as MitmproxyRequest
from urllib.parse import urlparse

from stoobly_agent.lib.logger import Logger

def reverse_proxy(request: MitmproxyRequest, service_url: str, options = {}):
    Logger.instance().debug(f"ReverseProxy:ServiceUrl: {service_url}")

    uri = urlparse(service_url)

    request.scheme = uri.scheme
    request.host = uri.hostname
    if uri.port:
        request.port = uri.port

