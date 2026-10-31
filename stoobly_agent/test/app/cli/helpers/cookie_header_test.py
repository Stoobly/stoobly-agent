import http.cookiejar
import io
from unittest.mock import patch

from stoobly_agent.app.cli.helpers.cookie_header import build_cookie_header

URL = 'https://example.com/api'


class TestBuildCookieHeader:

  def test_returns_none_for_empty_args(self):
    assert build_cookie_header((), URL) is None
    assert build_cookie_header([], URL) is None
    assert build_cookie_header(None, URL) is None

  def test_uses_cookie_string_with_equals(self):
    assert build_cookie_header(['session=abc123'], URL) == 'session=abc123'

  def test_merges_multiple_cookie_strings(self):
    result = build_cookie_header(['session=abc123', 'user=john'], URL)
    assert result == 'session=abc123; user=john'

  def test_strips_cookie_string(self):
    assert build_cookie_header(['  session=abc123  '], URL) == 'session=abc123'

  def test_reads_raw_cookie_file(self, tmp_path):
    cookie_file = tmp_path / 'cookies.txt'
    cookie_file.write_text('token=xyz; theme=dark')

    result = build_cookie_header([str(cookie_file)], URL)
    assert result == 'token=xyz; theme=dark'

  def test_reads_set_cookie_file(self, tmp_path):
    cookie_file = tmp_path / 'set_cookies.txt'
    cookie_file.write_text(
      'Set-Cookie: session=abc; Path=/\n'
      'Set-Cookie: user=john; HttpOnly\n'
    )

    result = build_cookie_header([str(cookie_file)], URL)
    assert result == 'session=abc; user=john'

  def test_skips_comments_and_blank_lines_in_file(self, tmp_path):
    cookie_file = tmp_path / 'cookies.txt'
    cookie_file.write_text('# comment\n\nsession=abc\n')

    result = build_cookie_header([str(cookie_file)], URL)
    assert result == 'session=abc'

  def test_ignores_missing_file(self):
    assert build_cookie_header(['/does/not/exist'], URL) is None

  def test_ignores_empty_file(self, tmp_path):
    cookie_file = tmp_path / 'empty.txt'
    cookie_file.write_text('')

    assert build_cookie_header([str(cookie_file)], URL) is None

  def test_reads_netscape_cookie_jar(self, tmp_path):
    cookie_file = tmp_path / 'cookies.txt'
    jar = http.cookiejar.MozillaCookieJar(str(cookie_file))
    cookie = http.cookiejar.Cookie(
      version=0,
      name='session',
      value='abc123',
      port=None,
      port_specified=False,
      domain='example.com',
      domain_specified=True,
      domain_initial_dot=False,
      path='/',
      path_specified=True,
      secure=True,
      expires=None,
      discard=True,
      comment=None,
      comment_url=None,
      rest={},
      rfc2109=False,
    )
    jar.set_cookie(cookie)
    jar.save(ignore_discard=True, ignore_expires=True)

    result = build_cookie_header([str(cookie_file)], URL)
    assert result == 'session=abc123'

  def test_reads_from_stdin(self):
    with patch('sys.stdin', io.StringIO('stdin=cookie')):
      result = build_cookie_header(['-'], URL)
    assert result == 'stdin=cookie'

  def test_merges_string_and_file(self, tmp_path):
    cookie_file = tmp_path / 'cookies.txt'
    cookie_file.write_text('from_file=1')

    result = build_cookie_header(['from_string=1', str(cookie_file)], URL)
    assert result == 'from_string=1; from_file=1'
