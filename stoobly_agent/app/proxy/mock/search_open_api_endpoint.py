import logging
import os
import re
from typing import Dict, List, Optional
from urllib.parse import urlparse

from stoobly_agent.app.cli.helpers.openapi_endpoint_adapter import OpenApiEndpointAdapter
from stoobly_agent.app.proxy.intercept_settings import InterceptSettings
from stoobly_agent.app.proxy.mock.hashed_request_decorator import COMPONENT_TYPES
from stoobly_agent.lib.api.interfaces.endpoints import EndpointShowResponse, IgnoredComponent

logger = logging.getLogger(__name__)

class OpenApiEndpointCache:
  """Lazy cache of parsed endpoints keyed by resolved absolute spec path."""

  def __init__(self):
    self._by_path: Dict[str, List[EndpointShowResponse]] = {}

  def endpoints_for(self, open_api_spec: str) -> List[EndpointShowResponse]:
    key = _normalize_open_api_spec_path(open_api_spec)
    if key not in self._by_path:
      self._by_path[key] = load_openapi_endpoints_from_file(key)
    return self._by_path[key]


_endpoint_cache = OpenApiEndpointCache()

def load_openapi_endpoints_from_file(open_api_spec: str) -> List[EndpointShowResponse]:
  """
  Parse an OpenAPI spec file into a list of endpoint show responses.
  """
  try:
    return OpenApiEndpointAdapter().adapt_from_file(open_api_spec)
  except Exception as e:
    logger.warning("Failed to load OpenAPI spec %s: %s", open_api_spec, e)
    return []


def sql_like(value: str, pattern: str) -> bool:
  """
  SQLite LIKE semantics for ASCII: % = any sequence, _ = single character.
  """
  parts: List[str] = []
  for c in pattern:
    if c == "%":
      parts.append(".*")
    elif c == "_":
      parts.append(".")
    else:
      parts.append(re.escape(c))
  regex = "".join(parts)
  return re.fullmatch(regex, value, flags=re.DOTALL) is not None


def _normalize_open_api_spec_path(open_api_spec: str) -> str:
  return os.path.abspath(os.path.normpath(open_api_spec))

def _request_port_str(uri) -> str:
  if uri.port is not None:
    return str(uri.port)
  if uri.scheme == "https":
    return "443"
  if uri.scheme == "http":
    return "80"
  return "0"


def _endpoint_hostname_from_netloc(host_field: str) -> Optional[str]:
  """
  OpenApiEndpointAdapter stores server netloc in host (e.g. 'localhost:80', 'petstore.swagger.io').
  Requests use urlparse().hostname without port when the URL omits :port.
  """
  if "://" in host_field:
    parsed = urlparse(host_field)
  else:
    parsed = urlparse("http://" + host_field)
  return parsed.hostname.lower() if parsed.hostname else None


def _host_matches(endpoint: EndpointShowResponse, request_hostname: Optional[str]) -> bool:
  host = endpoint.get("host") or ""
  if not host or host == "%":
    return True
  if host == "-":
    return True
  if not request_hostname:
    return False
  ep_hostname = _endpoint_hostname_from_netloc(host)
  if ep_hostname is None:
    return True
  return ep_hostname == request_hostname.lower()


def _port_matches(endpoint: EndpointShowResponse, request_port: str) -> bool:
  port = endpoint.get("port") or ""
  if not port or port == "%":
    return True
  return port == request_port


def _path_matches(endpoint: EndpointShowResponse, request_path: str) -> bool:
  match_pattern = endpoint.get("match_pattern") or ""
  like_pattern = f"%{match_pattern}"
  return sql_like(request_path, like_pattern)


def _find_matching_endpoint(
  endpoints: List[EndpointShowResponse],
  method: str,
  url: str,
) -> Optional[EndpointShowResponse]:
  uri = urlparse(url)
  request_path = uri.path or ""
  request_path = request_path.rstrip("/") or "/"
  request_hostname = uri.hostname
  request_port = _request_port_str(uri)
  method_u = method.upper()

  for endpoint in endpoints:
    if endpoint.get("method", "").upper() != method_u:
      continue
    if not _host_matches(endpoint, request_hostname):
      continue
    if not _port_matches(endpoint, request_port):
      continue
    if not _path_matches(endpoint, request_path):
      continue
    return endpoint

  return None


def _component_matches_ignoreable_ignored(component: dict) -> bool:
  """
  Mirrors stoobly-api Ignoreable#ignored?: !is_deterministic || !is_required
  (see app/models/endpoint.rb ignored_components and app/models/concerns/ignoreable.rb).
  """
  is_deterministic = component.get("is_deterministic", True)
  is_required = component.get("is_required", True)
  return (not is_deterministic) or (not is_required)


def build_ignored_components_from_openapi_endpoint(endpoint: EndpointShowResponse) -> List[IgnoredComponent]:
  """
  Mirrors Endpoint#ignored_components: query/header/body/response_header names where ignored?,
  serialized like endpoints/_ignored_component.json.jbuilder (name, query, type).
  """
  out: List[IgnoredComponent] = []

  for row in endpoint.get("query_param_names") or []:
    if _component_matches_ignoreable_ignored(row):
      out.append(
        {
          "name": row["name"],
          "query": row["name"],
          "type": COMPONENT_TYPES["QUERY_PARAM"],
        }
      )

  for row in endpoint.get("header_names") or []:
    if _component_matches_ignoreable_ignored(row):
      out.append(
        {
          "name": row["name"],
          "query": row["name"],
          "type": COMPONENT_TYPES["HEADER"],
        }
      )

  for row in endpoint.get("body_param_names") or []:
    if _component_matches_ignoreable_ignored(row):
      out.append(
        {
          "name": row["name"],
          "query": row["query"],
          "type": COMPONENT_TYPES["BODY_PARAM"],
        }
      )

  for row in endpoint.get("response_header_names") or []:
    if _component_matches_ignoreable_ignored(row):
      out.append(
        {
          "name": row["name"],
          "query": row["name"],
          "type": COMPONENT_TYPES["RESPONSE_HEADER"],
        }
      )

  return out


def search_open_api_endpoint(
  open_api_spec: str,
  method: str,
  url: str,
  **_query_params,
) -> Optional[EndpointShowResponse]:
  endpoints = _endpoint_cache.endpoints_for(open_api_spec)
  if not endpoints:
    return None
  ep = _find_matching_endpoint(endpoints, method, url)
  if ep is None:
    return None
  merged: EndpointShowResponse = dict(ep)
  merged["ignored_components"] = build_ignored_components_from_openapi_endpoint(ep)
  return merged


def inject_search_open_api_endpoint(intercept_settings: InterceptSettings):
  def _search(method: str, url: str, **_query_params):
    open_api_spec = intercept_settings.openapi_specification_path
    if not open_api_spec:
      return None
    return search_open_api_endpoint(open_api_spec, method, url, **_query_params)

  return _search
