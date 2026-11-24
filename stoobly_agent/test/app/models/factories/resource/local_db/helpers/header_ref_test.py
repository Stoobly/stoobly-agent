import os
import tempfile

import pytest

from stoobly_agent.app.models.adapters.joined_request_adapter import JoinedRequestAdapter
from stoobly_agent.app.models.adapters.raw_http_request_adapter import RawHttpRequestAdapter
from stoobly_agent.app.models.adapters.raw_http_response_adapter import RawHttpResponseAdapter
from stoobly_agent.app.models.factories.resource.local_db.helpers.body_ref import BODY_REF_HEADER
from stoobly_agent.app.models.factories.resource.local_db.helpers.joined_request_ref import (
  externalize_joined_request,
  reconstitute_joined_request,
)
from stoobly_agent.app.models.factories.resource.local_db.helpers.header_ref import (
  HEADER_REF_HEADER,
  REQUEST_HEADER_DEDUP_LIST,
  RESPONSE_HEADER_DEDUP_LIST,
  content_hash,
  extract_dedup_list_headers,
  full_content_hash,
  headers_dir_path,
  normalize_header_ref,
  read_headers,
  relative_header_ref,
  resolve_header_path,
  write_headers,
)
from stoobly_agent.app.proxy.record.joined_request import REQUEST_DELIMITTER


def _joined(
  request_headers: bytes,
  response_headers: bytes,
  request_body: bytes = b'',
  response_body: bytes = b'',
) -> bytes:
  request = (
    b'GET /api/test HTTP/1.1\r\n'
    + request_headers
    + b'Content-Length: ' + str(len(request_body)).encode() + b'\r\n'
    + b'\r\n' + request_body
  )
  response = (
    b'HTTP/1.1 200 OK\r\n'
    + response_headers
    + b'Content-Length: ' + str(len(response_body)).encode() + b'\r\n'
    + b'\r\n' + response_body
  )
  return REQUEST_DELIMITTER.join([
    b'1 id 1\r\n' + request,
    b'2 id 1 1\r\n' + response,
  ])


def _header_dict_from_raw(raw: bytes, response: bool = False):
  if response:
    return dict(RawHttpResponseAdapter(raw).headers)
  return dict(RawHttpRequestAdapter(raw).headers)


