import hashlib

from typing import Callable, Dict, List, Optional

from stoobly_agent.app.models.adapters.python import PythonRequestAdapterFactory
from stoobly_agent.app.models.adapters.raw_http_request_adapter import RawHttpRequestAdapter
from stoobly_agent.app.proxy.mitmproxy.request_facade import MitmproxyRequestFacade
from stoobly_agent.lib.cache import Cache
from stoobly_agent.lib.orm.request import Request

SUFFIX = 'last_request_id'
STOOBLY_HEADER_PREFIX = 'x-stoobly-'

def access_request(session_id: str, request_id: int, timeout = None):
  cache = Cache.instance()
  _last_request_id_key = __last_request_id_key(session_id)
  cache.write(_last_request_id_key, request_id, timeout)

def generate_session_id(query: dict):
  toks = []

  for k in query:
    toks.append(f"{k}#{query[k]}".encode())

  return hashlib.md5(b'.'.join(toks)).hexdigest()

def reset_sessions():
  Cache.instance().clear(f".+\\.{SUFFIX}")

def tiebreak_scenario_request(
  session_id: str,
  requests: List[Request],
  query_params: Optional[dict] = None,
  headers: Optional[dict] = None,
):
  if len(requests) == 0:
    return None

  if len(requests) == 1:
    return requests[0]

  parsed_cache: Dict[int, dict] = {}

  if query_params:
    winner = __most_matches_winner(
      requests,
      lambda request: __score_query_params(query_params, __parsed_components(request, parsed_cache)['query_params'])
    )
    if winner:
      return winner

  if headers:
    winner = __most_matches_winner(
      requests,
      lambda request: __score_headers(headers, __parsed_components(request, parsed_cache)['headers'])
    )
    if winner:
      return winner

  return __tiebreak_by_order(session_id, requests)

def __tiebreak_by_order(session_id: str, requests: List[Request]):
  _last_request_id_key = __last_request_id_key(session_id)

  cache = Cache.instance()
  last_request_id_data = cache.read(_last_request_id_key)

  if not last_request_id_data:
    return requests[0]

  last_request_id = last_request_id_data['value']

  for request in requests:
    if request.id > last_request_id:
      return request

  return requests[0]

def __most_matches_winner(candidates: List[Request], score_fn: Callable[[Request], int]) -> Optional[Request]:
  best_score = 0
  winner = None
  tie = False

  for candidate in candidates:
    score = score_fn(candidate)
    if score > best_score:
      best_score = score
      winner = candidate
      tie = False
    elif score == best_score and score > 0:
      tie = True

  if best_score > 0 and not tie:
    return winner

  return None

def __score_query_params(query_params: dict, stored_query_params: dict) -> int:
  score = 0

  for key, param_value in query_params.items():
    if key not in stored_query_params:
      continue

    stored_value = stored_query_params[key]
    values = param_value if isinstance(param_value, list) else [param_value]
    stored_values = stored_value if isinstance(stored_value, list) else [stored_value]

    for value in values:
      if value in stored_values:
        score += 1

  return score

def __score_headers(headers: dict, stored_headers: dict) -> int:
  score = 0
  stored_by_lower = {
    key.lower(): value for key, value in stored_headers.items()
    if not __is_stoobly_header(key)
  }

  for key, value in headers.items():
    if __is_stoobly_header(key):
      continue

    stored_value = stored_by_lower.get(key.lower())
    if stored_value is not None and stored_value == value:
      score += 1

  return score

def __is_stoobly_header(name: str) -> bool:
  return name.lower().startswith(STOOBLY_HEADER_PREFIX)

def __parsed_components(request: Request, cache: Dict[int, dict]) -> dict:
  request_id = request.id
  if request_id in cache:
    return cache[request_id]

  facade = __parse_stored_request(request)
  if facade is None:
    components = { 'query_params': {}, 'headers': {} }
  else:
    components = {
      'query_params': __deflatten_multi_dict(facade.query),
      'headers': dict(facade.headers),
    }

  cache[request_id] = components
  return components

def __parse_stored_request(request: Request) -> Optional[MitmproxyRequestFacade]:
  raw = getattr(request, 'raw', None)
  if not raw:
    return None

  python_request = RawHttpRequestAdapter(raw).to_request()
  http_version = getattr(request, 'http_version', None)
  if isinstance(http_version, float) or isinstance(http_version, int):
    http_version = f"HTTP/{http_version}"
  if not http_version:
    http_version = 'HTTP/1.1'

  mitmproxy_request = PythonRequestAdapterFactory(python_request).mitmproxy_request(http_version)
  return MitmproxyRequestFacade(mitmproxy_request)

def __deflatten_multi_dict(multi_dict) -> dict:
  params = {}
  for name, value in multi_dict.items(multi=True):
    if name not in params:
      params[name] = value
    else:
      if not isinstance(params[name], list):
        params[name] = [params[name]]

      params[name].append(value)
  return params

def __last_request_id_key(_key = None):
  _key = _key or generate_session_id()
  return f"{_key}.{SUFFIX}"
