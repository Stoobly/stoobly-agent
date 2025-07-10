from mitmproxy.http import Headers
from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow


def minimize_headers(flow: MitmproxyHTTPFlow):
  minimize_request_headers(flow)
  minimize_response_headers(flow)

def remove_headers(headers: Headers, allowlist: dict[str]):
  keys_to_remove = []

  for key in headers:
    if key.lower() not in {allowed_header.lower() for allowed_header in allowlist}:
      keys_to_remove.append(key)

  for key in keys_to_remove:
    headers.pop(key)

def minimize_request_headers(flow: MitmproxyHTTPFlow) -> None:
  request_headers_allowlist = {
    "Accept",
    "Accept-Encoding",
    "Accept-Language",
    "Content-Length",
    "Content-Type",
    "Host",
    "Origin",
    "Referer",
    "User-Agent",
  }

  remove_headers(flow.request.headers, request_headers_allowlist)

def minimize_response_headers(flow: MitmproxyHTTPFlow) -> None:
  response_headers_allowlist = {
    "Content-Length",
    "Content-Type",
    "Date",
    "Transfer-Encoding",
    "Server",  # Sometimes required for HTTP/1.0, but not strictly mandatory
  }

  remove_headers(flow.response.headers, response_headers_allowlist)
