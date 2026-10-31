import http.cookiejar
import os
import sys
import urllib.request

def build_cookie_header(cookie_args, url):
  """
  Build a Cookie header value from curl-style -b/--cookie arguments.

  If an argument contains '=', it is treated as Cookie header data
  (e.g. "NAME1=VALUE1; NAME2=VALUE2"). Otherwise it is treated as a
  filename to read cookies from (Netscape/Mozilla jar, Set-Cookie lines,
  or a raw Cookie header value). Use "-" to read from stdin.
  """
  if not cookie_args:
    return None

  parts = []
  for arg in cookie_args:
    # curl: if no '=' in the argument, treat it as a filename
    if '=' in arg:
      parts.append(arg.strip())
      continue

    if arg == '-':
      content = sys.stdin.read().strip()
      if content:
        parts.append(content)
      continue

    if not os.path.isfile(arg):
      continue

    try:
      jar = http.cookiejar.MozillaCookieJar(arg)
      jar.load(ignore_discard=True, ignore_expires=True)
      request = urllib.request.Request(url)
      jar.add_cookie_header(request)
      cookie_header = request.get_header('Cookie')
      if cookie_header:
        parts.append(cookie_header)
      continue
    except http.cookiejar.LoadError:
      pass

    with open(arg) as fp:
      content = fp.read().strip()

    if not content:
      continue

    # Support Set-Cookie style lines or a raw Cookie header value
    set_cookie_values = []
    for line in content.splitlines():
      line = line.strip()
      if not line or line.startswith('#'):
        continue
      if line.lower().startswith('set-cookie:'):
        name_value = line.split(':', 1)[1].strip().split(';', 1)[0].strip()
        if name_value:
          set_cookie_values.append(name_value)
      else:
        set_cookie_values.append(line)

    if set_cookie_values:
      parts.append('; '.join(set_cookie_values))

  return '; '.join(parts) if parts else None