class TestHeaderRef:
  def test_extract_omits_missing_dedup_list_names(self):
    lines = [
      b'Host: example.com',
      b'User-Agent: ua',
      b'Accept: text/html',
      b'Cookie: a=1',
    ]
    remaining, extracted, insert_index = extract_dedup_list_headers(
      lines, REQUEST_HEADER_DEDUP_LIST
    )
    assert remaining == [b'Host: example.com', b'Cookie: a=1']
    assert extracted == b'User-Agent: ua\r\nAccept: text/html'
    assert insert_index == 1
    assert b'origin' not in extracted.lower()
    assert b'referer' not in extracted.lower()

  def test_extract_empty_when_none_in_dedup_list(self):
    lines = [b'Host: example.com', b'Cookie: a=1']
    remaining, extracted, insert_index = extract_dedup_list_headers(
      lines, REQUEST_HEADER_DEDUP_LIST
    )
    assert remaining == lines
    assert extracted == b''
    assert insert_index == 0

  def test_externalize_writes_headers_and_refs(self):
    joined = _joined(
      b'Host: example.com\r\nUser-Agent: ua\r\nAccept: */*\r\n',
      b'Content-Type: application/json\r\nCache-Control: no-cache\r\nVary: Accept\r\n',
      request_body=b'hello',
      response_body=b'world',
    )
    with tempfile.TemporaryDirectory() as slug_dir:
      externalized = externalize_joined_request(joined, slug_dir)

      assert HEADER_REF_HEADER.encode() in externalized
      assert BODY_REF_HEADER.encode() in externalized
      assert b'User-Agent: ua' not in externalized
      assert b'Accept: */*' not in externalized
      assert b'Content-Type: application/json' not in externalized
      assert b'Host: example.com' in externalized

      headers_dir = os.path.join(slug_dir, 'headers')
      assert os.path.isdir(headers_dir)
      header_names = os.listdir(headers_dir)
      assert len(header_names) == 2
      assert all(len(name) == 16 for name in header_names)

      adapter = JoinedRequestAdapter(externalized)
      request_raw = adapter.build_request_string().get(control=False)
      response_raw = adapter.build_response_string().get(control=False)
      req_headers = request_raw.split(b'\r\n\r\n', 1)[0].split(b'\r\n')[1:]
      res_headers = response_raw.split(b'\r\n\r\n', 1)[0].split(b'\r\n')[1:]

      assert req_headers[-1].lower().startswith(BODY_REF_HEADER.lower().encode())
      assert any(h.lower().startswith(HEADER_REF_HEADER.lower().encode()) for h in req_headers)
      header_idx = next(
        i for i, h in enumerate(req_headers)
        if h.lower().startswith(HEADER_REF_HEADER.lower().encode())
      )
      body_idx = next(
        i for i, h in enumerate(req_headers)
        if h.lower().startswith(BODY_REF_HEADER.lower().encode())
      )
      assert header_idx < body_idx

      assert res_headers[-1].lower().startswith(BODY_REF_HEADER.lower().encode())

  def test_no_dedup_list_headers_skips_header_ref(self):
    joined = _joined(
      b'Host: example.com\r\nCookie: a=1\r\n',
      b'Set-Cookie: b=2\r\n',
      request_body=b'x',
      response_body=b'y',
    )
    with tempfile.TemporaryDirectory() as slug_dir:
      externalized = externalize_joined_request(joined, slug_dir)
      assert HEADER_REF_HEADER.encode() not in externalized
      assert BODY_REF_HEADER.encode() in externalized
      assert not os.path.isdir(os.path.join(slug_dir, 'headers'))

  def test_header_only_externalize_without_bodies(self):
    joined = _joined(
      b'Host: example.com\r\nUser-Agent: ua\r\n',
      b'Cache-Control: max-age=0\r\n',
    )
    with tempfile.TemporaryDirectory() as slug_dir:
      externalized = externalize_joined_request(joined, slug_dir)
      assert HEADER_REF_HEADER.encode() in externalized
      assert BODY_REF_HEADER.encode() not in externalized
      assert os.path.isdir(os.path.join(slug_dir, 'headers'))
      assert not os.path.isdir(os.path.join(slug_dir, 'bodies'))

  def test_shared_header_blob_dedupes(self):
    # Same dedup-list subset on request and response is unlikely with different
    # dedup lists; write the same bytes twice via write_headers instead.
    with tempfile.TemporaryDirectory() as slug_dir:
      payload = b'Content-Type: text/plain'
      h1 = write_headers(slug_dir, payload)
      h2 = write_headers(slug_dir, payload)
      assert h1 == h2
      assert len(h1) == 16
      assert len(os.listdir(os.path.join(slug_dir, 'headers'))) == 1

  def test_write_headers_truncated_collision_falls_back_to_full_digest(self):
    with tempfile.TemporaryDirectory() as slug_dir:
      payload = b'User-Agent: collision-test'
      short = content_hash(payload)
      headers = headers_dir_path(slug_dir)
      os.makedirs(headers)
      with open(os.path.join(headers, short), 'wb') as fp:
        fp.write(b'planted-different-bytes')

      hash_value = write_headers(slug_dir, payload)
      assert hash_value == full_content_hash(payload)
      assert len(hash_value) == 64
      assert read_headers(slug_dir, f'headers/{hash_value}') == payload
      with open(os.path.join(headers, short), 'rb') as fp:
        assert fp.read() == b'planted-different-bytes'

  def test_reconstitute_restores_header_values(self):
    joined = _joined(
      b'Host: example.com\r\nUser-Agent: ua\r\nAccept: text/html\r\nOrigin: https://ex.com\r\n',
      b'Content-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\n',
      request_body=b'req',
      response_body=b'res',
    )
    with tempfile.TemporaryDirectory() as slug_dir:
      externalized = externalize_joined_request(joined, slug_dir)
      restored = reconstitute_joined_request(externalized, slug_dir)

      assert HEADER_REF_HEADER.encode() not in restored
      assert BODY_REF_HEADER.encode() not in restored
      # Contiguous dedup-list blocks round-trip exactly
      assert restored == joined

      orig_adapter = JoinedRequestAdapter(joined)
      rest_adapter = JoinedRequestAdapter(restored)

      orig_req = _header_dict_from_raw(orig_adapter.build_request_string().get(control=False))
      rest_req = _header_dict_from_raw(rest_adapter.build_request_string().get(control=False))
      assert rest_req['User-Agent'] == orig_req['User-Agent']
      assert rest_req['Accept'] == orig_req['Accept']
      assert rest_req['Origin'] == orig_req['Origin']
      assert rest_req['Host'] == orig_req['Host']

      orig_res = _header_dict_from_raw(
        orig_adapter.build_response_string().get(control=False), response=True
      )
      rest_res = _header_dict_from_raw(
        rest_adapter.build_response_string().get(control=False), response=True
      )
      assert rest_res['Content-Type'] == orig_res['Content-Type']
      assert rest_res['Access-Control-Allow-Origin'] == orig_res['Access-Control-Allow-Origin']

      assert rest_adapter.build_request_string().get(control=False).endswith(b'req')
      assert rest_adapter.build_response_string().get(control=False).endswith(b'res')

  def test_normalize_rejects_traversal_and_absolute(self):
    assert normalize_header_ref('headers/abc') == 'headers/abc'
    assert normalize_header_ref('/headers/abc') == 'headers/abc'

    for bad in ('/etc/passwd', 'headers/../secret', '../headers/abc', 'etc/passwd', ''):
      with pytest.raises(ValueError, match='Invalid header ref'):
        normalize_header_ref(bad)

  def test_resolve_stays_under_slug_dir(self):
    with tempfile.TemporaryDirectory() as slug_dir:
      path = resolve_header_path(slug_dir, 'headers/deadbeef')
      assert path.startswith(slug_dir)
      assert path.endswith(os.path.join('headers', 'deadbeef'))

  def test_resolve_rejects_symlink_escape(self):
    with tempfile.TemporaryDirectory() as slug_dir:
      headers = os.path.join(slug_dir, 'headers')
      os.makedirs(headers)
      target = os.path.join(slug_dir, 'outside-secret')
      with open(target, 'wb') as fp:
        fp.write(b'secret')
      os.symlink(target, os.path.join(headers, 'deadbeef'))

      with pytest.raises(ValueError, match='Invalid header ref'):
        resolve_header_path(slug_dir, 'headers/deadbeef')

  def test_resolve_rejects_headers_dir_symlink_escape(self):
    with tempfile.TemporaryDirectory() as root:
      slug_dir = os.path.join(root, 'slug')
      os.makedirs(slug_dir)
      outside = os.path.join(root, 'outside')
      os.makedirs(outside)
      os.symlink(outside, os.path.join(slug_dir, 'headers'))

      with pytest.raises(ValueError, match='Invalid header ref'):
        resolve_header_path(slug_dir, 'headers/deadbeef')

  def test_relative_header_ref(self):
    assert relative_header_ref('abc') == 'headers/abc'

  def test_response_dedup_list_distinct_from_request(self):
    assert 'user-agent' in REQUEST_HEADER_DEDUP_LIST
    assert 'user-agent' not in RESPONSE_HEADER_DEDUP_LIST
    assert 'cache-control' in RESPONSE_HEADER_DEDUP_LIST
    assert 'cache-control' not in REQUEST_HEADER_DEDUP_LIST
    assert 'server' in RESPONSE_HEADER_DEDUP_LIST
    assert 'x-content-type-options' in RESPONSE_HEADER_DEDUP_LIST
