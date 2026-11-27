from stoobly_agent.app.models.adapters.raw_http_response_adapter import RawHttpResponseAdapter


class TestRawHttpResponseAdapterContentLength:

  def test_to_response_strips_transfer_encoding_chunked(self):
    raw = (
      b'HTTP/1.1 200 OK\r\n'
      b'Content-Type: text/event-stream\r\n'
      b'Transfer-Encoding: chunked\r\n'
      b'\r\n'
      b'data: hello\n\n'
    )
    response = RawHttpResponseAdapter(raw).to_response()

    assert response.headers.get('Content-Length') == str(len(b'data: hello\n\n'))
    assert 'Transfer-Encoding' not in response.headers
    assert response.raw.headers.getlist('Transfer-Encoding') == []

  def test_to_response_keeps_non_chunked_transfer_encoding(self):
    raw = (
      b'HTTP/1.1 200 OK\r\n'
      b'Transfer-Encoding: gzip\r\n'
      b'Transfer-Encoding: chunked\r\n'
      b'\r\n'
      b'body'
    )
    response = RawHttpResponseAdapter(raw).to_response()

    assert response.headers.get('Content-Length') == '4'
    assert response.raw.headers.getlist('Transfer-Encoding') == ['gzip']
    assert 'chunked' not in (response.headers.get('Transfer-Encoding') or '').lower()


class TestRawHttpResponseAdapterSetCookie:

  def test_repeated_set_cookie_kept_as_list(self):
    raw = (
      b'HTTP/1.1 200 OK\r\n'
      b'Set-Cookie: session=abc; Path=/\r\n'
      b'Set-Cookie: user=john; Expires=Wed, 21 Oct 2015 07:28:00 GMT\r\n'
      b'Content-Type: text/plain\r\n'
      b'\r\n'
      b'ok'
    )
    adapter = RawHttpResponseAdapter(raw)

    assert adapter.headers['Set-Cookie'] == [
      'session=abc; Path=/',
      'user=john; Expires=Wed, 21 Oct 2015 07:28:00 GMT',
    ]
    assert adapter.headers['Content-Type'] == 'text/plain'

  def test_to_response_preserves_repeated_set_cookie(self):
    raw = (
      b'HTTP/1.1 200 OK\r\n'
      b'Set-Cookie: session=abc; Path=/\r\n'
      b'Set-Cookie: user=john; Expires=Wed, 21 Oct 2015 07:28:00 GMT\r\n'
      b'\r\n'
      b'ok'
    )
    response = RawHttpResponseAdapter(raw).to_response()

    assert response.raw.headers.getlist('Set-Cookie') == [
      'session=abc; Path=/',
      'user=john; Expires=Wed, 21 Oct 2015 07:28:00 GMT',
    ]

  def test_str_emits_separate_set_cookie_lines(self):
    raw = (
      b'HTTP/1.1 200 OK\r\n'
      b'Set-Cookie: a=1\r\n'
      b'Set-Cookie: b=2\r\n'
      b'\r\n'
      b'ok'
    )
    text = str(RawHttpResponseAdapter(raw))

    assert 'Set-Cookie: a=1' in text
    assert 'Set-Cookie: b=2' in text
    assert 'Set-Cookie: a=1, b=2' not in text
