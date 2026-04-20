import json
import logging
import os
import re
from typing import Any, Dict, List, Optional, Set, Tuple, Union
from urllib.parse import urlparse

from stoobly_agent.app.cli.helpers.feature_flags import remote as remote_feature
from stoobly_agent.app.cli.helpers.openapi_endpoint_adapter import OpenApiEndpointAdapter
from stoobly_agent.app.proxy.mock.hashed_request_decorator import COMPONENT_TYPES
from stoobly_agent.app.settings import Settings
from stoobly_agent.lib.api.keys.project_key import InvalidProjectKey, ProjectKey
from stoobly_agent.lib.api.endpoints_resource import EndpointsResource
from stoobly_agent.lib.api.interfaces.endpoints import EndpointShowResponse, IgnoredComponent

logger = logging.getLogger(__name__)

LayerKind = str  # "openapi" | "project"


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


def _map_key_for_endpoint_id(endpoint: EndpointShowResponse) -> Optional[str]:
  eid = endpoint.get("id")
  return str(eid) if eid is not None else None


def _optional_project_key(key: Optional[Union[str, ProjectKey]]) -> Optional[ProjectKey]:
  if key is None:
    return None
  if isinstance(key, ProjectKey):
    return key
  try:
    return ProjectKey(key)
  except InvalidProjectKey:
    return None


