from dataclasses import dataclass
from typing import Any, Callable, Optional


@dataclass
class RequestDiffAnalysis:
  """Result of comparing a snapshot request to the current resource; used for printing once without recomputing."""

  request_key_str: str
  url_line: str
  snapshot_path: str
  snapshot_req_body: Any
  current_req_body: Any
  snapshot_res_body: Any
  current_res_body: Any
  snapshot_req_headers_str: Optional[str]
  current_req_headers_str: Optional[str]
  snapshot_res_headers_str: Optional[str]
  current_res_headers_str: Optional[str]
  request_headers_has_diff: bool
  response_headers_has_diff: bool
  request_body_has_diff: bool
  response_body_has_diff: bool
  has_diff: bool


def emit_request_diff_header(
  url_line: str,
  request_key: str,
  snapshot_path: str,
  *,
  emit: Callable[[str], None] = print,
) -> None:
  """Shared layout for request URL, key, and snapshot path."""
  emit(f"--- Request {url_line} {request_key}")
  emit("")
  emit("~ Snapshot Path")
  emit(snapshot_path)
  emit("")


def analyze_request_diff(request_snapshot: Any, current_request: Any) -> Optional[RequestDiffAnalysis]:
  """
  Compare snapshot vs current request/response; returns None when the snapshot has no request bytes to compare.
  """
  from stoobly_agent.app.models.adapters.orm import OrmResponseAdapterFactory
  from stoobly_agent.app.models.adapters.raw_http_request_adapter import RawHttpRequestAdapter

  try:
    request_key_str = current_request.key()
  except Exception:
    request_key_str = request_snapshot.uuid

  snapshot_raw = request_snapshot.request
  if snapshot_raw is None:
    return None

  snapshot_py_req = request_snapshot.python_request
  snapshot_py_res = request_snapshot.python_response
  snapshot_url = snapshot_py_req.url if snapshot_py_req else None
  snapshot_req_body = snapshot_py_req.data if snapshot_py_req else None
  snapshot_res_body = snapshot_py_res.content if snapshot_py_res else None
  snapshot_req_headers = None
  snapshot_res_headers = None
  if snapshot_py_req and hasattr(snapshot_py_req, "headers"):
    snapshot_req_headers = snapshot_py_req.headers
  if snapshot_py_res and hasattr(snapshot_py_res, "headers"):
    snapshot_res_headers = snapshot_py_res.headers

  current_url = getattr(current_request, "url", None)
  current_req_headers = None
  current_req_body = None
  if hasattr(current_request, "raw") and current_request.raw:
    try:
      adapter = RawHttpRequestAdapter(current_request.raw)
      current_req_body = adapter.body
      current_req_headers = adapter.headers
      current_url = adapter.url
    except Exception:
      current_req_body = None
      current_req_headers = None

  current_py_res = OrmResponseAdapterFactory(current_request.response).python_response()
  current_res_body = current_py_res.content if current_py_res else None
  current_res_headers = current_py_res.headers if current_py_res and hasattr(current_py_res, "headers") else None

  def headers_to_string(h):
    if not h:
      return None
    try:
      items = []
      for k in sorted(h.keys(), key=lambda s: str(s).lower()):
        items.append(f"{k}: {h.get(k)}")
      return "\n".join(items)
    except Exception:
      return None

  url_before = snapshot_url or ""
  url_after = current_url or ""
  url_has_diff = url_before != url_after

  snapshot_req_headers_str = headers_to_string(snapshot_req_headers)
  current_req_headers_str = headers_to_string(current_req_headers)
  request_headers_has_diff = (snapshot_req_headers_str or "") != (current_req_headers_str or "")
  request_body_has_diff = (snapshot_req_body or "") != (current_req_body or "")

  snapshot_res_headers_str = headers_to_string(snapshot_res_headers)
  current_res_headers_str = headers_to_string(current_res_headers)
  response_headers_has_diff = (snapshot_res_headers_str or "") != (current_res_headers_str or "")
  response_body_has_diff = (snapshot_res_body or "") != (current_res_body or "")

  has_diff = (
    url_has_diff
    or request_headers_has_diff
    or request_body_has_diff
    or response_headers_has_diff
    or response_body_has_diff
  )

  url_line = current_url or snapshot_url or ""

  return RequestDiffAnalysis(
    request_key_str=request_key_str,
    url_line=url_line,
    snapshot_path=request_snapshot.path,
    snapshot_req_body=snapshot_req_body,
    current_req_body=current_req_body,
    snapshot_res_body=snapshot_res_body,
    current_res_body=current_res_body,
    snapshot_req_headers_str=snapshot_req_headers_str,
    current_req_headers_str=current_req_headers_str,
    snapshot_res_headers_str=snapshot_res_headers_str,
    current_res_headers_str=current_res_headers_str,
    request_headers_has_diff=request_headers_has_diff,
    response_headers_has_diff=response_headers_has_diff,
    request_body_has_diff=request_body_has_diff,
    response_body_has_diff=response_body_has_diff,
    has_diff=has_diff,
  )


def emit_request_diff(
  analysis: RequestDiffAnalysis,
  *,
  full: bool = False,
  emit: Callable[[str], None] = print,
) -> None:
  """Print a single request diff report from a prior analysis (no recomputation)."""
  from stoobly_agent.app.proxy.test.helpers.diff_service import diff as diff_strings

  if not analysis.has_diff:
    return

  emit_request_diff_header(
    analysis.url_line,
    analysis.request_key_str,
    analysis.snapshot_path,
    emit=emit,
  )

  if full and analysis.request_headers_has_diff:
    emit("~ Request headers")
    emit(diff_strings(analysis.snapshot_req_headers_str or "", analysis.current_req_headers_str or ""))
    emit("")

  if full and analysis.request_body_has_diff:
    emit("~ Request body")
    emit(diff_strings(analysis.snapshot_req_body or "", analysis.current_req_body or ""))
    emit("")

  if full and analysis.response_headers_has_diff:
    emit("~ Response headers")
    emit(diff_strings(analysis.snapshot_res_headers_str or "", analysis.current_res_headers_str or ""))
    emit("")

  if full and analysis.response_body_has_diff:
    emit("~ Response body")
    emit(diff_strings(analysis.snapshot_res_body or "", analysis.current_res_body or ""))
    emit("")


def print_request_diff(request_snapshot: Any, current_request: Any, *, full: bool = False, emit: bool = True) -> bool:
  """
  Print diffs for a single request, returning True if any diffs were printed.
  Follows formatting used by scenario diffs:
    - Header: --- URL, ~ Request Key, ~ Snapshot Path
    - When full=True: ~ Request headers / ~ Request body / ~ Response headers / ~ Response body with unified diffs
  Snapshot is treated as previous, current as next.
  """
  analysis = analyze_request_diff(request_snapshot, current_request)
  if analysis is None or not analysis.has_diff:
    return False

  if emit:

    def out(value: str = "") -> None:
      print(value)

    emit_request_diff(analysis, full=full, emit=out)

  return True
