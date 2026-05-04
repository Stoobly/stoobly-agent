import pdb

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from requests import Response
    from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow
    from mitmproxy.http import Response as MitmproxyResponse

###
#
# Return response headers, body, and status code
#
def apply_response(flow: 'MitmproxyHTTPFlow', res: 'Response'):
    # Lazy import for runtime usage
    from mitmproxy.http import Response as MitmproxyResponse
    
    # Without specifying a length to read, requests will compare content length
    # with Content-Length header. If the content is gzipped, an IncompleteRead error will be thrown
    #content = res.raw.read(res.raw.length_remaining)

    # Ideally we just return the HTTPResponse object from res.raw
    # See Issue #11
    # content = res.raw
    content = res.content

    flow.response = MitmproxyResponse.make(
        res.status_code, content, dict(res.headers.items())
    )

def bad_request(flow: 'MitmproxyHTTPFlow', message: str):
    # Lazy import for runtime usage
    from mitmproxy.http import Response as MitmproxyResponse
    flow.response = MitmproxyResponse.make(
        400,  # (optional) status code
        message,
        {'Content-Type': 'text/plain'}  # (optional) headers
    )

def enable_cors(flow: 'MitmproxyHTTPFlow'):
    # Lazy import for runtime usage
    from mitmproxy.http import Response as MitmproxyResponse
    flow.response = MitmproxyResponse.make(
        200,
        '',
        {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, OPTIONS, POST, PATCH, PUT, DELETE',
            'Access-Control-Allow-Headers': '*'
        }
    )

# Without deleting this header, causes parsing issues when reading response
# Note: this should only be applied to live responses and not mocked responses
def disable_transfer_encoding(response: 'MitmproxyResponse') -> None:
    header_name = 'Transfer-Encoding'
    header_values = response.headers.get_all(header_name)

    if len(header_values) > 0:
        # Remove chunked transfer encoding
        new_header_values = [v for v in header_values if v.lower() != 'chunked']

        if len(new_header_values) != len(header_values):
            response.headers.set_all(header_name, new_header_values)
            response.headers['Content-Length'] = str(len(response.content))
