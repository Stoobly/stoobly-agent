from typing import Any

def print_request_diff(request_snapshot: Any, current_request: Any, *, full: bool = False) -> bool:
  """
  Print diffs for a single request, returning True if any diffs were printed.
  Follows formatting used by scenario diffs:
    - Header: '=== Request <request_key>'
    - Next line: snapshot path
    - Then either full raw diff (when full=True) or selective sections:
      --- URL
      --- Request body
      --- Response body
  Snapshot is treated as previous, current as next.
  """
  from stoobly_agent.app.proxy.test.helpers.diff_service import diff as diff_strings
  from stoobly_agent.app.models.adapters.orm import JoinedRequestStringAdapter, OrmResponseAdapterFactory
  from stoobly_agent.app.models.adapters.raw_http_request_adapter import RawHttpRequestAdapter

  # Derive a nice request key string
  try:
    request_key_str = current_request.key()
  except Exception:
    request_key_str = request_snapshot.uuid

  snapshot_raw = request_snapshot.request
  if snapshot_raw is None:
    return False

  # Component-wise diffs (URL, request headers, request body, response headers, response body)
  # Snapshot side
  snapshot_py_req = request_snapshot.python_request
  snapshot_py_res = request_snapshot.python_response
  snapshot_url = snapshot_py_req.url if snapshot_py_req else None
  snapshot_req_body = snapshot_py_req.data if snapshot_py_req else None
  snapshot_res_body = snapshot_py_res.content if snapshot_py_res else None
  snapshot_req_headers = None
  snapshot_res_headers = None
  if snapshot_py_req and hasattr(snapshot_py_req, 'headers'):
    snapshot_req_headers = snapshot_py_req.headers
  if snapshot_py_res and hasattr(snapshot_py_res, 'headers'):
    snapshot_res_headers = snapshot_py_res.headers

  # Current side
  current_url = getattr(current_request, 'url', None)
  current_req_headers = None
  current_req_body = None
  if hasattr(current_request, 'raw') and current_request.raw:
    try:
      adapter = RawHttpRequestAdapter(current_request.raw)
      current_req_body = adapter.body
      current_req_headers = adapter.headers
      # Prefer raw URL from the request line to avoid URL-encoding differences
      current_url = adapter.url
    except Exception:
      current_req_body = None
      current_req_headers = None

  current_py_res = OrmResponseAdapterFactory(current_request.response).python_response()
  current_res_body = current_py_res.content if current_py_res else None
  current_res_headers = current_py_res.headers if current_py_res and hasattr(current_py_res, 'headers') else None

  printed_header = False
  any_diffs = False

  def header_once():
    nonlocal printed_header
    if not printed_header:
      print("--- Request Key")
      print(request_key_str)
      print()
      print("--- Snapshot Path")
      print(request_snapshot.path)
      print()
      printed_header = True

  # URL section: only print if there is a difference
  url_before = snapshot_url or ''
  url_after = current_url or ''
  if url_before != url_after:
    print('=== Request')
    print(diff_strings(url_before, url_after))
    print()
    # Then print Request Snapshot header (path + key)
    header_once()
    any_diffs = True

  # Normalize headers to sorted "Key: Value" lines for stable diffs
  def headers_to_string(h):
    if not h:
      return None
    try:
      items = []
      # CaseInsensitiveDict or dict-like
      for k in sorted(h.keys(), key=lambda s: str(s).lower()):
        items.append(f"{k}: {h.get(k)}")
      return "\n".join(items)
    except Exception:
      return None

  snapshot_req_headers_str = headers_to_string(snapshot_req_headers)
  current_req_headers_str = headers_to_string(current_req_headers)
  if full:
    # Only print headers if there is a diff
    if (snapshot_req_headers_str or '') != (current_req_headers_str or ''):
      header_once()
      print('--- Request headers')
      print(diff_strings(snapshot_req_headers_str or '', current_req_headers_str or ''))
      print()
      any_diffs = True
  elif snapshot_req_headers_str is not None and current_req_headers_str is not None and snapshot_req_headers_str != current_req_headers_str:
    header_once()
    print('--- Request headers')
    print(diff_strings(snapshot_req_headers_str, current_req_headers_str))
    print()
    any_diffs = True

  if (snapshot_req_body or '') != (current_req_body or ''):
    header_once()
    print('--- Request body')
    print(diff_strings(snapshot_req_body or '', current_req_body or ''))
    print()
    any_diffs = True

  snapshot_res_headers_str = headers_to_string(snapshot_res_headers)
  current_res_headers_str = headers_to_string(current_res_headers)
  if full:
    # Only print headers if there is a diff
    if (snapshot_res_headers_str or '') != (current_res_headers_str or ''):
      header_once()
      print('--- Response headers')
      print(diff_strings(snapshot_res_headers_str or '', current_res_headers_str or ''))
      print()
      any_diffs = True
  elif snapshot_res_headers_str is not None and current_res_headers_str is not None and snapshot_res_headers_str != current_res_headers_str:
    header_once()
    print('--- Response headers')
    print(diff_strings(snapshot_res_headers_str, current_res_headers_str))
    print()
    any_diffs = True

  if (snapshot_res_body or '') != (current_res_body or ''):
    header_once()
    print('--- Response body')
    print(diff_strings(snapshot_res_body or '', current_res_body or ''))
    print()
    any_diffs = True

  return any_diffs