class EndpointCache:
  """
  Singleton: one map `_by_endpoint_id` (key = endpoint id) layering OpenAPI and remote
  project endpoints. Each merge assigns a monotonic sequence; higher sequence wins on duplicate
  keys and is tried first during search.
  """

  _instance: Optional["EndpointCache"] = None

  def __new__(cls) -> "EndpointCache":
    if cls._instance is None:
      inst = super().__new__(cls)
      inst._file_parse_cache: Dict[str, List[EndpointShowResponse]] = {}
      inst._project_fetch_cache: Dict[Tuple[str, str], List[EndpointShowResponse]] = {}
      inst._merged_openapi_paths: Set[str] = set()
      inst._merged_project_keys: Set[Tuple[str, str]] = set()
      inst._by_endpoint_id: Dict[str, Tuple[int, LayerKind, EndpointShowResponse]] = {}
      inst._merge_seq: int = 0
      inst._last_project_id: Optional[str] = None
      cls._instance = inst
    return cls._instance

  @classmethod
  def instance(cls) -> "EndpointCache":
    inst = cls()
    inst._ensure_prefetch_from_settings()
    return inst

  def _ensure_prefetch_from_settings(self) -> None:
    """
    Eager-load remote endpoints from settings (remote feature only): first the intercept
    project key when it is non-local, then settings.remote.project_key when non-local.
    """
    settings = Settings.instance()
    if not remote_feature(settings):
      return
    try:
      ik = settings.proxy.intercept.project_key
      if ik:
        p = ProjectKey(ik)
        if not p.is_local:
          self.with_project(str(p.id))
    except InvalidProjectKey:
      pass
    try:
      rk = settings.remote.project_key
      if rk:
        p = ProjectKey(rk)
        if not p.is_local:
          self.with_project(str(p.id))
    except InvalidProjectKey:
      pass

  def _next_merge_seq(self) -> int:
    self._merge_seq += 1
    return self._merge_seq

  def clear_cache(self) -> None:
    """Drop all cached OpenAPI parses, remote index responses, and merged endpoint maps."""
    self._file_parse_cache.clear()
    self._project_fetch_cache.clear()
    self._merged_openapi_paths.clear()
    self._merged_project_keys.clear()
    self._by_endpoint_id.clear()
    self._merge_seq = 0
    self._last_project_id = None

  def _get_openapi_endpoints_list(self, normalized_path: str) -> List[EndpointShowResponse]:
    if normalized_path not in self._file_parse_cache:
      self._file_parse_cache[normalized_path] = load_openapi_endpoints_from_file(normalized_path)
    return self._file_parse_cache[normalized_path]

  def _fetch_project_endpoints(self, project_id: str, **index_params: Any) -> List[EndpointShowResponse]:
    params_key = json.dumps(index_params, sort_keys=True, default=str)
    cache_key = (str(project_id), params_key)
    if cache_key not in self._project_fetch_cache:
      settings = Settings.instance()
      resource = EndpointsResource(settings.remote.api_url, settings.remote.api_key)
      res = resource.index(project_id=str(project_id), **index_params)
      if res.status_code != 200:
        logger.warning("Endpoints index failed for project %s: %s %s", project_id, res.status_code, res.text)
        self._project_fetch_cache[cache_key] = []
      else:
        data = res.json()
        self._project_fetch_cache[cache_key] = data if isinstance(data, list) else []
    return self._project_fetch_cache[cache_key]

  def _merge_openapi_specification(self, path: str) -> "EndpointCache":
    """Layer OpenAPI endpoints onto the map (id keys; latest merge wins on collision)."""
    normalized = _normalize_open_api_spec_path(path)
    if normalized in self._merged_openapi_paths:
      return self
    self._merged_openapi_paths.add(normalized)
    endpoints = self._get_openapi_endpoints_list(normalized)
    seq = self._next_merge_seq()
    for ep in endpoints:
      kid = _map_key_for_endpoint_id(ep)
      if kid is None:
        logger.warning("Skipping OpenAPI endpoint without id: %s %s", ep.get("method"), ep.get("path"))
        continue
      self._by_endpoint_id[kid] = (seq, "openapi", ep)
    return self

  def _merge_project_endpoints(self, project_id: str, **index_params: Any) -> "EndpointCache":
    """
    Layer remote project endpoints onto the map. index_params are merged with ignored_components=1
    for the index request.
    """
    params: Dict[str, Any] = {"ignored_components": 1, **index_params}
    merge_key = (str(project_id), json.dumps(params, sort_keys=True, default=str))
    if merge_key in self._merged_project_keys:
      return self
    self._merged_project_keys.add(merge_key)
    endpoints = self._fetch_project_endpoints(str(project_id), **params)
    seq = self._next_merge_seq()
    self._last_project_id = str(project_id)
    for ep in endpoints:
      kid = _map_key_for_endpoint_id(ep)
      if kid is None:
        logger.warning("Skipping remote endpoint without id: %s %s", ep.get("method"), ep.get("path"))
        continue
      self._by_endpoint_id[kid] = (seq, "project", ep)
    return self

  def with_openapi_specification(self, path: str) -> "EndpointCache":
    return self._merge_openapi_specification(path)

  def with_project(
    self,
    project: Optional[Union[str, ProjectKey]] = None,
    **index_params: Any,
  ) -> "EndpointCache":
    """
    Layer remote project endpoints into cache.

    Accepts either:
    - a raw project id (legacy callers), or
    - a ProjectKey / key string; local keys are ignored.

    Index params are passed through as-is for the API request.
    """
    if project is None:
      return self

    if not remote_feature(Settings.instance()):
      return self

    pk = _optional_project_key(project)
    if pk is not None:
      if pk.is_local:
        return self
      project_id = str(pk.id)
    else:
      project_id = str(project)

    return self._merge_project_endpoints(project_id, **index_params)

  def search(self, method: str, url: str, **query_params: Any) -> Optional[EndpointShowResponse]:
    if not self._by_endpoint_id:
      return None
    ordered = sorted(self._by_endpoint_id.values(), key=lambda t: -t[0])
    endpoints = [t[2] for t in ordered]
    ep = _find_matching_endpoint(endpoints, method, url)
    if ep is None:
      return None
    kid = _map_key_for_endpoint_id(ep)
    merged: EndpointShowResponse = dict(ep)
    if kid is not None:
      _seq, kind, _stored = self._by_endpoint_id[kid]
      if kind == "openapi":
        merged["ignored_components"] = build_ignored_components_from_openapi_endpoint(ep)
    return merged

  def show(self, endpoint_id: Union[int, str]) -> Optional[EndpointShowResponse]:
    """Return the merged endpoint for this id, or None if it is not in the cache."""
    kid = str(endpoint_id)
    entry = self._by_endpoint_id.get(kid)
    if entry is None:
      return None
    _seq, kind, ep = entry
    merged: EndpointShowResponse = dict(ep)
    if kind == "openapi":
      merged["ignored_components"] = build_ignored_components_from_openapi_endpoint(ep)
    return merged

  def index(self, **query_params: Any) -> Union[List[EndpointShowResponse], List[Any]]:
    if not self._by_endpoint_id:
      return []
    if query_params:
      settings = Settings.instance()
      resource = EndpointsResource(settings.remote.api_url, settings.remote.api_key)
      merged: Dict[str, Any] = dict(query_params)
      if self._last_project_id is not None:
        merged.setdefault("project_id", self._last_project_id)
      res = resource.index(**merged)
      if res.status_code != 200:
        logger.warning("Endpoints index failed: %s %s", res.status_code, res.text)
        return []
      data = res.json()
      return data if isinstance(data, list) else []

    return [v[2] for _eid, v in sorted(self._by_endpoint_id.items(), key=lambda x: x[0])]


endpoint_cache = EndpointCache.instance()
