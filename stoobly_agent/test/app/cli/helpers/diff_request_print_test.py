import io
import sys
import types

import pytest

from stoobly_agent.app.cli.helpers.diff_request_print import print_request_diff


class _StubPythonRequest:
  def __init__(self, url=None, data=None, headers=None):
    self.url = url
    self.data = data
    self.headers = headers


class _StubPythonResponse:
  def __init__(self, content=None, headers=None):
    self.content = content
    self.headers = headers


class _StubSnapshot:
  def __init__(self, uuid='u-1', path='/tmp/snap', py_req=None, py_res=None):
    self.uuid = uuid
    self.path = path
    self._py_req = py_req
    self._py_res = py_res
    self.request = b'RAW'  # non-None sentinel
  
  @property
  def python_request(self):
    return self._py_req
  
  @property
  def python_response(self):
    return self._py_res


class _StubCurrentReq:
  def __init__(self, url=None, body=None, headers=None, res_content=None, res_headers=None):
    self.url = url
    # Simulate minimal surface used in diff_request_print:
    self.raw = None
    # Attach a tiny adapter-compatible shape by monkeypatching via attributes accessed later
    self._body = body
    self._headers = headers
    # Provide response adapter factory compatible shape
    self._res = types.SimpleNamespace(
      content=res_content,
      headers=res_headers,
    )
  
  def key(self):
    return 'p0.i00000000000000000000000000000000'
  
  @property
  def response(self):
    # OrmResponseAdapterFactory(...) only needs a truthy object; contents accessed later
    return self._res


@pytest.mark.parametrize("snap_body,cur_body,expected_any", [
  ('abc', None, True),    # one-sided: current missing
  (None, 'abc', True),    # one-sided: snapshot missing
  ('abc', 'xyz', True),   # different
  ('', '', False),        # both empty
  (None, None, False),    # both missing
])
def test_request_body_one_sided_and_diff_detection(snap_body, cur_body, expected_any, monkeypatch):
  # Build snapshot/current with only request bodies differing
  snapshot = _StubSnapshot(py_req=_StubPythonRequest(url='u', data=snap_body))
  current = _StubCurrentReq(url='u', body=cur_body)
  current.raw = b'X'  # trigger raw adapter path

  # Monkeypatch OrmResponseAdapterFactory().python_response() to return None (no response diff)
  from stoobly_agent.app.models.adapters.orm import OrmResponseAdapterFactory
  class _FakeRespAdapter:
    def __init__(self, *_args, **_kwargs):
      pass
    def python_response(self):
      return None
  monkeypatch.setattr('stoobly_agent.app.models.adapters.orm.OrmResponseAdapterFactory', _FakeRespAdapter)

  # Monkeypatch RawHttpRequestAdapter to supply the current request body without needing a real raw HTTP request
  class _FakeRawReqAdapter:
    def __init__(self, raw):
      self.body = cur_body
      self.headers = None
      self.url = current.url
  monkeypatch.setattr('stoobly_agent.app.models.adapters.raw_http_request_adapter.RawHttpRequestAdapter', _FakeRawReqAdapter)

  # Capture stdout to ensure printing occurs only when expected
  buf = io.StringIO()
  old = sys.stdout
  sys.stdout = buf
  try:
    any_diffs = print_request_diff(snapshot, current, full=True)
  finally:
    sys.stdout = old
  out = buf.getvalue()

  assert any_diffs is expected_any
  if expected_any:
    assert '~ Request body' in out
  else:
    assert out == ''


def test_url_diff_sets_any_diffs_true_and_prints(monkeypatch):
  snapshot = _StubSnapshot(py_req=_StubPythonRequest(url='http://a'))
  current = _StubCurrentReq(url='http://b')

  # Ensure no response present
  from stoobly_agent.app.models.adapters.orm import OrmResponseAdapterFactory
  class _FakeRespAdapter:
    def __init__(self, *_args, **_kwargs):
      pass
    def python_response(self):
      return None
  monkeypatch.setattr('stoobly_agent.app.models.adapters.orm.OrmResponseAdapterFactory', _FakeRespAdapter)

  buf = io.StringIO()
  old = sys.stdout
  sys.stdout = buf
  try:
    any_diffs = print_request_diff(snapshot, current, full=False)
  finally:
    sys.stdout = old
  out = buf.getvalue()

  assert any_diffs is True
  assert '--- http://b' in out
