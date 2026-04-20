from stoobly_agent.app.proxy.mock.endpoint_cache import endpoint_cache


def inject_search_endpoint(project_id):
  project_id = str(project_id)

  def _search(method: str, url: str, **query_params):
    return search_endpoint(project_id, method, url, **query_params)

  return _search


def search_endpoint(
  project_id,
  method: str,
  url: str,
  **query_params,
):
  endpoint_cache.with_project_endpoints(str(project_id), **query_params)
  return endpoint_cache.search(method, url)
