import json

from mitmproxy.http import Request as MitmproxyRequest
from urllib.parse import urlparse

from stoobly_agent.lib.logger import Logger
from stoobly_agent.lib.orm.utils.requests_response_builder import RequestsResponseBuilder

def reverse_proxy(request: MitmproxyRequest, service_url: str, options = {}):
    Logger.instance().debug(f"ReverseProxy:ServiceUrl: {service_url}")

    uri = urlparse(service_url)

    request.scheme = uri.scheme
    request.host = uri.hostname
    if uri.port:
        request.port = uri.port

def build_response(passed, log):
    body = json.dumps({
        'log': log,
        'passed': passed,
    }).encode()
 
    builder = RequestsResponseBuilder()
    builder.with_header('content-type', 'application/json')
    builder.with_body(body)
    builder.with_status_code(200)

    return builder.build()