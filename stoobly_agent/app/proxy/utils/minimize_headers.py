import pdb

from typing import TYPE_CHECKING, Final

if TYPE_CHECKING:
    from mitmproxy.http import Headers
    from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow

REQUEST_HEADERS_ALLOWLIST: Final[dict[str]] = {
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

def minimize_headers(flow: 'MitmproxyHTTPFlow'):
  minimize_request_headers(flow)

def minimize_request_headers(flow: 'MitmproxyHTTPFlow') -> None:
  remove_headers(flow.request.headers, REQUEST_HEADERS_ALLOWLIST)

def remove_headers(headers: 'Headers', allowlist: dict[str]):
  keys_to_remove = []

  for key in headers:
    if key.lower() not in {allowed_header.lower() for allowed_header in allowlist}:
      keys_to_remove.append(key)

  for key in keys_to_remove:
    headers.pop(key)
