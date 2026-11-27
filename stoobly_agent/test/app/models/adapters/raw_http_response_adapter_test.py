from stoobly_agent.app.models.adapters.raw_http_response_adapter import RawHttpResponseAdapter


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
