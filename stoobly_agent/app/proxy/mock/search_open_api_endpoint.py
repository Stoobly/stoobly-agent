from typing import Optional

from stoobly_agent.app.proxy.mock.endpoint_cache import endpoint_cache
from stoobly_agent.lib.api.interfaces.endpoints import EndpointShowResponse

def search_open_api_endpoint(
  open_api_spec: str,
  method: str,
  url: str,
) -> Optional[EndpointShowResponse]:
  endpoint_cache.with_openapi_specification(open_api_spec)
  return endpoint_cache.search(method, url)


def inject_search_open_api_endpoint(open_api_spec: Optional[str]):
  def _search(method: str, url: str):
    if not open_api_spec:
      return None
    return search_open_api_endpoint(open_api_spec, method, url)

  return _search
