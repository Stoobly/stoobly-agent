import pdb

from stoobly_agent.app.proxy.intercept_settings import InterceptSettings
from stoobly_agent.lib.api.endpoints_resource import EndpointsResource

def inject_search_endpoint(intercept_settings: InterceptSettings):
  remote = intercept_settings.settings.remote
  resource = EndpointsResource(remote.api_url, remote.api_key)
  return lambda project_id, method, url: search_endpoint(resource, project_id, method, url)

def search_endpoint(endpoints_resource: EndpointsResource, project_id: int, method: str, url: str):
  res = endpoints_resource.index(**{
    'ignored_components': 1,
    'method': method,
    'project_id': project_id,
    'q': url,
    'size': 1,
  })

  if res.status_code != 200:
    return None

  endpoints = res.json()

  if len(endpoints) == 0:
    return None

  return endpoints[0]
