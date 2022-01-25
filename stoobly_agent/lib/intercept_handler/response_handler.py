from mitmproxy import http
from urllib.parse import urlparse

def reverse_proxy(request, service_url, options = {}):
    uri = urlparse(service_url)

    request.scheme = uri.scheme
    request.host = uri.hostname
    if uri.port:
        request.port = uri.port

###
#
# Return response headers, body, and status code
#
def pass_on(flow, res):
    # Ideally we just return the HTTPResponse object from res.raw
    # See Issue #11
    #flow.response = res.raw

    headers = {}
    for key, value in res.headers.items():
        headers[key.capitalize()] = value

    # Without specifying a length to read, requests will compare content length
    # with Content-Length header. If the content is gzipped, an IncompleteRead error will be thrown
    #content = res.raw.read(res.raw.length_remaining)

    content = res.content

    flow.response = http.HTTPResponse.make(
        res.status_code, content, headers,
    )

def bad_request(flow, message):
    flow.response = http.HTTPResponse.make(
        400,  # (optional) status code
        message,
        {'Content-Type': 'text/plain'}  # (optional) headers
    )

    return False
