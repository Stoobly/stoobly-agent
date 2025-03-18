import pdb

from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow
from mitmproxy.http import Response as MitmproxyResponse
from requests import Response

###
#
# Return response headers, body, and status code
#
def pass_on(flow: MitmproxyHTTPFlow, res: Response):
    if not isinstance(res, Response):
        return
  
    headers = {}
    for key, value in res.headers.items():
        headers[key.title()] = value

    # Without specifying a length to read, requests will compare content length
    # with Content-Length header. If the content is gzipped, an IncompleteRead error will be thrown
    #content = res.raw.read(res.raw.length_remaining)

    # Ideally we just return the HTTPResponse object from res.raw
    # See Issue #11
    # content = res.raw
    content = res.content

    flow.response = MitmproxyResponse.make(
        res.status_code, content, headers,
    )

def bad_request(flow: MitmproxyHTTPFlow, message: str):
    flow.response = MitmproxyResponse.make(
        400,  # (optional) status code
        message,
        {'Content-Type': 'text/plain'}  # (optional) headers
    )

# Without deleting this header, causes parsing issues when reading response
def disable_transfer_encoding(response: MitmproxyResponse) -> None:
    header_name = 'Transfer-Encoding'
    if header_name in response.headers and response.headers[header_name] == 'chunked':
        del response.headers['Transfer-Encoding']