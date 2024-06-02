import hashlib

from typing import List

from stoobly_agent.lib.cache import Cache
from stoobly_agent.lib.orm.request import Request

PREFIX = 'last_request_id'

def access_request(session_id: str, request_id: int, timeout = None):
  cache = Cache.instance()
  _last_request_id_key = __last_request_id_key(session_id)
  cache.write(_last_request_id_key, request_id, timeout)

def generate_session_id(query: dict):
  toks = []

  for k in query:
    toks.append(f"{k}#{query[k]}".encode())

  return hashlib.md5(b'.'.join(toks)).hexdigest()

def reset():
  Cache.instance().clear(f".+\.{PREFIX}")

def tiebreak_scenario_request(session_id: str, requests: List[Request]):
  if len(requests) == 0:
    return None

  if len(requests) == 1:
    return requests[0]

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

def __last_request_id_key(_key = None):
  _key = _key or generate_session_id()
  return f"{_key}.{PREFIX}"